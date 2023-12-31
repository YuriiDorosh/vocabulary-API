from django.contrib import admin

from apps.words.models import Sentence, Topic, TopicWord, Word


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    pass


@admin.register(Sentence)
class SentenceAdmin(admin.ModelAdmin):
    pass


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass


@admin.register(TopicWord)
class TopicWordAdmin(admin.ModelAdmin):
    pass
