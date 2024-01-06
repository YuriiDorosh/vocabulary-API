import random

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.models import User
from core.models import BaseModel

User = get_user_model()


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

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="words")
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

    def add_to_topic(self, topic: 'Topic'):
        """Add the word to the specified topic."""
        topic.add_word(self)

    def remove_from_topic(self, topic: 'Topic'):
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

    class Meta:
        db_table = "vocabulary_topics"
        verbose_name = _("topic")
        verbose_name_plural = _("topics")

    def __str__(self) -> str:
        words_list = self.words.values_list('word', flat=True)
        words_str = ', '.join(words_list) if words_list else ''
        return f"Topic: '{self.name}', Words: '{words_str}'"


class TopicWord(BaseModel):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)

    class Meta:
        db_table = "vocabulary_topic_word"
        verbose_name = _("topic_word")
        verbose_name_plural = _("topics_words")

    def __str__(self) -> str:
        if self.word:
            return f"Topic: {self.topic}, Word: {self.word}"
        return f"Topic: {self.topic} without words"
    
class SentenceQuerySet(models.QuerySet):
    def random_sentence(self, user: User) -> "SentenceQuerySet":
        """Get a random sentence."""
        return random.choice(self.objects.filter(word__user=user))


SentenceManager = models.Manager.from_queryset(SentenceQuerySet)


class Sentence(BaseModel):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name="sentences")
    text = models.TextField(verbose_name=_("text"), blank=False)

    objects = SentenceManager()

    class Meta:
        db_table = "vocabulary_sentences"
        verbose_name = _("sentence")
        verbose_name_plural = _("sentences")

    def __str__(self) -> str:
        return f"Sentence: '{self.text}'"