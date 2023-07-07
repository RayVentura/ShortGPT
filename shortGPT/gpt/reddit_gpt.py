from . import gpt_utils
import random
def generateRedditPostMetadata(title):
    name = generateUsername()
    if title and title[0] == '"':
        title = title.replace('"', '')
    n_months = random.randint(1,11)
    header = f"{name} - {n_months} months ago"
    n_comments = random.random() * 10 + 2
    n_upvotes = n_comments*(1.2+ random.random()*2.5)
    return title, header, f"{n_comments:.1f}k", f"{n_upvotes:.1f}k"


def getInterestingRedditQuestion(redundant_questions=['']):
    full_prompt = gpt_utils.load_json_file('shortGPT/prompt_templates/reddit_question.json')
    last_question = ""
    for question in redundant_questions:
        last_question+=question+"\n"
    system = full_prompt['system']
    input = full_prompt['input'].replace("<<LAST_QUESTIONS>>", last_question)
    result = gpt_utils.gpt3Turbo_completion(prompt=input, system=system, temp=2)
    return result

def createRedditCommentFromQuestion(question):
    full_prompt = gpt_utils.load_json_file('shortGPT/prompt_templates/reddit_script.json')
    system = full_prompt['system']
    input = full_prompt['input'].replace("<<QUESTION>>", question)
    result = "Reddit, " + question +" "+gpt_utils.gpt3Turbo_completion(prompt=input, system=system, temp=1.3)
    return result
    

def getRealisticness(text):
    full_prompt = gpt_utils.load_json_file('shortGPT/prompt_templates/filter_story.json')
    system = full_prompt['system']
    input = full_prompt['input'].replace("<<INPUT>>", text)
    result = gpt_utils.gpt3Turbo_completion(prompt=input, system=system, temp=1)
    try:
        dico = gpt_utils.extract_biggest_json(result)
        if (dico):
            return dico['score']
    except:
        pass
    return gpt_utils.get_first_number(result)


def getQuestionFromThread(text):
    if ((text.find("Reddit, ") < 15) and (10 < text.find("?") < 100)):
        question = text.split("?")[0].replace("Reddit, ", "").strip().capitalize()
    else:
        prompt = gpt_utils.open_file('shortGPT/prompt_templates/get_question.txt').replace("<<STORY>>", text)
        question = gpt_utils.gpt3Turbo_completion(prompt=prompt).replace("\n", "")
        question = question.replace('"', '').replace("?", "")
    return question


def generateUsername():
    full_prompt = gpt_utils.load_yaml_file('shortGPT/prompt_templates/reddit_username.yaml')
    system = full_prompt['system_prompt']
    chat = full_prompt['chat_prompt']
    return gpt_utils.gpt3Turbo_completion(prompt=chat, system=system, temp=2).replace("u/", "")


def getGenderFromText(text):
    prompt = gpt_utils.open_file('shortGPT/prompt_templates/identify_gender.txt').replace("<<STORY>>", text)
    result = gpt_utils.gpt3Turbo_completion(prompt).replace("\n", "").lower()
    if 'female' in result:
        return 'female'
    return 'male'

