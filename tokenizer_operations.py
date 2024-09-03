from transformers import GPT2Tokenizer

# Inicialize o tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Sua string de código
code_string = """ Seu código aqui """

# Tokenize a string e conte os tokens
tokens = tokenizer.encode(code_string)
print(len(tokens))
