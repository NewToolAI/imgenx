def get_provider_model_api_key(task, headers_or_env):
    task = task.strip()

    try:
        headers_or_env = {key.lower(): value for key, value in headers_or_env.items()}
        provider_model_name = f'imgenx_{task}'
        provider_model = headers_or_env.get(provider_model_name)
        provider, model = provider_model.split(':')
    except:
        provider = None
    
    api_key = headers_or_env.get(f'imgenx_{provider}_api_key')

    return provider_model, api_key

