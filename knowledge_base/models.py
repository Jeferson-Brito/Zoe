from django.db import models
from django.conf import settings

class Document(models.Model):
    VISIBILITY_CHOICES = (
        ('internal', 'Interno'),
        ('franchisee', 'Franqueado'),
        ('customer', 'Cliente'),
    )
    
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    processed = models.BooleanField(default=False)
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='internal')
    
    def __str__(self):
        return f"{self.file.name} - {self.uploaded_at}"

class LearnedKnowledge(models.Model):
    """Conhecimento aprendido durante conversas no chat"""
    title = models.CharField(max_length=255, help_text="Título resumido do conhecimento")
    content = models.TextField(help_text="O que foi aprendido")
    source = models.CharField(max_length=50, default='chat', help_text="Origem: chat, manual, etc")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True, help_text="Se False, não será usado nas respostas")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Conhecimento Aprendido'
        verbose_name_plural = 'Conhecimentos Aprendidos'
    
    def __str__(self):
        return f"{self.title} ({self.created_at.strftime('%d/%m/%Y')})"
