from time import sleep

def print_progress(index):
    if index % 20 == 0 and index > 0:
        sleep(3)
        print(f"Processing row {index}...")
