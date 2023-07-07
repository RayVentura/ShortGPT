import re

def interpolateTimeFromDict(word_position, d):
    for key, value in d.items():
        if key[0] <= word_position <= key[1]:
            return value
    return None

def cleanWord(word):
    return re.sub(r'[^\w\s]', '', word)

def getTimestampMapping(whisper_analysis):
    index = 0
    locationToTimestamp = {}
    for segment in whisper_analysis['segments']:
        for word in segment['words']:
            newIndex = index + len(word['text'])+1
            locationToTimestamp[(index, newIndex)] = word['end']
            index = newIndex
    return locationToTimestamp

def splitWordsBySize(words, maxCaptionSize):
    captions = []
    i = 0
    while i < len(words):
        caption = words[i]
        while i + 1 < len(words) and len(caption + ' ' + words[i + 1]) <= maxCaptionSize:
            i += 1
            caption += ' ' + words[i]
        captions.append(caption)
        i += 1
    return captions
def getCaptionsWithTime(whisper_analysis, maxCaptionSize=15):
    wordLocationToTime = getTimestampMapping(whisper_analysis)
    position = 0
    start_time = 0
    CaptionsPairs = []
    words = whisper_analysis['text'].split()
    split_captions = splitWordsBySize(words, maxCaptionSize)
    for caption in split_captions:
        position += len(caption) + 1
        end_time = interpolateTimeFromDict(position, wordLocationToTime)
        if(end_time and caption):
            CaptionsPairs.append(((start_time, end_time), cleanWord(caption)))
            start_time = end_time

    return CaptionsPairs
