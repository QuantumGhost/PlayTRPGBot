from enum import Enum, auto

from django.db import models


class LogKind(Enum):
    NORMAL = auto()
    DICE = auto()
    DESC = auto()
    SYSTEM = auto()
    ME = auto()
    ROLL = auto()
    HIDE_DICE = auto()


class VariableKind(Enum):
    NUM = auto()
    STR = auto()


def choice(enum):
    return [(kind.value, kind.name) for kind in enum]


class Chat(models.Model):
    chat_id = models.BigIntegerField('Chat ID', db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=256)
    parent = models.ForeignKey('Chat', on_delete=models.CASCADE, null=True, default=None)
    description = models.TextField()
    save_date = models.DateTimeField(null=True)
    recording = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Log(models.Model):
    user_id = models.BigIntegerField('User ID')
    message_id = models.BigIntegerField('Message ID')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, db_index=True)
    user_fullname = models.CharField('User Full Name', max_length=128, blank=True)
    character_name = models.CharField('Character', max_length=128, blank=True)
    kind = models.IntegerField(choices=choice(LogKind), default=LogKind.NORMAL.value)
    content = models.TextField()
    media = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True)
    gm = models.BooleanField('GM', default=False)
    reply = models.ForeignKey('Log', on_delete=models.SET_NULL, null=True)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField()
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        name = self.character_name or self.user_fullname or 'SYSTEM'
        return '{} - {} - {}'.format(self.chat.title, name, self.id)
