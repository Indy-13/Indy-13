import time


class Logger:
    def __init__(self, config: dict):
        self._log_messages = list()
        self._LOG_SEVERITY = config.get("LOG_SEVERITY", 3)
        self._LOG_FILE = config.get("LOG_FILE")

    def log_message(self, severity: int, level: str, message_text: str):

        date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        log_record = {
            "DateTime": date_time,
            "Level": level.upper(),
            "Message": message_text,
        }

        if severity <= self._LOG_SEVERITY:
            # print(log_record)
            self._log_messages.append(log_record)
            if self._LOG_FILE:
                try:
                    log_file = open(self._LOG_FILE, "a")
                    log_file.write(
                        "{}\t{}\t{}\n".format(
                            log_record["DateTime"],
                            log_record["Level"],
                            log_record["Message"],
                        )
                    )
                    log_file.close()
                except Exception as e:
                    print("Write to log file failed" + str(e))

    def get_log(self):
        return self._log_messages
