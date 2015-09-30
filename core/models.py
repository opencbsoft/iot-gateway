from django.db import models


class Device(models.Model):
    DEVICE_TYPE = (
        (0, 'READ'),
        (1, 'WRITE'),
        (2, 'READ/WRITE'),
    )
    created = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(db_index=True)
    type = models.SmallIntegerField(choices=DEVICE_TYPE, default=0)
    description = models.TextField(max_length=200, blank=True, null=True, default=None)
    enabled = models.BooleanField(default=True)
    action_file = models.CharField(max_length=200, blank=True, null=True, default=None)

    def __str__(self):
        return self.ip

