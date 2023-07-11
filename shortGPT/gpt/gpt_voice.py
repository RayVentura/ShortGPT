
from shortGPT.gpt import gpt_utils
def getGenderFromText(text):
    chat, system = gpt_utils.load_yaml_prompt('shortGPT/prompt_templates/voice_identify_gender.yaml')
    chat = chat.replace("<<STORY>>", text)
    result = gpt_utils.gpt3Turbo_completion(chat_prompt=chat, system=system).replace("\n", "").lower()
    if 'female' in result:
        return 'female'
    return 'male'