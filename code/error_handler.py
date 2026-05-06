import time

def retry_on_error(func, max_retries=3, delay=5):
    """Retry a function on error up to max_retries times"""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Error: {e}. Retrying in {delay}s... (attempt {attempt + 1}/{max_retries})")
                time.sleep(delay)
            else:
                print(f"Failed after {max_retries} attempts: {e}")
                return None