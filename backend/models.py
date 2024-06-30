from mongoengine import (
    Document,
    IntField,
    StringField,
    EmbeddedDocument,
    ListField,
    EmbeddedDocumentListField,
    EmbeddedDocumentField,
)
from datetime import datetime

NARCISSIST_MODEL = "ft:open-mistral-7b:bf1a70be:20240630:9fbc9c74"


class Model(Document):
    model_id = StringField(required=True, default=NARCISSIST_MODEL)

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                existing_instance = Model.objects.get()
                self.pk = existing_instance.pk
            except DoesNotExist:
                pass
        return super(Model, self).save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        try:
            return cls.objects.get()
        except DoesNotExist:
            return cls()


class Message(EmbeddedDocument):
    user_message = StringField(required=True)
    agent_message = StringField(required=True)


class Chat(Document):
    messages = EmbeddedDocumentListField(Message, default=[])
    chat_index = IntField()

class FinetuneJob(Document):
    finetune_job_id = StringField()