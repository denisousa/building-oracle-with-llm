system_prompt = '''
You are an expert in detect code clones
'''

code_example1 = '''
public ToStringInfo ( ITypeBinding typeBinding ) {
    IMethodBinding[] declaredMethods = typeBinding.getDeclaredMethods();
    for ( int i = 0; i < declaredMethods.length; i++ ) {
        if ( declaredMethods[i].getName().equals ( methodName ) && declaredMethods[i].getParameterTypes().length == 0 ) {
            this.foundToString = true;
            if ( Modifier.isFinal ( declaredMethods[i].getModifiers() ) ) {
                this.found = true;
            }
        }
    }
}
'''

code_example2 = '''
public ToStringInfo ( ITypeBinding typeBinding ) {
    IMethodBinding[] declaredMethods = typeBinding.getDeclaredMethods();
    for ( int i = 0; i < declaredMethods.length; i++ ) {
        if ( declaredMethods[i].getName().equals ( methodName ) && declaredMethods[i].getParameterTypes().length == 0 ) {
            this.foundToString = true;
            if ( Modifier.isFinal ( declaredMethods[i].getModifiers() ) ) {
                this.foundFinalToString = true;
            }
        }
    }
}
'''

user_example_prompt = f'''
Are these two codes clones of each other? True or False?
Code1: {code_example1}
Code2: {code_example2}
'''

assistant_example_prompt = f'''
True
'''

def get_prompt_to_compare_two_codes(code1, code2):
    return f'''
    Are these two codes clones of each other? True or False?
    Let me know their type, whether it is a Type-I, Type-II, Type-III or Type-IV clone.
    Code1: \n{code1}
    Code2: \n{code2}

    Your answer should be succinct, for example:
    True, they are Type-1 clones;
    '''

def get_chat_prompt_with_example(user_prompt):
    return [
            {"role": "system", "content": system_prompt},
            {"role": "assistant", "content": "I will answer only True or False"},
            {"role": "user", "content": user_example_prompt},
            {"role": "assistant", "content": assistant_example_prompt},
            {"role": "user", "content": user_prompt}
        ]

def get_chat_simple_prompt(user_prompt):
    return [
            {"role": "system", "content": system_prompt},
            {"role": "assistant", "content": "I will answer only True or False"},
            {"role": "user", "content": user_prompt},
        ]