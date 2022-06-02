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

for shift in range(start, end, step):
    output = ''
    try:
        for i in notes:
            if black.find(i) != -1:
                output += (black[black.find(i)+(5*shift)])
            elif white.find(i) != -1:
                output += (white[white.find(i)+(7*shift)])
            else:
                output += i
        break
    except Exception as e:
        pass

print(f'Output with Shift {shift}: \n{output}')

input()
