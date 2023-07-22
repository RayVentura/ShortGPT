from shortGPT.gpt import gpt_utils

def translateContent(content, language):
    chat, system = gpt_utils.load_yaml_prompt('shortGPT/prompt_templates/translate_content.yaml')
    if language == "arabic":
        language =="arabic, and make the translated text two third of the length of the original."
    system = system.replace("<<LANGUAGE>>", language)
    chat = chat.replace("<<CONTENT>>", content)
    result = gpt_utils.gpt3Turbo_completion(chat_prompt=chat, system=system, temp=1)
    return result