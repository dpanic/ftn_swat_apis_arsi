import os

path = "data/2015/Network/"
files = []
lines = []
linesSplit = []

os.chdir(path)
  
def readFiles():
    for file in os.listdir():
        if file.endswith(".csv"):
            files.append(file)

def readLines():
    for file in files:
        with open(file) as file:
            for line in file:
                lines.append(line)

## split by a coma for values
def splitLines():
    for line in lines:
        linesSplit.append(line.split(',', 20))

readFiles()
# Sort in chronological order
files.sort()

readLines()
splitLines()