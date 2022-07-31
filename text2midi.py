from piano_database import notes as sheet
from midiutil import MIDIFile as MIDI
import os

ConvertToAudio = 0 # use FluidSynth to convert to audio?
PlayTheFile    = 1 # open the file after converting?
NumOfTracks    = 4 # number of midi channels and tracks

textfile  = "input.txt"
midifile  = "output.mid"
audiofile = "output.mp3"

with open(textfile,'r') as f: text = f.read()

time  = 0
notes = []
midi  = MIDI( NumOfTracks )

# for every line in TXT file
for num, line in enumerate(text.split('\n')):
    
    lline = line.lower()
    
    # find lines with tags and it to note list
    # it probably would've been easier to add note to file on a spot 
    # instead of making a list and then reading from it
    if any((i in lline) for i in ('bpm:', 'tempo:')): #BPM
        
        try:
            # 89.5 for Virtual Piano
            bpm = float(line.split(":")[-1])
            notes.append(('bpm', bpm))
        except ValueError:
            raise('BPM Must Be a Float')
    

    elif any((i in lline) for i in ('ins:', 'inst:', 'instrument:', 'i:')): # Instrument
        
        try:
            instrument = int(line.split(":")[-1])
            notes.append(('instrument', instrument))
        
        except ValueError:
            raise('Instrument Must Be an Integer')
    

    elif any((i in lline) for i in ('time:', 't:')): # Change Time of Event
        
        try:
            time = float(line.split(":")[-1])
            notes.append(('time', time))
        
        except ValueError:
            raise('Time Must Be a Float')
    
    
    elif any((i in lline) for i in ('timeadd:', 'add:', 'a:')): # Add to Time of Event
        
        try:
            time = float(line.split(":")[-1])
            notes.append(('add', time))
        
        except ValueError:
            raise('TimeAdd Must Be a Float')
    
    elif any((i in lline) for i in ('channel:', 'c:')): # Channel
        
        try:
            channel = int(line.split(":")[-1])
            notes.append(('channel', channel))
        
        except ValueError:
            raise('Channel Must Be an Integer')
        
    elif any((i in lline) for i in ('track:', 'tr:')): # Track
        
        try:
            channel = int(line.split(":")[-1])
            notes.append(('track', channel))
        
        except ValueError:
            raise('Track Must Be an Integer')
        
    elif any((i in lline) for i in ('volume:', 'v:')): # Note Volume
            try:
                name = int(line.split(":")[-1])
                notes.append(('volume', name))
            except ValueError:
                raise('Volume Must Be an Integer between 0 and 127')
    
    elif any((i in lline) for i in ('name:', 'n:')): # Track Name
            name = str(line.split(":")[-1])
            notes.append(('name', name))
    
    # If none of the tags were found then play letters as notes
    else: # Note
        
        for note in line:
            
            # find pitch of note in the sheet
            try:    pitch, _ = sheet[note]
            except: pitch = None
            
            # if note is in the sheet then add it in list for play and reset offset 
            if (note in sheet.keys()):
                
                notes.append((pitch, str(time)))
                time = 1/4
                
            # otherwise check if it is one of specal symbols for offset
            # I should probably move this part to database.py
            else:
                
                if   note ==  '/': time += 4/4   # Measure
                
                elif note ==  '|': time += 3/4   # Full Note ?
                
                elif note == '\\': time += 2/4   # Half Note ?
                
                elif note ==  '-': time += -1/24
                
                elif note ==  '+': time += -1/12 # Eighth Note ?
                    
                elif note ==  ' ': time += 1/4   # Quarter Note ?
                
                elif note ==  '=': time += -1/6

                elif note ==  '~': time += -1/4  # Chord 1~3~5
                
                elif note == '\n': time += 0     # does nothing, can be changed
                
                else: time += 0

# initialize default values
channel = 0
track   = 0
volume  = 100

# for every item in the list
for note, data in notes:
    
    # if data carried with item is string then use it as note offset
    # this is really spagetti and inconvenient, another reason to NOT make it a list
    if isinstance(data, str) and note != 'name':
        data = float(data)
        time += data
    
    if   note == 'bpm': midi.addTempo(track, time, data)  # BPM
    
    elif note == 'instrument': midi.addProgramChange(track, channel, time, data - 1)   # Instrument
    
    elif note == 'name': midi.addTrackName(track, time, data) # Track Name
    
    elif note == 'channel': channel = int(data) # Channel Number

    elif note == 'track': track = data # Track Number

    elif note == 'time': time = data # Time of Event
    
    elif note == 'add': time += data # Add to Time of Event
    
    elif note == 'volume': volume = int(data) # Volume
   
                                   # note duration  V
    else: midi.addNote(track, channel, note, time, 0.5, volume) # Note
                                   # gonna add a tag for it next update 

# write midi to a file
with open(midifile, "wb") as f: midi.writeFile(f)


if ConvertToAudio:
    from midi2audio import FluidSynth
    FluidSynth().midi_to_audio(midifile, audiofile) # convert midi to audio
    if PlayTheFile: os.system(audiofile) # play audio if needed
    
else:
    if PlayTheFile: os.system(midifile) # play midi if needed
