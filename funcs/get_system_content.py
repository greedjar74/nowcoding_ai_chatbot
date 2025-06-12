def get_system_content(content_path):
    with open(content_path, 'r', encoding='utf-8') as f:
        system_content = f.read()

    return system_content