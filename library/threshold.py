import webrtcvad
import numpy as np
import pyaudio
import wave
import os


def record_audio_with_threshold(save_location):
    # Set up the VAD
    vad = webrtcvad.Vad()
    vad.set_mode(3)  # Experiment with different aggressiveness levels

    # Set up audio recording parameters
    sample_rate = 16000
    chunk_duration = 30  # milliseconds
    chunk_size = int(sample_rate * chunk_duration / 1000)  # Convert to samples

    # Initialize PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk_size)

    # Initialize threshold
    threshold = 0.0001

    # Initialize recording state
    recording = False
    frames = []
    silence_frames = 0
    silence_threshold = 5  # Adjust as needed (in number of chunks)

    try:
        print("Listening for audio... (Press Ctrl+C to stop)")
        while True:
            # Read audio data from the microphone
            audio_chunk = stream.read(chunk_size)
            audio_chunk_np = np.frombuffer(audio_chunk, dtype=np.int16)

            # Perform VAD
            is_speech = vad.is_speech(audio_chunk_np.tobytes(), sample_rate)

            if is_speech:
                print("Speech detected!")
                silence_frames = 0  # Reset silence counter
                if not recording:
                    recording = True
                    print("Start recording...")

                frames.append(audio_chunk)

                # Calculate threshold based on the current chunk
                chunk_threshold = np.mean(np.abs(audio_chunk_np)) / 32768.0
                if chunk_threshold > threshold:
                    threshold = chunk_threshold
                    print(f"Updated threshold: {threshold:.6f}")

            elif recording:
                silence_frames += 1
                if silence_frames >= silence_threshold:
                    recording = False
                    print("Stop recording...")

                    # Save the recorded speech to a WAV file
                    with wave.open(save_location, "wb") as wf:
                        wf.setnchannels(1)
                        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
                        wf.setframerate(sample_rate)
                        wf.writeframes(b''.join(frames))

                    # Break the loop if recorded audio duration is >= 2 seconds
                    duration = len(frames) * chunk_duration / \
                        1000  # in seconds
                    if duration >= 2:
                        break

                    frames = []

    except KeyboardInterrupt:
        print("\nRecording stopped.")
        if recording:
            print("Stop recording...")
        stream.stop_stream()
        stream.close()
        p.terminate()

# Example usage:
# audio_save_location = "recorded_speech.wav"
# record_audio_with_threshold(audio_save_location)
