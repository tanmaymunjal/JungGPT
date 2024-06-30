import json
from survey import NPI40Survey


def prompt_user_for_answers(
    survey: NPI40Survey, num_questions: int = 40
) -> tuple[list[int], list[dict]]:
    answers = []
    questions = survey.get_questions()[:num_questions]
    for question in questions:
        print(f"Question {question['id']}:")
        print(f"1: {question['option1']}")
        print(f"2: {question['option2']}")
        while True:
            try:
                answer = int(input("Select an option (1/2): "))
                if answer not in [1, 2]:
                    raise ValueError("Invalid input. Please enter 1 or 2.")
                answers.append(answer)
                break
            except ValueError as e:
                print(f"Error: {e}")
    return answers, questions


def save_responses_and_score(
    answers: list[int],
    questions: list[dict],
    score: int,
    output_file: str = "responses.json",
) -> None:
    responses = [
        {
            "option1": question["option1"],
            "option2": question["option2"],
            "selected_option": answer,
        }
        for question, answer in zip(questions, answers)
    ]

    result = {"responses": responses, "npi_score": score}

    try:
        with open(output_file, "w") as file:
            json.dump(result, file, indent=4)
        print(f"Responses and score saved to {output_file}")
    except IOError as e:
        print(f"Error saving responses: {e}")


def main():
    survey = NPI40Survey()
    answers, questions = prompt_user_for_answers(survey)
    score = survey.calculate_narcissistic_score(answers)
    save_responses_and_score(answers, questions, score)


if __name__ == "__main__":
    main()
