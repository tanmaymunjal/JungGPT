import requests


class MistralModel:
    def __init__(self, api_key, model_id):
        self.api_key = api_key
        self.model_id = model_id
        self.base_url = "https://api.mistral.ai/v1/"

    def get_completion(self, messages, response_format={"type": "json_object"}):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model_id,
            "messages": messages,
        }
        if response_format:
            payload["response_format"] = response_format
        response = requests.post(
            f"{self.base_url}chat/completions", headers=headers, json=payload
        )
        try:
            return response.json()["choices"][0]["message"]["content"]
        except:
            return {}
