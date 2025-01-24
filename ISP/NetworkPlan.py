from django.db import models

class ServicePlanManagement(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('canceled', 'Canceled'),
    ]

    plan_name = models.CharField(max_length=200, default="Basic Plan")
    speed = models.PositiveIntegerField(help_text="Speed in Mbps")
    data_limit = models.PositiveIntegerField(help_text="Data limit in GB")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=200, null=False, blank=True)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default='inactive')