from classify_operations import string_to_bool
from prompts import get_chat_simple_prompt
from time import sleep


def retry_model_response(client,execution_context, user_prompt):
    completion = client.chat.completions.create(
                model=execution_context['model'],
                messages=get_chat_simple_prompt(user_prompt),
                temperature=0.0
            )

    gpt_result = completion.choices[0].message.content
    try:
        gpt_result = string_to_bool(gpt_result)
        return gpt_result
    except:
        return None

def fix_hallucination(output_folder, index, gpt_result, client, execution_context, user_prompt):
    open(f'{output_folder}/error.txt', 'a').write(f'index: {index} - {gpt_result}\n')
    sleep(1)

    while True:
        gpt_result = retry_model_response(client, execution_context, user_prompt)
        if gpt_result is not None:
            return gpt_result