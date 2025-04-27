# tribes/models.py
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class People(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    description = models.TextField()
    culture = models.JSONField()
    images = models.JSONField()
    language = models.CharField(max_length=50)
    traditions = models.TextField()
    audio = models.TextField()
    history = models.TextField(blank=True, null=True)# Добавляем новое поле для истории

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    people = models.ForeignKey(People, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'people')  # Пользователь не может добавить одну культуру дважды

    def __str__(self):
        return f"{self.user.username} - {self.people.name}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    people = models.ForeignKey(People, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.people.name}"