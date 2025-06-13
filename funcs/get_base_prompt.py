def get_base_prompt(base_path):
    with open(base_path, 'r', encoding='utf-8') as f:
        base_prompt = f.read()

    return base_prompt