def get_test_case(test_case_path):
    with open(test_case_path, 'r', encoding='utf-8') as f:
        test_case = f.read()

    return test_case