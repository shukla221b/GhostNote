import sounddevice as sd
import soundfile as sf
from pynput import keyboard
import numpy as np
import threading
import os
from dotenv import load_dotenv
import openai
import time
from PIL import Image, ImageDraw
import pystray
import pyperclip

# --- Configuration ---
load_dotenv()
HOTKEY = {keyboard.Key.alt_l, keyboard.KeyCode.from_char('\\')}
SAMPLE_RATE = 44100
CHANNELS = 1
OUTPUT_FILENAME = "output.wav"

# --- State ---
current_keys = set()
is_recording = False
recording_thread = None
audio_frames = []
tray_icon = None
keyboard_listener = None

# --- Keyboard Controller ---
keyboard_controller = keyboard.Controller()

# --- Visual Feedback (System Tray Icon) ---
def create_image(color1, color2):
    image = Image.new('RGB', (64, 64), color1)
    dc = ImageDraw.Draw(image)
    dc.ellipse([(4, 4), (60, 60)], fill=color2)
    return image

ICON_IDLE = create_image('black', 'grey')
ICON_RECORDING = create_image('black', 'red')

def update_icon(recording: bool):
    if tray_icon:
        tray_icon.icon = ICON_RECORDING if recording else ICON_IDLE
        tray_icon.title = "GhostNote (Recording...)" if recording else "GhostNote (Idle)"
        tray_icon.update_menu()

# --- OpenAI Client ---
try:
    client = openai.OpenAI()
    print("OpenAI client initialized successfully.")
except openai.OpenAIError as e:
    print(f"Error initializing OpenAI client: {e}. Please check your API key.")
    client = None

def type_text(text):
    """Simulates typing out the given text."""
    print(f"Typing out: {text}")
    try:
        keyboard_controller.type(text.strip())
    except Exception as e:
        print(f"An error occurred while typing: {e}")

def transcribe_audio(file_path):
    """Transcribes the audio file using OpenAI's Whisper API."""
    if not client:
        print("OpenAI client is not available. Cannot transcribe.")
        return
    if not os.path.exists(file_path):
        print(f"Audio file not found: {file_path}")
        return

    print("Transcribing audio...")
    try:
        with open(file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        print(">" * 40)
        print(f"Transcription: {transcription.text}")
        print("<" * 40)
        type_text(transcription.text)
    except Exception as e:
        print(f"An error occurred during transcription: {e}")

def start_recording():
    global is_recording, audio_frames, recording_thread
    if is_recording:
        return
    is_recording = True
    audio_frames = []
    update_icon(recording=True)
    print("Recording started...")

    def record_audio():
        try:
            with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='float32') as stream:
                while is_recording:
                    frames, overflowed = stream.read(1024)
                    if overflowed:
                        print("Warning: Audio overflowed")
                    audio_frames.append(frames)
        except Exception as e:
            print(f"Audio input error: {e}")

    recording_thread = threading.Thread(target=record_audio)
    recording_thread.daemon = True
    recording_thread.start()

def stop_recording():
    global is_recording, recording_thread
    if not is_recording:
        return
    is_recording = False
    update_icon(recording=False)
    print("Recording stopped. Saving file...")

    if recording_thread:
        recording_thread.join()
        recording_thread = None

    if audio_frames:
        recording = np.concatenate(audio_frames, axis=0)
        sf.write(OUTPUT_FILENAME, recording, SAMPLE_RATE)
        print(f"File saved as {OUTPUT_FILENAME}")
        threading.Thread(target=transcribe_audio, args=(OUTPUT_FILENAME,), daemon=True).start()
    else:
        print("No audio recorded.")

def on_press(key):
    if key in HOTKEY:
        current_keys.add(key)
        if all(k in current_keys for k in HOTKEY) and not is_recording:
            start_recording()

def on_release(key):
    if all(k in current_keys for k in HOTKEY):
        if is_recording:
            stop_recording()
    
    if key in current_keys:
        try:
            current_keys.remove(key)
        except KeyError:
            pass

def quit_app(icon, item):
    print("Exiting...")
    if keyboard_listener:
        keyboard_listener.stop()
    icon.stop()

def setup_keyboard_listener():
    global keyboard_listener
    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    keyboard_listener.start()

def main():
    global tray_icon
    menu = (pystray.MenuItem('Quit', quit_app),)
    tray_icon = pystray.Icon("ghostnote", ICON_IDLE, "GhostNote (Idle)", menu)

    listener_thread = threading.Thread(target=setup_keyboard_listener)
    listener_thread.daemon = True
    listener_thread.start()
    
    print("GhostNote is running in the system tray.")
    tray_icon.run()

if __name__ == "__main__":
    main()