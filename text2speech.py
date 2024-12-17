import os
import azure.cognitiveservices.speech as speechsdk

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv("text2speech.env")

# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
speech_config = speechsdk.SpeechConfig(
    subscription=os.environ.get("SPEECH_KEY"), region=os.environ.get("SPEECH_REGION")
)

# List of voice names
speech_synthesis_voices = [
    "it-IT-ElsaNeural",
    "it-IT-IsabellaNeural",
    "it-IT-DiegoNeural",
    "it-IT-BenignoNeural",
    "it-IT-CalimeroNeural",
    "it-IT-CataldoNeural",
    "it-IT-FabiolaNeural",
    "it-IT-FiammaNeural",
]

text = "Capisco che potresti avere qualche difficoltà con la memoria o il pensiero, e va bene così. Siamo qui per supportarti e rendere le cose più facili per te."


def text_to_speech(text, voice_name):

    audio_config = speechsdk.audio.AudioOutputConfig(filename=f"{voice_name}.mp3")

    # The neural multilingual voice can speak different languages based on the input text.
    speech_config.speech_synthesis_voice_name = voice_name

    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )

    # Get text from the console and synthesize to the default speaker.
    # print("Enter some text that you want to speak >")
    # text = input()

    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if (
        speech_synthesis_result.reason
        == speechsdk.ResultReason.SynthesizingAudioCompleted
    ):
        print("Speech synthesized for text [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")


# Iterate over the list of voice names and synthesize speech for each
for voice_name in speech_synthesis_voices:
    text_to_speech(text, voice_name)
