# === User input ====

def user_input() -> dict[str, int]:
    """ Enters a subject name and its duration """

    subjects: dict[str, int] = {}

    while True:
        user_subject = input("Enter subject name: ")
        if user_subject == "":
            break

        while True:
            try:
                duration = int(input(f"Enter time allocated for {user_subject}: "))

                if duration < 0:
                    continue

                subjects[user_subject] = duration
                break
            except ValueError:
                continue

    return subjects

def main() -> None:
    subjects_duration = user_input()