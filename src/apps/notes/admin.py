from django.contrib import admin

from apps.notes.models import Note, Pause


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    pass


@admin.register(Pause)
class PauseAdmin(admin.ModelAdmin):
    pass
