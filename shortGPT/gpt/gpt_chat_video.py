from shortGPT.gpt import gpt_utils
import json
def generateScript(script_description, language):
    out = {'script': ''}
    full_prompt = gpt_utils.load_yaml_file('shortGPT/prompt_templates/chat_video_script.yaml')
    system = full_prompt['system_prompt']
    chat = full_prompt['chat_prompt']
    input = chat.replace("<<DESCRIPTION>>", script_description).replace("<<LANGUAGE>>", language)
    while not ('script' in out and out['script']):
        try:
            result = gpt_utils.gpt3Turbo_completion(prompt=input, system=system, temp=1)
            out = json.loads(result)
        except Exception as e:
            print(e, "Difficulty parsing the output in gpt_chat_video.generateScript")
    return out['script']

def correctScript(script, correction):
    out = {'script': ''}
    full_prompt = gpt_utils.load_yaml_file('shortGPT/prompt_templates/chat_video_edit_script.yaml')
    system = full_prompt['system_prompt']
    chat = full_prompt['chat_prompt']
    input = chat.replace("<<ORIGINAL_SCRIPT>>", script).replace("<<CORRECTIONS>>", correction)
    result = gpt_utils.gpt3Turbo_completion(prompt=input, system=system, temp=1)
    while not ('script' in out and out['script']):
        try:
            result = gpt_utils.gpt3Turbo_completion(prompt=input, system=system, temp=1)
            out = json.loads(result)
        except Exception as e:
            print("Difficulty parsing the output in gpt_chat_video.generateScript")
    return out['script']