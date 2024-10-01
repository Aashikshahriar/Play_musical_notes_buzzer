import machine
import time

# Define the frequencies for each note
note_frequencies = {
    'C4': 261,
    'C#4': 277,
    'D4': 294,
    'D#4': 311,
    'E4': 329,
    'F4': 349,
    'F#4': 370,
    'G4': 392,
    'G#4': 415,
    'A4': 440,
    'A#4': 466,
    'B4': 494,
    'C5': 523,
}

# Pin configuration
buzzer_pin = machine.Pin(15, machine.Pin.OUT)
pwm=machine.PWM(buzzer_pin)

# Function to play a note
def play(note, duration):
    if note in note_frequencies:
        frequency = note_frequencies[note]
        pwm.freq(frequency)  # Set frequency
        pwm.duty(512)  # Set duty cycle (50% on)
        time.sleep(duration)  # Play for the duration
        pwm.duty(0)  # Turn off buzzer
        time.sleep(0.3*duration)

# Load note names and durations from files
def load_notes(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f]

def load_durations(filename):
    with open(filename, 'r') as f:
        return [float(line.strip()) for line in f]

# Main function to play the melody
def play_melody():
    note_names = load_notes('note_names.txt')
    note_durations = load_durations('note_duration.txt')

    for note, duration in zip(note_names, note_durations):
        play(note, duration)

# Start playing the melody
play_melody()
