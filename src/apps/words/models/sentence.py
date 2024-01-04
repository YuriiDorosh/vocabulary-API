import random
from django.db import models
from core.models import BaseModel
from django.utils.translation import gettext_lazy as _
from apps.users.models import User
from apps.words.models.word import Word


class SentenceQuerySet(models.QuerySet):
    def random_sentence(self, user: User) -> "SentenceQuerySet":
        """Get a random sentence."""
        return random.choice(self.objects.filter(word__user=user))


SentenceManager = models.Manager.from_queryset(SentenceQuerySet)


class Sentence(BaseModel):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name="sentences")
    text = models.TextField(verbose_name=_("text"), blank=False)

    objects = SentenceManager()

    def __str__(self) -> str:
        return f"Sentence: {self.text}"
