import random
from django.db import models
from django.contrib.auth import get_user_model
from core.models import BaseModel
from django.utils.translation import gettext_lazy as _
from apps.users.models import User
from apps.words.models.sentence import Sentence
from apps.words.models.topic import Topic
User=get_user_model()

class WordQuerySet(models.QuerySet):
    def words_by_date(self: models.Model, user: User) -> "WordQuerySet":
        """Get words ordered by date of creation."""
        return self.objects.filter(user=user).order_by("-created_at")

    def words_by_alphabet(self: models.Model, user: User) -> "WordQuerySet":
        """Get words ordered alphabetically."""
        return self.objects.filter(user=user).order_by("word")

    def words_reverce_alphabet(self: models.Model, user: User) -> "WordQuerySet":
        """Get words ordered in reverse alphabetically."""
        return self.objects.filter(user=user).order_by("-word")

    def random_word(self: models.Model, user: User) -> "WordQuerySet":
        """Get a random word."""
        return random.choice(self.objects.filter(user=user))

    def words_by_difficulty(
        self: models.Model, user: User, difficulty: str
    ) -> "WordQuerySet":
        """Get words by difficulty level."""
        return self.objects.filter(user=user, difficulty=difficulty)

    def words_sorted_by_difficulty(self: models.Model, user: User) -> "WordQuerySet":
        """Get words sorted by difficulty."""
        return self.objects.filter(user=user).order_by("difficulty")


WordManager = models.Manager.from_queryset(WordQuerySet)


class Word(BaseModel):
    class Difficulty(models.TextChoices):
        EASY = "1", _("Easy")
        MEDIUM = "2", _("Medium")
        HARD = "3", _("Hard")
        EXPERT = "4", _("Expert")
        MASTER = "5", _("Master")
        LEGENDARY = "6", _("Legendary")

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="words"
    )
    word = models.CharField(max_length=64, unique=True, blank=False)
    translate = models.CharField(max_length=64, blank=True)
    context = models.TextField(
        verbose_name=_("context"), default="The context from which the word is taken."
    )
    difficulty = models.CharField(
        verbose_name=_("difficulty"),
        max_length=1,
        choices=Difficulty.choices,
        blank=True,
    )

    objects = WordManager()

    class Meta:
        db_table = "vocabulary_words"
        verbose_name = _("word")
        verbose_name_plural = _("words")

    def __str__(self) -> str:
        if self.translate:
            return f"Word: {self.word} | Translate: {self.translate}"
        return self.word

    def add_to_topic(self, topic: Topic):
        """Add the word to the specified topic."""
        topic.add_word(self)

    def remove_from_topic(self, topic: Topic):
        """Remove the word from the specified topic."""
        topic.remove_word(self)

    def add_sentence(self, text):
        """Add a sentence to the word."""
        return Sentence.objects.create(word=self, text=text)

    def remove_sentence(self, sentence_id):
        """Remove a sentence from the word."""
        Sentence.objects.filter(word=self, id=sentence_id).delete()

    def get_sentences(self):
        """Get all sentences associated with the word."""
        return self.sentences.all()

    def get_random_sentence(self):
        """Get a random sentence associated with the word."""
        return Sentence.objects.random_sentence(user=self)