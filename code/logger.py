from time import localtime

def log(message: str) -> None:
    """
    Logs a message to a file with a timestamp.
    """
    t = localtime()
    timestamp = f"{t[0]:04}-{t[1]:02}-{t[2]:02} {t[3]:02}:{t[4]:02}:{t[5]:02}"
    print(f"[{timestamp}] {message}")
    with open("log.txt", "a", encoding="utf-8") as logs:
        logs.write(f"[{timestamp}] {message}\n")
        logs.flush()
