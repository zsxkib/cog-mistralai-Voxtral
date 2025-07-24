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

Most speech models do one thing. Voxtral does two things really well.

First, it transcribes audio. You can throw 30 minutes of audio at it and it'll write down what everyone said. It automatically figures out what language people are speaking - works with English, Spanish, French, Portuguese, Hindi, German, Dutch, and Italian.

Second, it understands what's happening in audio. Ask it questions about a podcast and it can tell you what the host was discussing. Play it a meeting recording and it can summarize the key points. This part can handle up to 40 minutes of audio.

You can also use it to trigger functions in your code just by talking to it - no need to build separate speech recognition.

There are two sizes: the small one (3 billion parameters) runs faster, the big one (24 billion parameters) is more accurate for tricky audio.

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
- `model_size` - `"mini"` (3 billion parameters, faster) or `"small"` (24 billion parameters, more accurate)
- `max_tokens` - Response length (50-1000 tokens)

## What you need

- NVIDIA GPU with around 8GB of memory for the mini model, around 55GB for the small model
- Docker
- Cog (see https://cog.run)

## Use cases

Content creators transcribing and analyzing podcasts, interviews, and videos. Businesses processing meeting recordings and customer calls. Researchers working with multilingual audio data. Developers building voice-controlled applications.

Good when you need both accurate transcription AND smart audio understanding.

## How it works

Mistral took their Small 3 language model and taught it to understand audio. It handles speech transcription, translation, and audio understanding in one model.

The understanding mode combines speech recognition with Mistral's reasoning. It doesn't just hear what's said - it understands meaning, context, and can answer complex questions about audio content.

## Performance  

Voxtral beats other models on FLEURS, Mozilla Common Voice, and Multilingual LibriSpeech benchmarks. But benchmarks are just numbers - try it on your audio and see how it handles real-world messiness.

## Two model sizes

**Mini (3 billion parameters)**: Runs faster, uses less GPU memory, handles most use cases  
**Small (24 billion parameters)**: More accurate for complex audio, better for challenging recordings

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