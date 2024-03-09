import assemblyai as aai
import speech_recognition as sr
import pyaudio
import wave

def record_audio(output_file, duration=7, sample_rate=44100, chunk_size=1024, audio_format=pyaudio.paInt16, channels=2):
    audio = pyaudio.PyAudio()

    stream = audio.open(format=audio_format,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk_size)

    print("Recording...")

    frames = []
    for i in range(0, int(sample_rate / chunk_size * duration)):
        data = stream.read(chunk_size)
        frames.append(data)

    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio to a file
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(audio_format))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

output_file = "recorded_audio.wav"
record_audio(output_file)
print(f"Audio recorded and saved as '{output_file}'")

aai.settings.api_key = "ad9eac5fd74d4397a76c95a6d1ed4810"
audio_url = "recorded_audio.wav"

transcriber = aai.Transcriber()
transcript = transcriber.transcribe(audio_url)
print(transcript.text)

