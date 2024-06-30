import json
import os
from mistralai.client import MistralClient
from mistralai.models.jobs import TrainingParameters
from config import config
from models import Chat, Model, FinetuneJob
from db import connect_to_db
import random

connect_to_db(config.get("Application", "DB"))

# # Set up the Mistral client
client = MistralClient(api_key=config.get("Mistral", "API_KEY"))


def format_chat_data(chat):
    formatted_data = []
    for message in chat.messages:
        formatted_data.append(
            {
                "messages": [
                    {"role": "user", "content": message.user_message},
                    {"role": "assistant", "content": message.agent_message},
                ]
            }
        )
    return formatted_data


def get_formatted_chats():
    chat = Chat.objects.first()
    all_formatted_data = format_chat_data(chat)
    return all_formatted_data


def upload_data_to_mistral(
    formatted_data, chat_file="chat.jsonl", file_name="finetune.jsonl"
):
    # Read chat.jsonl and append its data to formatted_data
    with open(chat_file, "r") as f:
        for line in f:
            formatted_data.append(json.loads(line))

    # Randomly shuffle the combined data
    random.shuffle(formatted_data)

    # Write shuffled data to JSONL file
    with open(file_name, "w") as f:
        for line in formatted_data:
            json.dump(line, f)
            f.write("\n")

    # Upload the file
    with open(file_name, "rb") as f:
        jsonl_data = client.files.create(file=(file_name, f))

    return jsonl_data


def create_finetuning_job(jsonl_data):
    created_jobs = client.jobs.create(
        model="open-mistral-7b",
        training_files=[jsonl_data.id],
        hyperparameters=TrainingParameters(
            training_steps=10,
            learning_rate=0.0001,
        ),
    )
    FinetuneJob(finetune_job_id=created_jobs.id).save()
    return created_jobs


finetune_job = FinetuneJob.objects().first()
if finetune_job is None or finetune_job.finetune_job_id is None:
    data = get_formatted_chats()
    if data != []:
        create_finetuning_job(upload_data_to_mistral(data))
else:
    finetune_job_id = finetune_job.finetune_job_id
    retrieved_jobs = client.jobs.retrieve(finetune_job_id)
    if retrieved_jobs.status=="SUCCESS":
        model = Model.get_instance()
        model.update(
            set__model_id =retrieved_jobs.fine_tuned_model
        )
        FinetuneJob.objects.delete()
