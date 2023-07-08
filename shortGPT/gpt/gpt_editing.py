from shortGPT.gpt import gpt_utils
import json
def getImageQueryPairs(captions,n=15 ,maxTime=2):
    
    prompt = gpt_utils.open_file('shortGPT/prompt_templates/generate_images.txt').replace('<<CAPTIONS TIMED>>', f"{captions}").replace("<<NUMBER>>", f"{n}")
    res = gpt_utils.gpt3Turbo_completion(prompt=prompt)
    imagesCouples = ('{'+res).replace('{','').replace('}','').replace('\n', '').split(',')
    pairs = []
    t0 = 0
    end_audio = captions[-1][0][1]
    for a in imagesCouples:
        try:
            query = a[a.find("'")+1:a.rfind("'")]
            time = float(a.split(":")[0].replace(' ',''))
            if (time > t0 and time< end_audio):
                pairs.append((time, query+" image"))
                t0 = time
        except:
            print('problem extracting image queries from ', a)
    for i in range(len(pairs)):
        if(i!= len(pairs)-1):
            end = pairs[i][0]+ maxTime if (pairs[i+1][0] - pairs[i][0]) > maxTime else pairs[i+1][0]
        else:
            end = pairs[i][0]+ maxTime if (end_audio - pairs[i][0]) > maxTime else end_audio
        pairs[i] = ((pairs[i][0], end), pairs[i][1])
    return pairs


def getVideoSearchQueriesTimed(captions_timed):
    end = captions_timed[-1][0][1]
    full_prompt = gpt_utils.load_yaml_file('shortGPT/prompt_templates/video_search_queries.yaml')
    system = full_prompt['system_prompt']
    chat = full_prompt['chat_prompt']
    input = chat.replace("<<TIMED_CAPTIONS>>", f"{captions_timed}")
    out = [[[0,0],""]]
    while out[-1][0][1] != end:
        try:
            out = json.loads(gpt_utils.gpt3Turbo_completion(prompt=input, system=system, temp=1).replace("'", '"'))
        except Exception as e:
            print(e)
            print("not the right format")
    return out