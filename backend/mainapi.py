from fastapi import FastAPI
from typing import Annotated
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from config import config
from models import Model, Message, Chat
from middleware import custom_middleware
from pydantic_models import ChatPydanticModel
from chatbot import MistralModel
from survey import NPI40Survey
from db import connect_to_db
from fill_out_survey import generate_model_npi40_score


class Application:
    def __init__(self, app, middleware, db_uri, cors_origins):
        self.app = app
        self.middleware = middleware
        self.db_uri = db_uri
        self.cors_origins = cors_origins

    def build_application(self):
        self.app.middleware("http")(self.middleware)
        self.app.middleware("https")(self.middleware)
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=self.cors_origins,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        connect_to_db(self.db_uri)
        return self

    def add_routes(self):
        @self.app.get("/")
        async def sanity_check():
            """
            Health check endpoint to ensure the service is up and running.
            """
            return {"message": "Service is up!"}

        @self.app.post("/chat")
        async def chat(chat: ChatPydanticModel):
            model_instance = Model.get_instance()
            mistral_model = MistralModel(
                config.get("Mistral", "API_KEY"), model_instance.model_id
            )
            chat_instance = Chat.objects.first() or Chat()

            # Prepare the messages for the API call
            messages = []
            for msg in chat_instance.messages[:10]:
                messages.append({"role": "user", "content": msg.user_message})
                messages.append({"role": "assistant", "content": msg.agent_message})
            messages.append({"role": "user", "content": chat.prompt})

            # Get the completion from the Mistral model
            response = mistral_model.get_completion(messages, response_format=None)

            # Create a new Message and add it to the chat
            new_message = Message(user_message=chat.prompt, agent_message=response)
            chat_instance.messages.append(new_message)
            chat_instance.save()

            return {"response": response}

        @self.app.get("/npi_score")
        async def fetch_npi_score():
            model_instance = Model.get_instance()
            mistral_model = MistralModel(
                config.get("Mistral", "API_KEY"), model_instance.model_id
            )
            survey = NPI40Survey()
            score, anwsered_ques = generate_model_npi40_score(mistral_model, survey)
            return {"score": score, "anwsered_ques": anwsered_ques}

        return self

    def get_app(self):
        return self.app


app = (
    Application(
        FastAPI(),
        custom_middleware,
        config.get("Application", "DB"),
        ["*"],
    )
    .build_application()
    .add_routes()
    .get_app()
)

if __name__ == "__main__":
    uvicorn.run("mainapi:app", reload=True)
