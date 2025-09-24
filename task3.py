import os
import re
import sys
from collections import namedtuple, Counter
from typing import Optional

LogEntry = namedtuple("LogEntry", ["date", "time", "level", "message"])
# Format is: YYYY-MM-DD hh-mm-ss LOG_LEVEL MESSAGE
LOG_FORMAT_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\s+(INFO|WARNING|ERROR|DEBUG)\s+.*$")

def load_logs(file_path: str) -> list[LogEntry]:
    log_list: list[LogEntry] = []

    with open(file_path, "r") as log_file:
        for line_number, line in enumerate(log_file, start=1):
            line = line.strip()
            if line:
                log = parse_log_line(line)
                if not log:
                    print(f"Incorrect log line format at line number: {line_number}, will skip this line")
                else:
                    log_list.append(log)

    return log_list


def parse_log_line(line: str) -> Optional[LogEntry]:
    if LOG_FORMAT_PATTERN.match(line):
        date, time, level, message = line.split(" ", maxsplit=3)
        return LogEntry(date=date, time=time, level=level, message=message)
    else:
        return None


def filter_logs_by_level(logs: list[LogEntry], level: str) -> list[LogEntry]:
    return list(filter(lambda log: log.level == level, logs))


def count_logs_by_level(logs: list) -> dict[str, int]:
    return dict(Counter(entry.level for entry in logs))


def display_log_counts(log_counts: dict[str, int]):
    level_width = max(len("Log level"), *(len(level) for level in log_counts.keys()))
    count_width = max(len("Number"), *(len(str(count)) for count in log_counts.values()))

    print(f"{'Log level':<{level_width}} | {'Count':>{count_width}}")
    print(f"{'-' * level_width}-|{'-' * count_width}")

    for level, count in log_counts.items():
        print(f"{level:<{level_width}} | {count:<{count_width}}")

    print("\n")


def display_filtered_logs_by_level(log_level: str, filtered_logs: list[LogEntry]):
    print(f"Details for logs under log level: '{log_level}'")
    for log in filtered_logs:
        print(f"{log.date} {log.time} {log.message}")

if __name__ == "__main__":
    if len(sys.argv) == 1 or len(sys.argv) > 3:
        print("Usage: python task3.py <file_path> <[optional log level]>")
        sys.exit(1)
    else:
        if os.path.exists(sys.argv[1]):
            logs = load_logs(sys.argv[1])
            if len(sys.argv) == 3:
                log_level = sys.argv[2].upper()
                filtered_logs = filter_logs_by_level(logs, log_level)
                display_log_counts(count_logs_by_level(filtered_logs))
                display_filtered_logs_by_level(log_level, filtered_logs)
            else:
                display_log_counts(count_logs_by_level(logs))
        else:
            print(f"No such file: {sys.argv[1]}")