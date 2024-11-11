import time

def start_timer(duration):
    start_time = time.time()
    end_time = start_time + duration
    print(f"Sınav başladı! Süre: {duration} saniye.")
    return start_time, end_time

def check_time_remaining(start_time, duration):
    elapsed_time = time.time() - start_time
    remaining_time = duration - elapsed_time
    
    if remaining_time <= 0:
        print("\nSüreniz doldu!")
        return True
    else:
        print(f"Kalan süre: {remaining_time:.2f} saniye", end="\r")
        return False
