#installing the libraries
import librosa
import numpy as np

#load the audio file in WAV format
y,sr=librosa.load('iraaday1.mp3',sr=None)
print('Sampling rates: ',sr)
#Detect start of the notes
onset_frames=librosa.onset.onset_detect(y=y,sr=sr)
onset_times=librosa.frames_to_time(onset_frames,sr=sr)

#detect pitches using HPSS(Harmonic-Percussive Source Seperation)
harmonic,percussive=librosa.effects.hpss(y)
pitches,magnitudes=librosa.core.piptrack(y=harmonic,sr=sr)

#function to get the most prominent peaks
def get_pitch(pithces,magnitudes):
    pitch_list=[]
    for i in range(pitches.shape[1]):
        index=magnitudes[:,i].argmax()
        pitch=pitches[index,i]
        if pitch>0:
            pitch_list.append(pitch)
    return pitch_list
melody_pitches=get_pitch(pitches,magnitudes)
#extract the pitches at the onset times
notes=[]
durations=[]
for i in range(len(onset_frames)):
    pitch=melody_pitches[onset_frames[i]]  if onset_frames[i]<len(melody_pitches) else None
    if pitch:
        note=librosa.hz_to_midi(pitch)
        notes.append(note)
    #calculate note duration 
    if i<len(onset_times)-1:
        duration=onset_times[i+1]-onset_times[i]
    else:
        duration=0
    durations.append(duration)
def midi_to_note_name(midi_num):
    notes=['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave=(midi_num//12)-1
    note=notes[midi_num%12]
    return f'{note}{octave}'

note_names=[midi_to_note_name(int(n)) for n in notes]

with open('note_duration.txt','w') as duration_file:
    for duration in durations:
        duration_file.write(f'{duration:.2f}\n')
with open('note_names.txt','w') as note_file:
    for name in note_names:
        note_file.write(f'{name}\n')

print('note names and duration are saved to respective files')