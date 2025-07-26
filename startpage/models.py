from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

User = get_user_model()


class ContactMessage(models.Model):
    """Сохраняет сообщения, отправленные через форму контактов."""
    name = models.CharField("Имя", max_length=100)
    email = models.EmailField("Email")
    subject = models.CharField("Тема", max_length=255, blank=True)
    message = models.TextField("Сообщение")
    created_at = models.DateTimeField("Дата отправки", auto_now_add=True)

    class Meta:
        verbose_name = "Сообщение контактов"
        verbose_name_plural = "Сообщения контактов"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.subject[:50] if self.subject else self.message[:50]}"

