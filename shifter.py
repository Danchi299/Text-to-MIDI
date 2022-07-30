from piano_database import black_notes as black
from piano_database import white_notes as white

#black = "!@$%^*(QWETYIOPSDGHJLZCVB"
#white = "1234567890qwertyuiopasdfghjklzxcvbn"

num = int(input("Input Shift: "))

notes = open("input.txt",'r').read()

if notes[0] == '\n': notes = notes [1:]

if 0 < num:
    start = num
    end = 0
    step = -1
else:
    start = num
    end = 0
    step =  1

e = 0
for shift in range(start, end, step):
    output = ''
    try:
        for line in notes.splitlines():
        
            if ":" in line: continue
            
            else:
                for i in line:
                    
                    if black.find(i) != -1:
                        output += (black[black.find(i)+(5*shift)])
                    elif white.find(i) != -1:
                        output += (white[white.find(i)+(7*shift)])
                    else:
                        output += i
            
            output += '\n'
            
    except Exception as e:
        print("Error: Index Out of Range")
        e = 1
        break

print(f'Output with Shift {shift}: \n{output}')

input("Press Enter to Continue")