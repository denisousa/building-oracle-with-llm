from classify_operations import string_to_bool
from prompts import get_chat_simple_prompt
from time import sleep
import gc


def retry_model_response(execution_context, user_prompt):
    client = execution_context['client']()
    completion = client.chat.completions.create(
                model=execution_context['model'],
                messages=get_chat_simple_prompt(user_prompt),
                max_tokens=5,
                temperature=0.7,
            )

    return completion.choices[0].message.content

def fix_hallucination(output_folder, index, llm_result, execution_context, user_prompt):
    open(f'{output_folder}/error.txt', 'a').write(f'index: {index} - {llm_result}\n')

    while True:
        sleep(1)
        llm_result = retry_model_response(execution_context, user_prompt)
        try:
            llm_result = string_to_bool(llm_result)
            return llm_result
        except:
            pass

