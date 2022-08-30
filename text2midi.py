from piano_database import notes as sheet
from piano_database import delays
from midiutil import MIDIFile as MIDI
import os

def getDur(text, lineNum, noteNum):

    time = 0

    lines = text.splitlines()[lineNum][noteNum+1:]

    for line in text.splitlines()[lineNum+1:]:
        lines += line

    for note in lines:
        if (note in sheet.keys()):
            break
        else:
            time += delays.setdefault(note, 0)

    return time


def main(infile, outfile):
    midi  = MIDI(8)

    with open(infile,'r') as f: text = f.read()

    offTime = 0
    time    = 0

    channel  = 0
    track    = 0
    duration = 0
    volume   = 100

    fullDur = True

    # for every line in TXT file
    for numLine, line in enumerate(text.split('\n')):
        
        line = line.lower()
        
        if ':' in line: data = line.split(":")[-1]

        # BPM
        if any((i in line) for i in ('bpm:', 'tempo:')): 
            midi.addTempo(track, time, float(data))  # BPM

        # Instrument Change
        elif any((i in line) for i in ('ins:', 'instr:', 'instrument', 'i:')): # Instrument
            midi.addProgramChange(track, channel, time, int(data) - 1)   # Instrument
        
        # Time Set
        elif any((i in line) for i in ('time:', 't:')): 
            time = float(data)
        
        # Time offset
        elif any((i in line) for i in ('add:', 'a:')): 
            time += float(data)
        
        # Channel
        elif any((i in line) for i in ('channel:', 'c:')): 
            channel = int(data)
        
        # Track
        elif any((i in line) for i in ('track:', 'tr:')): 
            track = int(data)
        
        # Note Volume
        elif any((i in line) for i in ('vol:', 'v:')): 
                volume = int(data)
        
        # Note Duration
        elif any((i in line) for i in ('duration:', 'dur:', 'd:')):
            duration = float(data)
            fullDur = False
            if duration <= 0: fullDur = True


        # Track Name
        elif any((i in line) for i in ('name:', 'n:')):
                 midi.addTrackName(track, time, str(data))
        
        # If none of the tags were found then play letters as notes
        else: # Note
            
            for numNote, note in enumerate(line):
                
                # find pitch of note in the sheet
                pitch = False
                if (note in sheet.keys()):
                    pitch, _ = sheet[note]

                # if note is in the sheet then add it
                if pitch:

                    if not fullDur: 
                        midi.addNote(track, channel, pitch, time, duration, volume)
                    
                    else:          
                        midi.addNote(track, channel, pitch, time, getDur(text, numLine, numNote), volume)


                # otherwise check if it is one of specal symbols for offset
                else:
                    time += delays.setdefault(note, 0)


    # write midi to a file
    with open(outfile, "wb") as f: midi.writeFile(f)


if __name__ == '__main__':
    main('input.txt', 'output.mid')