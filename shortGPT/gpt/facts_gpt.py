from shortGPT.gpt import gpt_utils
import json
def generateFacts(facts_type):
    chat, system = gpt_utils.load_yaml_prompt('shortGPT/prompt_templates/facts_generator.yaml')
    chat = chat.replace("<<FACTS_TYPE>>", facts_type)
    result = gpt_utils.gpt3Turbo_completion(chat_prompt=chat, system=system, temp=1.3)
    return result

def generateFactSubjects(n):
    out = []
    chat, system = gpt_utils.load_yaml_prompt('shortGPT/prompt_templates/facts_subjects_generation.yaml')
    chat = chat.replace("<<N>>", f"{n}")
    count = 0
    while len(out) != n:
        result = gpt_utils.gpt3Turbo_completion(chat_prompt=chat, system=system, temp=1.69)
        count+=1
        try:
            out = json.loads(result.replace("'", '"'))
        except Exception as e:
            print(f"INFO - Failed generating {n} fact subjects after {count} trials", e)
            pass
        
    return out