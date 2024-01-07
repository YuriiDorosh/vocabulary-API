from django.db import models

from core.models import BaseModel
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

User = get_user_model()

# TODO: QuerySet

class TodoGroup(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todogroups")
    title = models.CharField(_("title"), max_length=64, unique=True, blank=False)
    
    class Meta:
        db_table = "vocabulary_todogroups"
        verbose_name = _("todogroup")
        verbose_name_plural = _("todogroups")
        
    def count(self):
        return self.todos.count()
    
    
    def count_finished(self):
        return self.todos.filter(is_finished=True).count()
    
    def count_open(self):
        return self.todos.filter(is_finished=False).count()

# TODO: QuerySet

class Todo(BaseModel):
    class Importance(models.TextChoices):
        INDIFFERENTLY = "1", _("Indifferently")
        LATER = "2", _("Later")
        HARD = "3", _("Hard") # TODO
        EXPERT = "4", _("Expert") # TODO
        MASTER = "5", _("Master") # TODO
        LEGENDARY = "6", _("Legendary") # TODO
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todos")
    group = models.ForeignKey(TodoGroup, on_delete=models.SET_NULL, related_name="todos")
    title = models.CharField(_("title"), max_length=64, unique=True, blank=False)
    is_finished = models.BooleanField(default=False)
    finished_at = models.DateTimeField(null=True)
    importance = models.CharField(
        verbose_name=_("difficulty"),
        max_length=1,
        choices=Importance.choices,
        blank=True,
    )
    
    class Meta:
        db_table = "vocabulary_todos"
        verbose_name = _("todo")
        verbose_name_plural = _("todos")
        
    
    def __str__(self) -> str:
        return f"Todo: {self.title}"
    
    def close(self):
        self.is_finished = True
        self.finished_at = timezone.now()
        self.save()
        
    def reopen(self):
        self.is_finished = False
        self.finished_at = None
        self.save()
    
    