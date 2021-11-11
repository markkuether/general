import os
import pathlib
import csv
'''
Finds the 100 largest files of types specified 
in the extensions list. Writes sorted results to a
csv file.

Designed for Windows.
'''

# Set initial conditions including file types to search
biggestFiles = []
streamFmts = ["mp4", "wmv", "mp3", "wav"]
imageFmts = ["jpg", "png", "bmp"]
docFmts = ["docx", "doc", "xlsx", "xls", "pptx", "ppt", "pdf"]
extensions = streamFmts + imageFmts + docFmts

# Set directory paths.
rootPath = pathlib.Path("<root path>")
outPath = rootPath / "<output path>"
fullOut = outPath / "<output file>.csv"


def findFiles(origin_folder: pathlib.Path, biggestFiles: list, extensions: list):
    '''
    Recursively searches folders for files matching extensions 
    listed in the extensions list. Uses FindLargest to build a list of
    the largest files.

    Returns a 2-tuple list (full file path, size) of the largest files.
    '''

    try:
        with os.scandir(origin_folder) as file_list:
            for item in file_list:
                if item.is_dir():
                    next_origin = origin_folder / item.name
                    biggestFiles = findFiles(
                        next_origin, biggestFiles, extensions)
                else:  # This is a file
                    try:
                        fileDetails = item.stat()
                        fileSize = fileDetails.st_size
                        filePath = item.path
                        fileName = item.name
                        dotPos = fileName.rfind(".")
                        if dotPos > 0:
                            fileExt = str(fileName[dotPos+1:]).lower()
                            if fileExt in extensions:
                                fileSpecs = (filePath, fileSize)
                                biggestFiles = FindLargest(
                                    fileSpecs, biggestFiles)
                    except IOError as e:
                        print(
                            f"A problem occurred getting file detials for {item}")
                        print(e)
    except:
        # This typically occurs due to access restrictions.
        # Since this is recursive, this just returns
        # to the calling routine and continues.
        # Printing X provides a type of progress indicator.
        print("X", end="")

    return biggestFiles


def FindLargest(fileDetails: tuple, biggestFiles: list, size: int = 100):
    '''
    Creates a list of up to (size) of the largest files.
    Sorts the list by file size descending.
    Returns a list of 2-tuples containing (file name,size).
    '''

    fileSize = fileDetails[1]
    if len(biggestFiles) < size:
        biggestFiles.append(fileDetails)
        biggestFiles = sorted(biggestFiles, key=lambda x: x[1], reverse=True)
    else:
        if biggestFiles[-1][1] < fileSize:
            biggestFiles.append(fileDetails)
            biggestFiles = sorted(
                biggestFiles, key=lambda x: x[1], reverse=True)
            biggestFiles = biggestFiles[0:size+1]

    return biggestFiles


def saveResults(biggestFiles: list, fullOut: pathlib.Path):
    '''
    Detects duplicates based on size and marks duplicates.
    Saves sorted list of files in CSV file with columns:
    ("Dup","Size","Full_Path")
    '''

    lastSize = 0
    try:
        with open(fullOut, 'w', newline='') as csvfile:
            sizeWriter = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
            sizeWriter.writerow(["Dup", "Size", "Full_Path"])
            for item in biggestFiles:
                thisSize = int(item[1])
                if thisSize == lastSize:
                    dupeStr = "*"
                else:
                    dupeStr = ""
                sizeWriter.writerow([dupeStr, item[1], item[0]])
                lastSize = thisSize
            print(f"Results written to {fullOut}")
    except IOError as ioe:
        print(f"Error writing file:{ioe}")

    print()


### MAIN CODE ####
biggestFiles = findFiles(rootPath, biggestFiles, extensions)
print()
saveResults(biggestFiles, fullOut)

### Output to console ###
# for item in biggestFiles:
#    print(f"{item[1]},{item[0]}")
