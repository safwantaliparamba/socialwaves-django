from django.db import models

from general.models import BaseModel
from accounts.models import User


class Notification(BaseModel):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=128, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    model_id = models.UUIDField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=True)

    class Meta:
        db_table = 'notifications_notification'
        verbose_name = 'notification'
        verbose_name_plural = 'notifications'
        ordering = ('-date_added',)

    def __str__(self):
        return str(self.sender)