
from django.db import models
from core.models import BaseModel
from django.utils.translation import gettext_lazy as _
from apps.words.models.word import Word


class Topic(BaseModel):
    name = models.CharField(max_length=64, unique=True, blank=False)
    words = models.ManyToManyField(Word, through="TopicWord", related_name="topics")

    def add_word(self, word):
        """Add a word to the topic."""
        TopicWord.objects.create(topic=self, word=word)

    def remove_word(self, word):
        """Remove a word from the topic."""
        TopicWord.objects.filter(topic=self, word=word).delete()

    def get_words_by_difficulty(self, difficulty: str) -> Word:
        """Get words from the topic by difficulty level."""
        return self.words.filter(difficulty=difficulty)

    def __str__(self) -> str:
        return f"Topic: {self.words.all()}"


class TopicWord(BaseModel):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Topic: {self.topic}, Word: {self.word}"
