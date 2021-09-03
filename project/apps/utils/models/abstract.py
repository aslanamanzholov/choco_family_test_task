from uuid import uuid4
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from utils.const import GenderChoice, TaskStatusChoice
from utils.managers import SoftDeletionManager


class AbstractUUID(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid4,
        verbose_name=_('uuid')
    )

    class Meta:
        abstract = True
        ordering = ('uuid',)


class AbstractTimeTrackable(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата изменения')
    )

    class Meta:
        abstract = True
        ordering = ('created_at', 'updated_at')


class AbstractUserModel(models.Model):
    first_name = models.CharField(
        _('first name'),
        max_length=126
    )
    last_name = models.CharField(
        _('last name'),
        max_length=126
    )
    middle_name = models.CharField(
        _('middle name'),
        max_length=126,
        blank=True,
        null=True
    )
    gender = models.CharField(
        _('gender'),
        choices=GenderChoice.choices(),
        max_length=6,
        blank=True,
        null=True
    )
    birth_date = models.DateField(
        _('Date of Birth'),
        blank=True,
        null=True
    )

    class Meta:
        abstract = True

    @property
    def age(self):
        if not self.birth_date:
            return 0
        result = timezone.localdate() - self.birth_date
        return int(result.days / 365.2425)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.last_name, self.first_name, self.middle_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name


class AbstractCreatedByTrackable(models.Model):
    created_by = models.ForeignKey(
        'users.User',
        verbose_name=_("Кем создан"),
        related_name="%(app_label)s_%(class)s_created_by",
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True


class Status(AbstractCreatedByTrackable, AbstractTimeTrackable, models.Model):
    id = models.CharField(
        primary_key=True,
        choices=TaskStatusChoice.choices(),
        max_length=30
    )
    name = models.CharField(
        _("name"),
        max_length=150
    )

    class Meta:
        verbose_name = _("status")
        verbose_name_plural = _("statuses")

    def __str__(self):
        return self.name


class AbstractStatusAddModel(models.Model):
    status = models.ForeignKey(
        'utils.Status',
        verbose_name=_('statuses'),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class AbstractTimeControlModel(models.Model):
    plan_start_at = models.DateTimeField(
        _('plan_start_date'),
        null=True,
        blank=True
    )
    plan_end_at = models.DateTimeField(
        _('plan_end_date'),
        null=True,
        blank=True)
    fact_start_at = models.DateTimeField(
        _('fact_start_date'),
        null=True,
        blank=True
    )
    fact_end_at = models.DateTimeField(
        _('fact_end_date'),
        null=True,
        blank=True
    )

    class Meta:
        abstract = True


class AbstractRemindControlModel(models.Model):
    remind_start_at = models.DateTimeField(_('remind_start_at'), blank=True, null=True)
    remind_end_at = models.DateTimeField(_('remind_end_at'), blank=True, null=True)

    class Meta:
        abstract = True


class AbstractFakeDeleteModel(models.Model):
    deleted = models.BooleanField(_('deleted'), default=False)

    class Meta:
        abstract = True

    def fake_delete(self):
        if self.deleted:
            raise ValueError('Already deleted.')
        self.deleted = True
        self.save(update_fields=['deleted'])


class AbstractSoftDeletionModel(models.Model):
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super(AbstractSoftDeletionModel, self).delete()
