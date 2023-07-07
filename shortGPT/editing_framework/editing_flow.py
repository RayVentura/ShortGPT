import json
from typing import Any, Dict, List, Union
from enum import Enum
import collections.abc

from shortGPT.editing_framework.core_editing_engine import CoreEditingEngine

def update_dict(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update_dict(d.get(k, {}), v)
        else:
            d[k] = v
    return d


class EditingStep(Enum):
    CROP_1920x1080 = "crop_1920x1080_to_short.json"
    ADD_CAPTION = "make_caption.json"
    ADD_CAPTION_ARABIC = "make_caption_arabic.json"
    ADD_WATERMARK = "show_watermark.json"
    ADD_SUBSCRIBE_ANIMATION = "subscribe_animation.json"
    SHOW_IMAGE = "show_top_image.json"
    ADD_VOICEOVER_AUDIO = "add_voiceover.json"
    ADD_BACKGROUND_MUSIC = "background_music.json"
    ADD_REDDIT_IMAGE = "show_reddit_image.json"

class Flow(Enum):
    WHITE_REDDIT_IMAGE_FLOW = "build_reddit_image.json"

STEPS_PATH = "shortGPT/editing_framework/editing_steps/"
FLOWS_PATH = "shortGPT/editing_framework/flows/"


class EditingFlow:
    def __init__(self,):
        self.editing_step_tracker = dict((step, 0) for step in EditingStep)
        self.schema = {'visual_assets': {}, 'audio_assets': {}}

    def addEditingStep(self, editingStep: EditingStep, args: Dict[str, any] = {}):
        json_step = json.loads(
            open(STEPS_PATH+editingStep.value, 'r', encoding='utf-8').read())
        step_name, editingStepDict = list(json_step.items())[0]
        if 'inputs' in editingStepDict:
            required_args = (editingStepDict['inputs']['actions'] if 'actions' in editingStepDict['inputs'] else []) + (editingStepDict['inputs']['parameters'] if 'parameters' in editingStepDict['inputs'] else [])
            for required_argument in required_args:
                if required_argument not in args:
                    raise Exception(
                        f"Error. '{required_argument}' input missing, you must include it to use this editing step")
            if required_args:
                pass
            action_names = [action['type'] for action in editingStepDict['actions']
                            ] if 'actions' in editingStepDict else []
            param_names = [param_name for param_name in editingStepDict['parameters']
                           ] if 'parameters' in editingStepDict else []
            for arg_name in args:
                if ('inputs' in editingStepDict):
                    if 'parameters' in editingStepDict['inputs'] and arg_name in param_names:
                        editingStepDict['parameters'][arg_name] = args[arg_name]
                        pass
                    if 'actions' in editingStepDict['inputs'] and arg_name in action_names:
                        for i, action in enumerate(editingStepDict['actions']):
                            if action['type'] == arg_name:
                                editingStepDict['actions'][i]['param'] = args[arg_name]
        if editingStepDict['type'] == 'audio':
            self.schema['audio_assets'][f"{step_name}_{self.editing_step_tracker[editingStep]}"] = editingStepDict
        else:
            self.schema['visual_assets'][f"{step_name}_{self.editing_step_tracker[editingStep]}"] = editingStepDict
        self.editing_step_tracker[editingStep] += 1


    def ingestFlow(self, flow: Flow, args):
        json_flow = json.loads(open(FLOWS_PATH+flow.value, 'r', encoding='utf-8').read())
        for required_argument in list(json_flow['inputs'].keys()):
                if required_argument not in args:
                    raise Exception(
                        f"Error. '{required_argument}' input missing, you must include it to use this editing step")
                update = args[required_argument]
                for path_key in reversed(json_flow['inputs'][required_argument].split("/")):
                    update = {path_key: update}
                json_flow = update_dict(json_flow, update)
        self.schema = json_flow

    def dumpEditingSchema(self):
        return self.schema
    
    def renderVideo(self, outputPath, logger=None):
        engine = CoreEditingEngine()
        engine.generate_video(self.schema, outputPath, logger=logger)
    def renderImage(self, outputPath):
        engine = CoreEditingEngine()
        engine.generate_image(self.schema, outputPath)



# editingflow = EditingFlow()
# editingflow.ingestFlow(Flow.WHITE_REDDIT_IMAGE_FLOW, {
#     "username_text": "Hello world1",
#     "ncomments_text": "Hello world2",
#     "nupvote_text": "Hello world3",
#     "question_text": "Hello world4"
# })
# print(editingflow.dumpEditingSchema())
# editingflow.addEditingStep(EditingStep.ADD_VOICEOVER_AUDIO, {'url': "editing_test/audio_voice.wav"})
# editingflow.addEditingStep(EditingStep.ADD_BACKGROUND_MUSIC, {'url': "editing_test/music.wav",
#                                                               'loop_background_music': 45, "volume_percentage": 0.09})
# editingflow.addEditingStep(EditingStep.CROP_1920x1080, {'url': 'editing_test/clippedBackground.mp4'})
# editingflow.addEditingStep(EditingStep.ADD_SUBSCRIBE_ANIMATION)
# editingflow.addEditingStep(EditingStep.ADD_WATERMARK, {'text': "WRITEPRODIGY"})
# for i in range(0, 30):
#     editingflow.addEditingStep(EditingStep.ADD_CAPTION, {'text': f'HELLO{i}',
#                                                      'set_time_start': i,
#                                                      'set_time_end': i+1})
# editingflow.addEditingStep(EditingStep.SHOW_IMAGE, {'url': "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRMGHxMzcs0p4qEZuhcKVwlcvpb9jC6eyMLcoL2ODo4EQ&usqp=CAU&ec=48600113",
#                                                     "set_time_start": 3, "set_time_end": 10})
# with open("shortGPT/editing_framework/temp.json", "w", encoding="utf-8") as f:
#     f.write(json.dumps(editingflow.dumpEditingSchema()))

