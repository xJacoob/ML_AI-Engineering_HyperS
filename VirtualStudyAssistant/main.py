"""Virtual study assistant.

Builds a study plan, tracks study progress and generates
a motivational message using a local LLM.
"""

from huggingface_hub import InferenceClient

def user_input() -> dict[str, int]:
    """Enters a subject name and its duration"""
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


def calculate_breaks_and_subjects(subjects: dict[str, int]) -> tuple[int, int]:
    """Calculates breaks between subjects and subjects total duration"""
    total_subject_duration = 0
    for time in subjects.values():
        total_subject_duration += time

    breaks = (total_subject_duration // 45) * 15
    return total_subject_duration, breaks


def calculate_progress(subjects: dict[str, int]) -> float:
    """Calculates progress of how much time spend on studying"""
    total_subject_duration, _ = calculate_breaks_and_subjects(subjects)
    time_studied = 0

    if total_subject_duration == 0:
        return 100.0

    while True:
        try:
            time_studied = int(input("Enter time spent studying: "))

            if time_studied < 0:
                continue
            break
        except ValueError:
            continue

    progress = min((time_studied / total_subject_duration) * 100, 100.0)
    return progress


def pretty_output(subjects: dict[str, int]) -> None:
    """Pretty prints for the subjects and its durations, also including breaks"""
    subjects_duration, breaks = calculate_breaks_and_subjects(subjects)
    print("Your study plan:")
    for subject, duration in subjects.items():
        print(f"{subject}: {duration} minutes")
    print(f"Total study time: {subjects_duration} minutes")
    print(f"Total time including breaks: {subjects_duration + breaks} minutes")


def generate_motivation(
    client: InferenceClient, subjects: dict[str, int], completeness: float
) -> str:
    """Generates a motivational message with a local LLM."""
    prompt = (
        f"I have to prepare for my {','.join(subjects.keys())} exams. "
        f"I've completed {completeness:.2f}% of my curriculum. "
        f"My motivation should be:"
    )

    response = client.chat_completion(
        messages=[{"role": "user", "content": prompt}],
        model="tinyllama",
        temperature=0.01,
        max_tokens=50,
        seed=42,
    )

    return response.choices[0].message.content


def main() -> None:
    client = InferenceClient(base_url="http://localhost:11434/v1", api_key="ollama")

    subjects_duration = user_input()

    if not subjects_duration:
        return

    pretty_output(subjects_duration)
    time_studied = calculate_progress(subjects_duration)
    print(f"You have completed {time_studied:.2f}% of your planned study time.")
    response = generate_motivation(client, subjects_duration, time_studied)
    print(response)


if __name__ == "__main__":
    main()
