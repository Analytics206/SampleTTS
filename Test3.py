import os
import random
import string
import time
import soundfile as sf
import speech_recognition as sr
import simpleaudio as sa
from kokoro import KPipeline
from IPython.display import display, Audio

# Disable TensorFlow OneDNN optimizations
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Initialize KPipeline
pipeline = KPipeline(lang_code='a')

def get_text_from_mic():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... Please speak clearly.")
        try:
            recognizer.adjust_for_ambient_noise(source, duration=1)
        except Exception as e:
            print(f"Error adjusting for ambient noise: {e}")
            return None
        audio = recognizer.listen(source)
    print("Processing...")
    try:
        text = recognizer.recognize_google(audio)
        print(f"Recognized: {text}")
        return text
    except sr.UnknownValueError as e:
        print("Could not understand audio:", e)
        return None
    except sr.RequestError as e:
        print("Could not request results:", e)
        return None

while True:
    print("\nEnter text (leave empty to use microphone, say 'exit' to quit): ", end="")
    user_input = input().strip()

    if not user_input:
        user_input = get_text_from_mic()
        if not user_input:
            print("No valid input received. Try again.")
            continue

    if user_input.lower() == "exit":
        print("Exiting program...")
        break

    # Process text-to-speech
    try:
        generator = pipeline(
            user_input, voice='af_heart', speed=.9, split_pattern=r'\n+'
        )
    except Exception as e:
        print(f"Error processing text-to-speech: {e}")
        continue

    for i, (gs, ps, audio) in enumerate(generator):
        print(i)  # Index
        print(gs)  # Graphemes/text
        print(ps)  # Phonemes
        display(Audio(data=audio, rate=24000, autoplay=i == 0))
        random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        filename = f'{i}_{random_str}.wav'
        sf.write(filename, audio, 24000)  # Save each audio file

        # Playback through speakers
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        play_obj.wait_done()

    time.sleep(1)  # Small delay to prevent instant looping