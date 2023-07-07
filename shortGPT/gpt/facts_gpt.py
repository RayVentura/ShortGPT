from shortGPT.gpt import gpt_utils
import json
def generateFacts(facts_type):
    full_prompt = gpt_utils.load_yaml_file('shortGPT/prompt_templates/facts_generator.yaml')
    system = full_prompt['system_prompt']
    chat = full_prompt['chat_prompt']
    input = chat.replace("<<FACTS_TYPE>>", facts_type)
    result = gpt_utils.gpt3Turbo_completion(prompt=input, system=system, temp=1.3)
    return result

def generateFactSubjects(n):
    out = []
    full_prompt = gpt_utils.load_yaml_file('shortGPT/prompt_templates/facts_subjects_generation.yaml')
    system = full_prompt['system_prompt']
    chat = full_prompt['chat_prompt']
    input = chat.replace("<<N>>", f"{n}")
    count = 0
    while len(out) != n:
        result = gpt_utils.gpt3Turbo_completion(prompt=input, system=system, temp=1.69)
        count+=1
        try:
            out = json.loads(result.replace("'", '"'))
        except Exception as e:
            print(f"INFO - Failed generating {n} fact subjects after {count} trials", e)
            pass
        
    return out