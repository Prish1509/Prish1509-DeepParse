import re

# this function uses regex patterns to classify log messages
def classify_with_regex(log_message):
    # dictionary of known patterns and their matching labels
    regex_patterns = {
        r"User User\d+ logged (in|out).*": "User Action",
        r"Backup (started|ended) at .*": "System Notification",
        r"Backup completed successfully.*": "System Notification",
        r"System updated to version .*": "System Notification",
        r"File .* uploaded successfully by user .*": "System Notification",
        r"Disk Cleanup completed successfully.*": "System Notification",
        r"System reboot initiated by user .*": "System Notification",
        r"Account with ID .* created by .*": "User Action"
    }

    # check if any pattern matches the log message
    for pattern, label in regex_patterns.items():
        if re.search(pattern, log_message, re.IGNORECASE):
            return label

    # if no pattern matched, return None
    return None

if __name__ == "__main__":
    # test the function with different kinds of log messages
    print(classify_with_regex("User User123 logged in."))
    print(classify_with_regex("Backup started at 12:00."))
    print(classify_with_regex("Backup completed successfully."))
    print(classify_with_regex("System updated to version 1.0.0."))
    print(classify_with_regex("File file1.txt uploaded successfully by user user1."))
    print(classify_with_regex("Disk cleanup completed successfully."))
    print(classify_with_regex("System reboot initiated by user user1."))
    print(classify_with_regex("Hey Bro, chill ya!"))  # this one should return None
