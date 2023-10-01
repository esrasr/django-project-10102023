from django.db import models


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.PositiveSmallIntegerField(default=0)

    class Meta:
        abstract = True
