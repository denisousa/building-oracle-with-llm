system_prompt = '''
You are an expert in detect code clones
'''

def get_prompt_to_compare_two_codes(code1, code2):
    return f'''Are these two codes clones of each other? True or False?
    Code1: {code1}
    Code2: {code2}
    '''