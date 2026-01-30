import uuid
from django.db import models
from django.conf import settings

class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='documents/')
    filename = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    VISIBILITY_CHOICES = [
        ('internal', 'Equipe Interna'),
        ('franchisee', 'Franqueados'),
    ]
    processed = models.BooleanField(default=False)
    content_hash = models.CharField(max_length=64, blank=True)
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='internal')
    
    def __str__(self):
        return self.filename
