import sys
sys.path.insert(0, '../../..')
import base64
import time
from pathlib import Path
from typing import List, Dict
from volcenginesdkarkruntime import Ark

from imgenx.predictor.base.base_video_generator import BaseVideoGenerator


class DoubaoVideoGenerator(BaseVideoGenerator):

    def __init__(self, model: str, api_key: str):
        self.model = model
        self.client = Ark(
            base_url='https://ark.cn-beijing.volces.com/api/v3',
            api_key=api_key,
        )

    def text_to_video(self, prompt: str, resolution: str = '720p', ratio: str = '16:9', duration: int = 5) -> str:
        create_result = self.client.content_generation.tasks.create(
            model=self.model,
            content=[
                {
                    'type': 'text',
                    'text': prompt.strip()
                }
            ],
            extra_body={
                'resolution': resolution,
                'ratio': ratio,
                'duration': duration,
            }
        )
        task_id = create_result.id

        while True:
            get_result = self.client.content_generation.tasks.get(task_id=task_id)
            status = get_result.status
            if status == "succeeded":
                return get_result.content.video_url
            elif status == "failed":
                raise Exception(str(get_result.error))
            else:
                time.sleep(3)

    def image_to_video(self, prompt: str, first_frame: str, last_frame: str|None = None, 
                       resolution: str = '720p', ratio: str = '16:9', duration: int = 5) -> str:
        if not first_frame.startswith('http'):
            first_frame = self._image_to_base64(first_frame)

        if last_frame is not None and not last_frame.startswith('http'):
            last_frame = self._image_to_base64(last_frame)

        content = [
            {
                'type': 'text',
                'text': prompt.strip()
            },
            {
                'type': 'image_url',
                'image_url': {
                    'url': first_frame
                },
                'role': 'first_frame'
            }
        ]

        if last_frame is not None:
            content.append({
                'type': 'image_url',
                'image_url': {
                    'url': last_frame
                },
                'role': 'last_frame'
            })

        create_result = self.client.content_generation.tasks.create(
            model=self.model,
            content=content,
            extra_body={
                'resolution': resolution,
                'ratio': ratio,
                'duration': duration,
            }
        )
        task_id = create_result.id

        while True:
            get_result = self.client.content_generation.tasks.get(task_id=task_id)
            status = get_result.status
            if status == "succeeded":
                return get_result.content.video_url
            elif status == "failed":
                raise Exception(str(get_result.error))
            else:
                time.sleep(3)

    def _image_to_base64(self, image_path: str) -> str:
        image_path = Path(image_path)

        with open(image_path, 'rb') as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            base64_image = f'data:image/{image_path.suffix.strip(".")};base64,{base64_image}'

        return base64_image


if __name__ == '__main__':
    import os
    from dotenv import load_dotenv

    load_dotenv()

    api_key = os.getenv('IMGENX_API_KEY')
    model = 'doubao-seedance-1-0-pro-fast-251015' 

    generator = DoubaoVideoGenerator(model, api_key)
    image = '/Volumes/DATA/个人/project/imgenx-mcp-server/logo.jpg'
    result = generator.image_to_video('一个人在运动', resolution='720p', ratio='16:9', first_frame=image, duration=5)
    print(result)
