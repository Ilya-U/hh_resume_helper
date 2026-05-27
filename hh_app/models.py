from django.db import models
from django.utils.translation import gettext_lazy as _


class Resume(models.Model):
    class Status(models.TextChoices):
        SUBMITTED = 'submitted', _('Заявка поступила')
        PROCESSING = 'processing', _('В обработке')
        PROCESSED = 'processed', _('Обработана')
        REJECTED = 'rejected', _('Отказано')
        APPROVED = 'approved', _('Одобрено')

    applicant_name = models.CharField(
        max_length=255,
        verbose_name=_('Имя подающего')
    )
    position = models.CharField(
        max_length=255,
        verbose_name=_('Должность')
    )
    email = models.EmailField(
        verbose_name=_('Почта')
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SUBMITTED,
        verbose_name=_('Статус')
    )
    resume_file = models.FileField(
        upload_to='resumes/%Y/%m/%d/',
        verbose_name=_('Резюме (PDF)')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления')
    )

    class Meta:
        verbose_name = _('Резюме')
        verbose_name_plural = _('Резюме')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.applicant_name} — {self.position}'

    def get_status_display_color(self):
        colors = {
            self.Status.SUBMITTED: 'secondary',
            self.Status.PROCESSING: 'info',
            self.Status.PROCESSED: 'primary',
            self.Status.REJECTED: 'danger',
            self.Status.APPROVED: 'success',
        }
        return colors.get(self.status, 'secondary')