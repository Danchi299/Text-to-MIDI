Simple program that converts TXT files to MIDI files
  music out of pure text!

This program requires Midiutil library
  pip install midiutil

If you want to automatically convert MIDI to MP3 you need to install and setup FluidSynth
  pip install pyFluidSynth

Use letter to play notes 
  qQwWeErtTyYui

Change delay between them using symbols and spaces -+=\|/
  I/O/T\O/P/O-I-i-Y-i/T/W
  
Add tags to change instruments tempo and tracks
  tempo:100
  intrument: 1
  qwertyu
  add:0.5
  instrument: 5
  qwertyu
  
Play 2 instruments at once
  bpm: 120
  
  channel: 1
  time: 0
  ins: 1
  qwertyu
  
  channel: 2
  time: 0.2
  volume: 50
  ins: 5
  qwertyu
