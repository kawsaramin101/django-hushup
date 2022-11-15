import uuid 
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class ReadMessageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(read=True, soft_deleted=False)


class UnReadMessageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(read=False, soft_deleted=False)


class SoftDeletedMessageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(soft_deleted=True)



class Message(models.Model):
    
    secondary_id = models.UUIDField(default=uuid.uuid4, editable=False)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="posts", null=False, blank=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    created = models.DateTimeField()
    read = models.BooleanField(default=False)
    soft_deleted = models.BooleanField(default=False)
    
    objects = models.Manager()
    read_objs = ReadMessageManager()
    unread_objs = UnReadMessageManager()
    soft_deleted_objs = SoftDeletedMessageManager()
     
    class Meta:
        ordering = ["read", "-created"]
   
    def __str__(self):
        return self.title or self.body
    