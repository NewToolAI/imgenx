from typing import List, Dict
from abc import ABC, abstractmethod


class BaseVideoGenerator(ABC):

    @abstractmethod
    def __init__(self, model: str, api_key: str):
        raise NotImplementedError

    @abstractmethod
    def text_to_video(self, prompt: str, resolution: str, ratio: str, duration: int) -> Dict[str, str]:
        raise NotImplementedError

    @abstractmethod
    def image_to_video(self, prompt: str, first_frame: str, last_frame: str|None, 
                       resolution: str, ratio: str, duration: int) -> Dict[str, str]:
        raise NotImplementedError
