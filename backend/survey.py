import json


class NPI40Survey:
    _instance = None
    _questions = []

    def __new__(cls, file_path="npi_40.json"):
        if cls._instance is None:
            cls._instance = super(NPI40Survey, cls).__new__(cls)
            cls._instance._load_questions(file_path)
        return cls._instance

    def _load_questions(self, file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
        self._questions = data.get("questions", [])

    def get_questions(self):
        return self._questions

    def calculate_narcissistic_score(self, answers):
        score = 0
        for question, answer in zip(self._questions, answers):
            if answer == question["narcissistic_choice"]:
                score += 1
        return score
