from typing import List, Dict
from abc import ABC, abstractmethod


class BaseImageAnalyzer(ABC):

    @abstractmethod
    def __init__(self, model: str, api_key: str):
        raise NotImplementedError

    @abstractmethod
    def analyze(self, prompt: str, image: str) -> List[Dict[str, str]]:
        raise NotImplementedError
