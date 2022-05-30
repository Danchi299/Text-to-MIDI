from piano_database import notes as sheet
from midiutil import MIDIFile as MIDI
import os

# 89.5 for Virtual Piano

conver2audio = 1
play7file    = 0

textfile  = "input.txt"
midifile  = "output.mid"
audiofile = "output.mp3"

with open(textfile,'r') as f: text = f.read()

notes = []
times = []

time = 0

midi = MIDI(1)

for num, line in enumerate(text.split('\n')):
    
    lline = line.lower()
    if any((i in lline) for i in ('bpm:', 'tempo:')):
        
        try:
            bpm = float(line.split(":")[-1])
            notes.append(('bpm', bpm))
        except ValueError:
            raise('BPM Must Be a Float')
    

    elif any((i in lline) for i in ('ins:', 'inst:', 'instrument:', 'i:')):
        
        try:
            instrument = int(line.split(":")[-1])
            notes.append(('instrument', instrument))
        
        except ValueError:
            raise('Instrument Must Be an Integer')
    

    elif any((i in lline) for i in ('time:', 't:')):
        
        try:
            time = float(line.split(":")[-1])
            notes.append(('time', time))
        
        except ValueError:
            raise('Time Must Be a Float')
        
    elif any((i in lline) for i in ('channel:', 'c:')):
        
        try:
            channel = int(line.split(":")[-1])
            notes.append(('channel', channel))
        
        except ValueError:
            raise('Channel Must Be an Integer')
        
    elif any((i in lline) for i in ('track:', 'tr:')):
        
        try:
            channel = int(line.split(":")[-1])
            notes.append(('track', channel))
        
        except ValueError:
            raise('Track Must Be an Integer')
        
    elif any((i in lline) for i in ('name:', 'n:')):
            name = str(line.split(":")[-1])
            notes.append(('name', name))
    
    
    else:
        
        for note in line:
            
            try:    pitch, _ = sheet[note]
            except: pitch = None
            
            if (note in sheet.keys()):
                
                notes.append((pitch, str(time)))
                time = 1/4
                
            else:
                
                if   note ==  '/': time += 4/4 # Measure
                
                elif note ==  '|': time += 3/4
                
                elif note == '\\': time += 2/4
                
                elif note ==  '-': time += -1/24
                
                elif note ==  '+': time += -1/12
                
                elif note ==  '=': time += -1/6

                elif note ==  '~': time += -1/4
                
                elif note == '\n': time += 0
                
                elif note ==  ' ': time += 1/4
                
                else: time += 0

channel = 0
track   = 0
for note, data in notes:
    
    if isinstance(data, str) and note != 'name':
        data = float(data)
        time += data
    
    if note == 'bpm': midi.addTempo(track, time, data)  # BPM
    
    elif note == 'instrument': midi.addProgramChange(track, channel, time, data - 1)   # Instrument
    
    elif note == 'name': midi.addTrackName(track, time, data) # Track Name
    
    elif note == 'channel': channel = int(data) # Channel Number

    elif note == 'track': track = data # Track Number

    elif note == 'time': time = data # Time of Event
    
    else: midi.addNote(track, channel, note, time, 0.5, 100) # Note
    

with open(midifile, "wb") as f: midi.writeFile(f)

if conver2audio:
    from midi2audio import FluidSynth
    FluidSynth().midi_to_audio(midifile, audiofile)
    if play7file: os.system(audiofile)
    
else:
    if play7file: os.system(midifile)