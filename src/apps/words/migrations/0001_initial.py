# Generated by Django 5.0 on 2024-01-04 20:32

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Topic",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("date_added", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ("-date_added",),
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Word",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("date_added", models.DateTimeField(auto_now_add=True)),
                ("word", models.CharField(max_length=64, unique=True)),
                ("translate", models.CharField(blank=True, max_length=64)),
                (
                    "context",
                    models.TextField(
                        default="The context from which the word is taken.",
                        verbose_name="context",
                    ),
                ),
                (
                    "difficulty",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("1", "Easy"),
                            ("2", "Medium"),
                            ("3", "Hard"),
                            ("4", "Expert"),
                            ("5", "Master"),
                            ("6", "Legendary"),
                        ],
                        max_length=1,
                        verbose_name="difficulty",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="words",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "word",
                "verbose_name_plural": "words",
                "db_table": "vocabulary_words",
            },
        ),
        migrations.CreateModel(
            name="TopicWord",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("date_added", models.DateTimeField(auto_now_add=True)),
                (
                    "topic",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="words.topic"
                    ),
                ),
                (
                    "word",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="words.word"
                    ),
                ),
            ],
            options={
                "ordering": ("-date_added",),
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="topic",
            name="words",
            field=models.ManyToManyField(
                related_name="topics", through="words.TopicWord", to="words.word"
            ),
        ),
        migrations.CreateModel(
            name="Sentence",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("date_added", models.DateTimeField(auto_now_add=True)),
                ("text", models.TextField(verbose_name="text")),
                (
                    "word",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sentences",
                        to="words.word",
                    ),
                ),
            ],
            options={
                "ordering": ("-date_added",),
                "abstract": False,
            },
        ),
    ]