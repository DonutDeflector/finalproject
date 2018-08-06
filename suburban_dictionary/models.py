from django.conf import settings
from django.db import models


# Create your models here.

class Term(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Definition(models.Model):
    term = models.ForeignKey(
        Term, on_delete=models.CASCADE, related_name="term")
    definition = models.TextField()
    example = models.TextField()
    username = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)
    likes = models.PositiveIntegerField(default=0)
    liked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="liked")
    dislikes = models.PositiveIntegerField(default=0)
    disliked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="disliked")

    class Meta:
        ordering = ["term"]

    def __str__(self):
        return f"{self.term}"
