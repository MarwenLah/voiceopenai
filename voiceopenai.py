import re

import openai
import pyttsx3
import speech_recognition as sr


def say_and_print_sentences(text):
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()

    # Set the properties for the speech
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 0.8)  # Volume (0.0 to 1.0)

    # Split the text into sentences using regular expressions
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # Print each sentence on a new line
    print("OUTPUT : ")
    for sentence in sentences:
        print(sentence)

        # Convert the text to speech
        engine.say(sentence)

        # Play the speech
        engine.runAndWait()
    print('')


if __name__ == '__main__':
    # Set up your OpenAI API credentials
    openai.api_key = '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'
    # Create a recognizer object
    r = sr.Recognizer()
    # r.energy_threshold = 500
    r.phrase_threshold = 0.1
    r.pause_threshold = 1
    # Read input from the user
    last_text_cached = ''
    enabled = True
    while True:

        # Use the default microphone as the audio source
        with sr.Microphone() as source:
            print("Say something...")

            # Capture the audio
            audio = r.listen(source, timeout=5)

            # Recognize speech using Google Speech Recognition
            try:
                text = r.recognize_google(audio)
                lower_text = str(text).lower()
                if lower_text == "enable":
                    enabled = True
                    say_and_print_sentences("STATUS: ENABLED")
                    continue
                elif lower_text == "disable":
                    enabled = False
                    say_and_print_sentences("STATUS: DISABLED")
                    continue
                if not enabled:
                    print("say 'enable' to start using again")
                    continue

                if lower_text.startswith("tell me more"):
                    text = last_text_cached
                    print("INPUT REPEATED: " + text)
                else:
                    print("INPUT: " + text)
                if text == "":
                    continue

            except Exception:
                continue

        # Generate text using the completions API
        # try:
            response = openai.Completion.create(
                engine='text-davinci-003',
                prompt=text,
                max_tokens=1000
            )
        # except Exception:
        #     say_and_print_sentences("chat API issue. Say again")
        #     continue

        # Get the generated text from the API response
        generated_text = response.choices[0].text.strip()
        last_text_cached = text

        # Print the generated text
        say_and_print_sentences(generated_text)
