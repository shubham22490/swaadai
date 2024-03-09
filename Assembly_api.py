import assemblyai as aai
import speech_recognition as sr

aai.settings.api_key = "ad9eac5fd74d4397a76c95a6d1ed4810"
test_url = "https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"


def get_transcript(audio_url: str) -> str:
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_url)
    return transcript.text

