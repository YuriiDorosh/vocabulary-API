import random
from django.db import models
from django.contrib.auth import get_user_model
from core.models import BaseModel
from django.utils.translation import gettext_lazy as _
from apps.users.models import User


class WordQuerySet(models.QuerySet):
    def words_by_date(self: models.Model, user: User) -> "WordQuerySet":
        return self.objects.filter(user=user).order_by("-created_at")

    def words_by_alphabet(self: models.Model, user: User) -> "WordQuerySet":
        return self.objects.filter(user=user).order_by("word")

    def words_reverce_alphabet(self: models.Model, user: User) -> "WordQuerySet":
        return self.objects.filter(user=user).order_by("-word")

    def random_word(self: models.Model, user: User) -> "WordQuerySet":
        return random.choice(self.objects.filter(user=user))

    def words_by_difficulty(
        self: models.Model, user: User, diffuculty: str
    ) -> "WordQuerySet":
        return self.objects.filter(user=user, diffuculty=diffuculty)

    def words_sorted_by_difficulty(self: models.Model, user: User) -> "WordQuerySet":
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
        User=get_user_model(), on_delete=models.CASCADE, related_name="words"
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
    
    def add_to_topic(self, topic: 'Topic'):
        topic.add_word(self)

    def remove_from_topic(self, topic: 'Topic'):
        topic.remove_word(self)
        
    def add_sentence(self, text):
        return Sentence.objects.create(word=self, text=text)

    def remove_sentence(self, sentence_id):
        Sentence.objects.filter(word=self, id=sentence_id).delete()

    def get_sentences(self):
        return self.sentences.all()
    
    def get_random_sentence(self):
        return Sentence.random_sentence(user=self)


class SentenceQuerySet(models.QuerySet):
    def random_sentence(self, user: User) -> "SentenceQuerySet":
        return random.choice(self.objects.filter(word__user=user))

SentenceManager = models.Manager.from_queryset(SentenceQuerySet)

class Sentence(BaseModel):
    word = models.ForeignKey(
        Word,  on_delete=models.CASCADE, related_name="sentences"
    )
    text = models.TextField(verbose_name=_("text"), blank=False)
    
    objects = SentenceManager()
    
    def __str__(self) -> str:
        return f"Sentence: {self.text}"
    

class Topic(BaseModel):
    words = models.ManyToManyField(Word, through='TopicWord', related_name="topics")
    
    def add_word(self, word):
        TopicWord.objects.create(topic=self, word=word)
    
    def remove_word(self, word):
        TopicWord.objects.filter(topic=self, word=word).delete()
        
    def get_words_by_difficulty(self, difficulty: str) -> "QuerySet[Word]":
        return self.words.filter(difficulty=difficulty)
    
    def __str__(self) -> str:
        return f"Topic: {self.words.all()}"

class TopicWord(BaseModel):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"Topic: {self.topic}, Word: {self.word}"
    