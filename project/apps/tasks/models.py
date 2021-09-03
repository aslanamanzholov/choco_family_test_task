from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.const import TaskStatusChoice, PriorityChoice
from utils.models import AbstractUUID, AbstractTimeTrackable


class Task(AbstractUUID,
           AbstractTimeTrackable):
    name = models.CharField(
        _('name'),
        max_length=255,
        blank=True,
        null=True
    )
    priority = models.CharField(
        _('priority'),
        choices=PriorityChoice.choices(),
        default=PriorityChoice.LOW.value,
        max_length=6
    )
    end_date = models.DateTimeField(
        _('deadline'),
    )
    status = models.CharField(
        _('status'),
        choices=TaskStatusChoice.choices(),
        default=TaskStatusChoice.TODO.value,
        max_length=11
    )

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')

    def __str__(self):
        return f'Задача {self.name} со статусом {self.status} c приоритетом {self.priority}'

    def change_status(self, status):
        self.status = status
        self.save(update_fields=['status', 'updated_at'])
