import re
from datetime import datetime
from collections import OrderedDict
from bisect import bisect_left
from typing import List


class EpisodesAPI:
    """The API for the episodes
    """
    
    def get_episode_transcriptions(self, episode_id:str) -> OrderedDict:
        """
        Returns the transcriptions of an episode.
        """
        transcriptions = []
        with open(f'{episode_id}.txt', 'r') as f:
            transcriptions = f.readlines()
        return self.build_transcription(transcriptions)
    
    def build_transcription(self, lines:List[str]) -> OrderedDict:
        """From a list of strings representing lines of a transcript,
        builds a TranscriptionSegment object.
        """
        transcriptions = TranscriptionSegments()
        current_key = None
        for line_w_end in lines:
            line = line_w_end.strip()
            is_time = re.match(r'^(0?[1-9]?|1[0-2]):[0-5][0-9]$', line) or \
                re.match(r'^(?:[0-9]\d?|[0-9]):(?:[0-9]\d):(?:[0-9]\d)$', line)
            if is_time:
                len_time = len(line.split(':'))
                current_key = datetime.strptime(line, '%H:%M:%S') if len_time == 3 \
                    else datetime.strptime(line, '%M:%S')
                continue
            if line.strip() == '':
                continue
            
            int_key = current_key.second + current_key.minute*60 + current_key.hour*360
            transcriptions[int_key] = line
            
        return transcriptions


class PodcastEpisode:
    """Represents a podcast episode and the transcriptions of it.
    """
    
    def __init__(self, id, transcriptions:OrderedDict) -> None:
        self.id = id
        self.transcriptions = transcriptions


class TranscriptionSegments(OrderedDict):
    """An extension of the OrderedDict to store the 
    transcriptions and the times of an episode.
    """
    
    def __get_closest_key(self, timestamp):
        """Get the closest time in the dictionary for a given time.
        Ex: 
        Giving a dict with the following keys:
        [3, 7, 9]
        get_closest_key(6) == 7
        get_closest_key(7) == 7
        """
        if timestamp in self:
            return timestamp
        
        key_list = list(self.keys()) 
        pos = bisect_left(key_list, timestamp)
        return key_list[pos]
    
    def get_transcription(self, start_timestamp, end_timestamp):
        """Giving a start and end timestamp, returns the corresponding transcription
        using the following algorithm:
        1. Get the closest key
        2. if the key exists, return the corresponding transcription
        3. Calculate the offset of words and return the corresponding transcription
        """
        if end_timestamp < start_timestamp:
            raise ValueError('End time must be greater than start time')
          
        initial_key = self.__get_closest_key(start_timestamp)
        final_key = self.__get_closest_key(end_timestamp)
        
        if initial_key == start_timestamp and final_key == end_timestamp:
            return self.get(initial_key, None)
        
        splitted_words = self.get(initial_key).strip().split(" ")
        words_len = len(splitted_words)
        
        final_initial_diff = final_key - initial_key
        if final_initial_diff == 0:
            return None
        
        if initial_key == start_timestamp and final_key != end_timestamp:
            offset = end_timestamp - initial_key
            words_to_return = round((words_len * offset) / final_initial_diff)
            
            return " ".join(splitted_words[:words_to_return])
        
        if initial_key != start_timestamp and final_key == end_timestamp:
            offset = initial_key - start_timestamp
            words_to_return = round((words_len * offset) / final_initial_diff)
            
            return " ".join(splitted_words[words_to_return:])
        
        return None
        
        
        
        
