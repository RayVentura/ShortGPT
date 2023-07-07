from abc import ABC, abstractmethod
class VoiceModule(ABC):

    def __init__(self):
        pass
    @abstractmethod    
    def update_usage(self):
        pass

    @abstractmethod
    def get_remaining_characters(self):
        pass

    @abstractmethod
    def generate_voice(self,text, outputfile):
        pass