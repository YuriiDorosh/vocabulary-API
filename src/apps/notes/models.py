import random

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel

User = get_user_model()


class NoteQuerySet(models.QuerySet):
    def notes_by_date(self, user: User) -> "NoteQuerySet":
        """Get notes ordered by date of creation."""
        return self.filter(user=user).order_by("-created_at")

    def notes_by_resource(self, user: User) -> "NoteQuerySet":
        """Get notes ordered by resource."""
        return self.filter(user=user).order_by("resource")

    def random_note(self, user: User) -> "NoteQuerySet":
        """Get a random note."""
        return random.choice(self.filter(user=user))


NoteManager = models.Manager.from_queryset(NoteQuerySet)


class Note(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    title = models.CharField(_("title"), max_length=64, unique=True, blank=False)
    resource = models.CharField(_("resource"), max_length=64, blank=False)

    objects = NoteManager()

    class Meta:
        db_table = "vocabulary_notes"
        verbose_name = _("note")
        verbose_name_plural = _("notes")

    def __str__(self) -> str:
        return self.title


class PauseQuerySet(models.QuerySet):
    def pauses_by_place(self, note_id: int) -> "PauseQuerySet":
        """Get pauses for a specific note ordered by place."""
        return self.filter(note_id=note_id).order_by("place")


PauseManager = models.Manager.from_queryset(PauseQuerySet)


class Pause(BaseModel):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name="pauses")
    place = models.CharField(_("place"), max_length=64, blank=False)
    description = models.TextField(_("description"), blank=True)

    objects = PauseManager()

    class Meta:
        db_table = "vocabulary_pauses"
        verbose_name = _("pause")
        verbose_name_plural = _("pauses")

    def __str__(self) -> str:
        return f"Pause for {self.note.title}"
