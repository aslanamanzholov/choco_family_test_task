from enum import Enum

from django.utils.translation import ugettext_lazy as _


class Choice(Enum):
    @classmethod
    def choices(cls):
        return [(c.value, _(c.name)) for c in cls]

    @classmethod
    def repr(cls):
        return {c.name: {'id': c.value, 'name': _(c.name)} for c in cls}

    @classmethod
    def list(cls):
        return [c.value for c in cls]

    def __str__(self):
        return self.value


class GenderChoice(str, Choice):
    MALE = 'MALE'
    FEMALE = 'FEMALE'


class TaskStatusChoice(str, Choice):
    TODO = 'TODO'
    IN_PROGRESS = 'IN_PROGRESS'
    DONE = 'DONE'


class PriorityChoice(str, Choice):
    LOW = '1'
    MEDIUM = '2'
    HIGH = '3'
