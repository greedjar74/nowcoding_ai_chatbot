def get_teaching_prompt(content_path):
    with open(content_path, 'r', encoding='utf-8') as f:
        input_content = f.read()

    return input_content