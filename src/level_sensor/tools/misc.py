import json
from datetime import datetime, timedelta

def to_list(json_list_string: str):
    try:
        json_list = json.loads(json_list_string)
        assert isinstance(json_list, list)
        return json_list
    except:
        return None

class Bouncer:
    def __init__(self, bouncing_time=0.2):
        self.last_call_times = {}
        self.last_call_results = {}
        self.bouncing_time = timedelta(seconds=bouncing_time)

    def call_again(self, method, now):
        return self.last_call_times[method] + self.bouncing_time < now

    def apply(self, method):
        def inner(*args, **kwargs):
        
            now = datetime.now()

            uncalled_method = method not in self.last_call_times

            if uncalled_method or self.call_again(method, now):
                self.last_call_times[method] = now
                self.last_call_results[method] = method(*args, **kwargs)
                return self.last_call_results[method]
            else:
                return self.last_call_results[method]
        
        return inner
    
