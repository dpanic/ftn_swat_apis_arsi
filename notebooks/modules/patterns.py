import os

  
def bootstrap(file_loc):
    files = []


    total_files = 0
    total_loaded = 0
    total_skipped = 0

    for file in os.listdir(file_loc):
        total_files += 1
        if file.endswith(".csv"):
            files.append(file)
            total_loaded += 1
        else:
            total_skipped += 1
    
    files.sort()

    stats = [
        [ "Total files", "Skipped", "Loaded" ],
        [ total_files, total_skipped, total_loaded ]
    ]

    return [ files, stats ]


def process(file):
    """
        process file
    """
    with open(file) as file:
        for line in file:
            print(line)