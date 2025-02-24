import re

def getSpeechBlocks(whispered, silence_time=0.8):
    text_blocks, (st, et, txt) = [], (0,0,"")
    for i, seg in enumerate(whispered['segments']):
        if seg['start'] - et > silence_time:
            if txt: text_blocks.append([[st, et], txt])
            (st, et, txt) = (seg['start'], seg['end'], seg['text'])
        else: 
            et, txt = seg['end'], txt + seg['text']

    if txt: text_blocks.append([[st, et], txt]) # For last text block

    return text_blocks

def cleanWord(word):
    return re.sub(r'[^\w\s\-_"\'\']', '', word)

def interpolateTimeFromDict(word_position, d):
    for key, value in d.items():
        if key[0] <= word_position <= key[1]:
            return value
    return None

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
    halfCaptionSize = maxCaptionSize / 2
    captions = []
    while words:
        caption = words[0]
        words = words[1:]
        while words and len(caption + ' ' + words[0]) <= maxCaptionSize:
            caption += ' ' + words[0]
            words = words[1:]
            if len(caption) >= halfCaptionSize and words:
                break
        captions.append(caption)
    return captions

#Single word captions
def getCaptionsWithTime(transcriptions):
    time_splits = []
    
    # Ensure we only work with transcriptions that have word-level timing
    segments = [seg for seg in transcriptions['segments'] if 'words' in seg]
    
    # Flatten all words from all segments
    all_words = []
    for segment in segments:
        all_words.extend(segment['words'])
    
    # Process each word individually
    for word in all_words:
        word_text = word['text']
        start_time = word['start']
        end_time = word['end']
        
        # Store each word with its exact timing
        time_splits.append(((start_time, end_time), word_text))
    
    return time_splits
