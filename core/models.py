from django.db import models


class DeviceType(models.Model):
    name = models.CharField(max_length=200)
    variables = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Device(models.Model):
    DEVICE_TYPE = (
        (0, 'READ'),
        (1, 'WRITE'),
        (2, 'READ/WRITE'),
    )
    created = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(db_index=True)
    type = models.SmallIntegerField(choices=DEVICE_TYPE, default=0)
    device_type = models.ForeignKey(DeviceType, blank=True, null=True, default=None)
    description = models.TextField(max_length=200, blank=True, null=True, default=None)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.ip


class Rule(models.Model):
    RULE_TYPE = (
        (0, 'Any'),
        (1, 'All'),
    )
    name = models.CharField(max_length=200)
    condition_type = models.PositiveSmallIntegerField(choices=RULE_TYPE, default=1)
    enabled = models.BooleanField(default=False)
    running = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Condition(models.Model):
    CONDITION_TYPE = (
        (0, 'Contains'),
        (1, 'Matches exactly'),
        (2, 'Does not contain'),
        (10, 'Is greater (int or float)'),
        (11, 'Is greater or equal (int or float)'),
        (12, 'Is lower (int or float)'),
        (13, 'Is lower or equal (int or float)'),
        (14, 'Is equal (int or float)'),
    )
    rule = models.ForeignKey(Rule)
    device = models.ForeignKey(Device, blank=True, null=True, default=None)
    value = models.CharField(max_length=200)

    def __str__(self):
        return self.value


class DeviceAction(models.Model):
    rule = models.ForeignKey(Rule)
    device = models.ForeignKey(Device)
    values = models.TextField()

    def __str__(self):
        return self.values


class SoftwareAction(models.Model):
    rule = models.ForeignKey(Rule)
    command = models.TextField()

    def __str__(self):
        return self.command
