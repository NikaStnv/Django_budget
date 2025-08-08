from django.db import models
from django.utils import timezone


class MixinsModel(models.Model):
    name = models.CharField(max_length=100)
    descriptions = models.TextField(blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
  

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Mixin Model"
        verbose_name_plural = "Mixin Models"
        ordering = ['-id']

