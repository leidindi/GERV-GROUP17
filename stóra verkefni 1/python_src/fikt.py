value = 0
width = 8
height = 8
state = [["W"]*width if i < 2 else ["B"]*width if i > height -3 else ["-"]*width for i in range(height)]
for y,row in enumerate(state[2:height-2]):
    for x,column in enumerate(row):
        # if white is in midsection
        if column == "W":
            value += 1
for y,row in enumerate(state[height-2:]):
    for x,column in enumerate(row):
        # if white is in blacks space
        if column == "W":
            value += 2

print(value)