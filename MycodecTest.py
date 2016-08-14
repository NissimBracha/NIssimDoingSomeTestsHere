"""
This python script encodes all files that have the extension MTS in all
working directories.
Sources:
    http://ffmpeg.org/trac/ffmpeg/wiki/x264EncodingGuide
"""
import os, fnmatch, glob

#-------------------------------------------------------------------------------
# CONFIGURABLE SETTINGS
#-------------------------------------------------------------------------------

# controls the quality of the encode
CRF_VALUE = '21'

# h.264 profile
PROFILE = 'high'

# encoding speed:compression ratio
PRESET = 'slow'

# path to ffmpeg bin

# With Concat

FFMPEG_CONCAT = '/usr/local/bin/ffmpeg -i \"concat:'

# simple for convert

FFMPEG_CONVERT = '/usr/local/bin/ffmpeg -i '

# root dir - this is where the search starts

SEARCH_DIR = '/Users/nissimbracha'


#-------------------------------------------------------------------------------
# encoding script
#-------------------------------------------------------------------------------

#Function - get directories and file names with ext

def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
             if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename


locateMTS = set()



for filename in find_files(SEARCH_DIR , '*.MTS'):
    #get all folders with MTS files
    locateMTS.add(os.path.dirname(filename))


#for filename in find_files(SEARCH_DIR , '*.mts'):
    #get all folders with mts files
    #locateMTS.add(os.path.dirname(filename))


locateMTS2 = list(locateMTS)




for folder in locateMTS2:
    MtsNames = glob.glob1(folder, "*.MTS")
    #MtsNames.append(glob.glob1(folder, "*.mts"))
    MtsCounter = len(MtsNames)
    #print MtsCounter

    getFileName = folder.rsplit("/")[-1].replace('.', '-')

    # if there are more then 1 MTS files and concatenate is needed

    if MtsCounter > 1:
        MtsConcat = folder + "/" + ("|" + folder + "/").join(MtsNames)
        os.system(FFMPEG_CONCAT + MtsConcat + "\" -c copy " + folder + "/" + "concatfile.MTS")
        #print FFMPEG_CONCAT + MtsConcat + "\" -c copy " + folder + "/" + "concatfile.MTS"
        os.system(FFMPEG_CONVERT + folder + "/" + "concatfile.MTS" + " -c:v libx264 -preset " + PRESET + "  -crf " + CRF_VALUE + " -tune film " + folder + "/" + getFileName + ".mp4")
        #print FFMPEG_CONVERT + folder + "/" + "concatfile.MTS" + " -c:v libx264 -preset " + PRESET + " -crf " + CRF_VALUE + " -tune film " + folder + "/" +  getFileName + ".mp4"
        os.system("rm -f " + folder + "/*.MTS")

    # if no concat Needed

    elif MtsCounter == 1:
        os.system(FFMPEG_CONVERT + folder + "/" + MtsNames[0] + " -c:v libx264 -preset " + PRESET + " -crf " + CRF_VALUE + " -tune film " + folder + "/" + getFileName + ".mp4")
        #print FFMPEG_CONVERT + folder + "/" + MtsNames[0] + " -c:v libx264 -preset " + PRESET + " -crf " + CRF_VALUE + " -tune film " + folder + "/" + getFileName + ".mp4"
        os.system("rm -f " + folder + "/*.MTS")

    elif MtsCounter == 0:
        print "no file was found"
        continue

#---------------------  End  ------------------------------------------



