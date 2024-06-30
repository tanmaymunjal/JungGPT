import json
import os
from mistralai.client import MistralClient
from mistralai.models.jobs import TrainingParameters
from config import config
from models import Model
from db import connect_to_db

# # Load the original JSON data
# with open('train.json', 'r') as f:
#     data = json.load(f)

# # Prepare the data in the new format
# formatted_data = []
# for item in data['items']:
#     text = item["item"].split(".",maxsplit=1)[1]
#     formatted_data .append({
#         "messages": [
#             {
#                 "role": "user",
#                 "content": f"Do you feel that {text}"
#             },
#             {
#                 "role": "assistant",
#                 "content": f"Yes, I feel that {text}"
#             }
#         ]
#     })

# # Write data to JSON file
# with open('chat.jsonl', 'w') as f:
#     for line in formatted_data:
#         json.dump(line, f)
#         f.write("\n")

# # Set up the Mistral client
client = MistralClient(api_key=config.get("Mistral", "API_KEY"))

# # Upload the file
# with open("chat.jsonl", "rb") as f:
#     ultrachat_data = client.files.create(file=("chat.jsonl", f))

# # Create the fine-tuning job
# created_jobs = client.jobs.create(
#     model="open-mistral-7b",
#     training_files=[ultrachat_data.id],
#     hyperparameters=TrainingParameters(
#         training_steps=10,
#         learning_rate=0.0001,
#     )
# )

# print(created_jobs)
connect_to_db(config.get("Application", "DB"))
Model().save()
