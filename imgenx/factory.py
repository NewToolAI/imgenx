from pathlib import Path
from functools import cache
from importlib import import_module

from imgenx.predictor.base.base_image_generator import BaseImageGenerator
from imgenx.predictor.base.base_video_generator import BaseVideoGenerator
from imgenx.predictor.base.base_image_analyzer import BaseImageAnalyzer


@cache
def create_image_generator(model: str, api_key: str) -> BaseImageGenerator:
    return create_predictor(model, api_key, 'image_generator')


@cache
def create_video_generator(model: str, api_key: str) -> BaseVideoGenerator:
    return create_predictor(model, api_key, 'video_generator')


@cache
def create_image_analyzer(model: str, api_key: str) -> BaseImageAnalyzer:
    return create_predictor(model, api_key, 'image_analyzer')


def create_predictor(model: str, api_key: str, role: str) -> BaseImageAnalyzer:
    provider, model = model.split(':')
    provider = provider.lower()

    if provider not in get_providers():
        raise ValueError(f'Provider {provider} not found.')

    predictor_package = f'imgenx.predictor.generators.{provider}_{role.lower()}'
    predictor_class = f'{provider.capitalize()}{role.split("_")[0].capitalize()}{role.split("_")[1].capitalize()}'

    try:
        package = import_module(predictor_package)
        predictor = getattr(package, predictor_class)
    except (ImportError, AttributeError):
        raise ValueError(f'Provider {provider} not found.')

    return predictor(model, api_key)


@cache
def get_providers():
    providers = set()
    for path in (Path(__file__).parent / 'predictor/generators').glob('*_*_*.py'):
        providers.add(path.stem.split('_')[0])

    return list(providers)
