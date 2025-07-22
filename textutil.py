from google.cloud import texttospeech

# Load your service account key
import os

if os.getenv("GITHUB_ACTIONS") != "true":
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "security/advance-symbol-407401-6cda3249d713.json"  # Change this

def text_to_mp3(message, output):

    # Create client
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=message)

    # Voice config (Korean)
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR",
        name="ko-KR-Wavenet-A",  # or B, C, D
    )

    # Audio config
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Request synthesis
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Save the result as MP3
    with open(output, "wb") as out:
        out.write(response.audio_content)

    print("MP3 saved successfully!")
