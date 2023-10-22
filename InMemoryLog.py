from datetime import datetime


class InMemoryLog:
    _logs = []
    _last_read = -1

    @staticmethod
    def info(msg: str):
        InMemoryLog._logs.append(f'{datetime.utcnow()} INFO: {msg}')

    @staticmethod
    def read_new():
        msg = ''
        for i in range(InMemoryLog._last_read + 1, len(InMemoryLog._logs)):
            msg += f'{InMemoryLog._logs[i]}\n'
        InMemoryLog._last_read = len(InMemoryLog._logs) - 1
        return msg