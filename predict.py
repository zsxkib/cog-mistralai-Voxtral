# Prediction interface for Cog ⚙️
# https://cog.run/python

import os
import torch
from cog import BasePredictor, Input, Path
from transformers import AutoProcessor, VoxtralForConditionalGeneration

MODEL_CACHE = "model_cache"
os.environ["HF_HOME"] = MODEL_CACHE
os.environ["TORCH_HOME"] = MODEL_CACHE
os.environ["HF_DATASETS_CACHE"] = MODEL_CACHE
os.environ["TRANSFORMERS_CACHE"] = MODEL_CACHE
os.environ["HUGGINGFACE_HUB_CACHE"] = MODEL_CACHE

LANGUAGES = {
    "English": "en",
    "French": "fr",
    "German": "de", 
    "Spanish": "es",
    "Italian": "it",
    "Portuguese": "pt",
    "Dutch": "nl",
    "Russian": "ru",
    "Chinese": "zh",
    "Japanese": "ja",
    "Arabic": "ar",
}


class Predictor(BasePredictor):
    def setup(self) -> None:
        """Load the models into memory to make running multiple predictions efficient"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")

        # Load Voxtral Mini model and processor (3B)
        print("Loading Voxtral Mini (3B) model...")
        self.voxtral_mini_processor = AutoProcessor.from_pretrained(
            "MohamedRashad/Voxtral-Mini-3B-2507-transformers",
            cache_dir=MODEL_CACHE
        )
        self.voxtral_mini_model = VoxtralForConditionalGeneration.from_pretrained(
            "MohamedRashad/Voxtral-Mini-3B-2507-transformers",
            torch_dtype=torch.bfloat16,
            cache_dir=MODEL_CACHE
        )
        self.voxtral_mini_model = self.voxtral_mini_model.to(self.device)
        
        # Load Voxtral Small model and processor (24B)
        print("Loading Voxtral Small (24B) model...")
        self.voxtral_small_processor = AutoProcessor.from_pretrained(
            "MohamedRashad/Voxtral-Small-24B-2507-transformers",
            cache_dir=MODEL_CACHE
        )
        self.voxtral_small_model = VoxtralForConditionalGeneration.from_pretrained(
            "MohamedRashad/Voxtral-Small-24B-2507-transformers",
            torch_dtype=torch.bfloat16,
            cache_dir=MODEL_CACHE
        )
        self.voxtral_small_model = self.voxtral_small_model.to(self.device)
        
        print("Models loaded successfully!")

    def predict(
        self,
        audio: Path = Input(
            description="Audio file to process."
        ),
        mode: str = Input(
            description="Choose processing mode: 'transcription' converts speech to text, 'understanding' analyzes audio content using prompts.",
            choices=["transcription", "understanding"],
            default="transcription",
        ),
        prompt: str = Input(
            description="Question or instruction for understanding mode (e.g., 'What is the speaker discussing?', 'Summarize this audio'). Ignored in transcription mode.",
            default="What can you tell me about this audio?",
        ),
        language: str = Input(
            description="Audio language. 'Auto-detect' works for most content, or choose a specific language for better accuracy.",
            choices=["Auto-detect"] + list(LANGUAGES.keys()),
            default="Auto-detect",
        ),
        model_size: str = Input(
            description="Model selection: 'mini' (3B) is faster and uses less GPU memory, 'small' (24B) provides higher accuracy for complex audio.",
            choices=["mini", "small"],
            default="mini",
        ),
        max_tokens: int = Input(
            description="Maximum response length. Higher values allow longer outputs but increase processing time.",
            ge=50,
            le=1000,
            default=500,
        ),
    ) -> str:
        """
        Voxtral speech recognition and audio understanding.
        
        This model offers two modes:
        - Transcription: Convert speech to text
        - Understanding: Ask questions about audio content (e.g., summarize, analyze, extract information)
        """
        
        # Select model based on size parameter
        if model_size == "mini":
            model = self.voxtral_mini_model
            processor = self.voxtral_mini_processor
            repo_id = "MohamedRashad/Voxtral-Mini-3B-2507-transformers"
            print("Using Voxtral Mini (3B) model")
        else:
            model = self.voxtral_small_model
            processor = self.voxtral_small_processor
            repo_id = "MohamedRashad/Voxtral-Small-24B-2507-transformers"
            print("Using Voxtral Small (24B) model")
        
        print(f"Mode: {mode}")
        
        if mode == "transcription":
            return self._transcribe_audio(audio, language, model, processor, repo_id, max_tokens)
        else:
            return self._understand_audio(audio, prompt, model, processor, max_tokens)
    
    def _transcribe_audio(self, audio, language, model, processor, repo_id, max_tokens):
        """Convert speech to text"""
        # Handle language selection
        if language == "Auto-detect":
            language_code = "en"  # Use English as fallback for auto-detect
            print("Auto-detecting language (using English as fallback)")
        else:
            language_code = LANGUAGES[language]
            print(f"Transcribing in {language}")
        
        # Process audio using transcription request
        print("Processing audio for transcription...")
        inputs = processor.apply_transcrition_request(
            language=language_code, 
            audio=str(audio), 
            model_id=repo_id
        )
        inputs = inputs.to(self.device, dtype=torch.bfloat16)
        
        # Generate transcription
        print("Generating transcription...")
        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=max_tokens)
        
        # Decode only the newly generated tokens
        decoded_outputs = processor.batch_decode(
            outputs[:, inputs.input_ids.shape[1]:], 
            skip_special_tokens=True
        )
        
        transcription = decoded_outputs[0].strip()
        print(f"Transcription completed: {len(transcription)} characters")
        
        return transcription
    
    def _understand_audio(self, audio, prompt, model, processor, max_tokens):
        """Analyze audio content using a prompt"""
        print(f"Analyzing audio with prompt: {prompt}")
        
        # Structure conversation for audio understanding
        conversation = [
            {
                "role": "user",
                "content": [
                    {"type": "audio", "path": str(audio)},
                    {"type": "text", "text": prompt}
                ],
            }
        ]
        
        # Apply chat template
        print("Processing audio for understanding...")
        inputs = processor.apply_chat_template(conversation)
        inputs = inputs.to(self.device, dtype=torch.bfloat16)
        
        # Generate response
        print("Generating audio understanding response...")
        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=max_tokens)
        
        # Decode only the newly generated tokens
        decoded_outputs = processor.batch_decode(
            outputs[:, inputs.input_ids.shape[1]:], 
            skip_special_tokens=True
        )
        
        response = decoded_outputs[0].strip()
        print(f"Audio understanding completed: {len(response)} characters")
        
        return response
