from proglog import ProgressBarLogger
import time

class MoviepyProgressLogger(ProgressBarLogger):
    
    def __init__(self, callBackFunction = None):
        super().__init__()
        self.callBackFunction = callBackFunction
        self.start_time = time.time()
    
    def bars_callback(self, bar, attr, value, old_value=None):
        # Every time the logger progress is updated, this function is called        
        percentage = (value / self.bars[bar]['total']) * 100
        elapsed_time = time.time() - self.start_time
        estimated_time = (elapsed_time / percentage) * (100 - percentage) if percentage != 0 else 0
        progress_string = f'Rendering progress : {value}/{self.bars[bar]["total"]} | Time spent: {self.format_time(elapsed_time)} | Time left: {self.format_time(estimated_time)}'
        if (self.callBackFunction):
            self.callBackFunction(progress_string)
        else:
            print(progress_string)

    def format_time(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        return f'{int(minutes)}m {int(seconds)}s'
