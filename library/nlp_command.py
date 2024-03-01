
import sounddevice as sd
from scipy.io.wavfile import write


def record_and_save_audio(duration, save_path, sample_rate=16000):

    # Record audio from the microphone in mono (1 channel)

    audio_data = sd.rec(int(duration * sample_rate),

                        samplerate=sample_rate, channels=1, dtype='int16')

    sd.wait()

    # Save the recorded audio as a WAV file

    write(save_path, sample_rate, audio_data)


def check_sentence(sentence, words_to_check):
    if sentence is None or not isinstance(sentence, str):
        return -1  # Return -1 for invalid input

    for idx, word in enumerate(words_to_check, start=1):  # Start enumeration from 1
        if word in sentence.lower():
            return idx

    return -1  # Return -1 if none of the words are found

# List of words to check
# words_to_check = ["sprite", "water", "coffee", "orange"]

# Input sentence
# input_sentence = input("Enter a sentence: ")

# result = check_sentence(input_sentence.lower(), words_to_check)

# if result != -1:
#     print(f"The sentence contains '{words_to_check[result]}', and its index is {result}.")
# else:
#     print("The sentence does not contain any of the specified words.")
