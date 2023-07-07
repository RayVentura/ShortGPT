from shortGPT.gpt import gpt_utils
from shortGPT.database.content_data_manager import ContentDataManager
import json

class APITracker:

    def __init__(self):
        self.initiateAPITracking()
        
    def setDataManager(self, contentManager : ContentDataManager):
        if(not contentManager):
            raise Exception("contentManager is null")
        self.datastore = contentManager

    def openAIWrapper(self, gptFunc):

        def wrapper(*args, **kwargs):
            result = gptFunc(*args, **kwargs)
            prompt = kwargs.get('prompt') or kwargs.get('conversation') or args[0]
            prompt = json.dumps(prompt)
            if self.datastore and result:
                tokensUsed = gpt_utils.num_tokens_from_messages([prompt, result])
                self.datastore.save('api_openai', tokensUsed, add=True)
            return result

        return wrapper
    
    def elevenWrapper(self, audioFunc):

        def wrapper(*args, **kwargs):
            result = audioFunc(*args, **kwargs)
            textInput = kwargs.get('text') or args[0]
            if self.datastore and result:
                self.datastore.save('api_eleven', len(textInput), add=True)
            return result

        return wrapper
    

    def wrap_turbo(self):
        func_name = "gpt3Turbo_completion"
        module = __import__("gpt_utils", fromlist=["gpt3Turbo_completion"])
        func = getattr(module, func_name)
        wrapped_func = self.openAIWrapper(func)
        setattr(module, func_name, wrapped_func)
    
    def wrap_eleven(self):
        func_name = "generateVoice"
        module = __import__("audio_generation", fromlist=["generateVoice"])
        func = getattr(module, func_name)
        wrapped_func = self.elevenWrapper(func)
        setattr(module, func_name, wrapped_func)

    
    def initiateAPITracking(self):
        self.wrap_turbo()
        self.wrap_eleven()



