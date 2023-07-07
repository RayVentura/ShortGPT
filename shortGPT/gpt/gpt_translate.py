from shortGPT.gpt import gpt_utils

def translateContent(content, language):
    full_prompt = gpt_utils.load_yaml_file('shortGPT/prompt_templates/translate_content.yaml')
    system = full_prompt['system_prompt']
    chat = full_prompt['chat_prompt']
    system = full_prompt['system_prompt'].replace("<<LANGUAGE>>", language)
    input = chat.replace("<<CONTENT>>", content)
    result = gpt_utils.gpt3Turbo_completion(prompt=input, system=system, temp=1)
    return result