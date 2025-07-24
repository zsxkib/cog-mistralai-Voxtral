# Voxtral

[![Replicate](https://replicate.com/zsxkib/voxtral/badge)](https://replicate.com/zsxkib/voxtral)

You know how most speech AI either transcribes what you say or completely misses the point? Voxtral actually gets it.

Ask it to transcribe a 30-minute meeting and it catches every word. Play it audio in French and ask a question in English - it handles both. Give it a messy conversation with multiple people talking over each other, and it can tell you what's actually happening.

This is Mistral's Voxtral - their language model that learned how to hear.

## Try it right now

Got a GPU and Docker? Three commands and you're processing audio:

```bash
git clone https://github.com/zsxkib/cog-mistralai-voxtral.git
cd cog-mistralai-voxtral
cog predict -i audio=@examples/french_mathis_voice_intro.mp3 -i mode="understanding" -i prompt="What is this person saying?"
```

That's it. No setup, no hunting for model weights. It downloads everything and starts working.

## What makes this different

Voxtral isn't just another speech model. It's Mistral's language model that can hear:

- **Actually understands context**: Can handle up to 30 minutes of audio for transcription, 40 minutes for understanding
- **Speaks 8 languages**: Automatic language detection across English, Spanish, French, Portuguese, Hindi, German, Dutch, and Italian  
- **Two modes**: Perfect transcription AND smart audio analysis
- **Function calling from voice**: Trigger backend functions and API calls directly from what people say
- **Built on Mistral Small 3**: All the text smarts, plus audio superpowers

Pick Mini (3B) for speed or Small (24B) for accuracy.

## Some things you can try

```bash
# Try the included French example
cog predict -i audio=@examples/french_mathis_voice_intro.mp3 -i mode="transcription" -i language="French"

# Ask questions about the audio content  
cog predict -i audio=@examples/french_mathis_voice_intro.mp3 -i mode="understanding" -i prompt="Summarize what this person is talking about"

# Let it auto-detect the language
cog predict -i audio=@examples/french_mathis_voice_intro.mp3 -i mode="transcription" -i language="Auto-detect"

# Use your own audio file
cog predict -i audio=@your_meeting.wav -i mode="understanding" -i prompt="Who are the speakers and what are they discussing?"

# Use the bigger model for complex audio
cog predict -i audio=@complex_discussion.wav -i mode="understanding" -i model_size="small" -i prompt="Extract key insights and action items"

# Get longer responses
cog predict -i audio=@presentation.wav -i mode="understanding" -i max_tokens=800 -i prompt="Give me a detailed summary"
```

## All the parameters

- `audio` - Your audio file (up to 30 minutes for transcription, 40 minutes for understanding)
- `mode` - `"transcription"` (speech-to-text) or `"understanding"` (analyze and answer questions)
- `prompt` - Question or instruction for understanding mode (ignored in transcription)  
- `language` - `"Auto-detect"` or pick one (English, French, German, Spanish, Italian, Portuguese, Dutch, Russian, Chinese, Japanese, Arabic)
- `model_size` - `"mini"` (3B, faster) or `"small"` (24B, more accurate)
- `max_tokens` - Response length (50-1000 tokens)

## What you need

- NVIDIA GPU with ~8GB VRAM for Mini model, ~55GB for Small model
- Docker
- Cog (`pip install cog`)

## Use cases

Content creators transcribing and analyzing podcasts, interviews, and videos. Businesses processing meeting recordings and customer calls. Researchers working with multilingual audio data. Developers building voice-controlled applications.

Perfect when you need both accurate transcription AND smart audio understanding.

## How it works

Mistral took their Small 3 language model and taught it to understand audio. It handles speech transcription, translation, and audio understanding in one model.

The understanding mode combines speech recognition with Mistral's reasoning. It doesn't just hear what's said - it understands meaning, context, and can answer complex questions about audio content.

## Performance  

Voxtral beats other models on FLEURS, Mozilla Common Voice, and Multilingual LibriSpeech benchmarks. But benchmarks are just numbers - try it on your audio and see how it handles real-world messiness.

## Two model sizes

**Mini (3B)**: Fast, lower GPU requirements, handles most use cases  
**Small (24B)**: Maximum accuracy for complex audio, professional transcription quality

## What's included

- `predict.py` - Main Cog interface with transcription and understanding modes
- `cog.yaml` - Cog configuration  
- `examples/french_mathis_voice_intro.mp3` - Sample French audio to test with
- Model weights download automatically from Hugging Face

## Languages supported

Auto-detection plus dedicated support for:
- English
- Spanish  
- French
- Portuguese
- Hindi
- German
- Dutch
- Italian

## License

Code is open source. Model weights follow Mistral's Apache 2.0 license. Built on Mistral's Voxtral technology.

## Citation

```bibtex
@article{voxtral2024,
  title={Voxtral: State-of-the-art Speech Understanding},
  author={Mistral AI},
  year={2024},
  url={https://mistral.ai/news/voxtral}
}
```

---

Built by Mistral AI. Packaged for Replicate by [@zsxkib](https://github.com/zsxkib) ([@zsakib_](https://twitter.com/zsakib_)).

[![Replicate](https://replicate.com/zsxkib/voxtral/badge)](https://replicate.com/zsxkib/voxtral)