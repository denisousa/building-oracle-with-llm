from datetime import datetime
from functools import wraps

def time_it(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = datetime.now()  # Tempo de início
        result = func(*args, **kwargs)  # Executa a função original
        end_time = datetime.now()  # Tempo de término
        execution_time = end_time - start_time  # Calcula o tempo de execução
        print(f"\nExecution time for {func.__name__}: {execution_time}\n")
        return result
    return wrapper
