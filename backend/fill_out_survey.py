from chatbot import MistralModel
from config import config
from survey import NPI40Survey
import json


def fill_survey_option(chatbot: MistralModel, survey_ques: str) -> dict:
    messages = [
        {
            "role": "system",
            "content": "You are taking a survey on narcissism, you will be presented two options at all times.Respond accurately to the option that you think suits you best in the json format {'key':1} or {'key':2}.",
        },
        {"role": "user", "content": survey_ques},
    ]

    response = chatbot.get_completion(messages)
    return json.loads(response)


def generate_model_npi40_score(
    chatbot: MistralModel, survey: NPI40Survey
) -> (int, int):
    answers = []
    anwsered_ques = 0
    for ques in survey.get_questions():
        response = fill_survey_option(
            chatbot, f"Option 1: {ques['option1']} Option 2: {ques['option2']}"
        )
        answer = response.get("key")
        if answer:
            answers.append(answer)
            anwsered_ques += 1
    score = survey.calculate_narcissistic_score(answers)
    return score, anwsered_ques


if __name__ == "__main__":
    api_key = config.get("Mistral", "API_KEY")
    model_id = "ft:open-mistral-7b:bf1a70be:20240630:9fbc9c74"
    mistral_model = MistralModel(api_key, model_id)
    survey = NPI40Survey()
    print(generate_model_npi40_score(mistral_model, survey))
