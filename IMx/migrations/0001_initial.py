# Generated by Django 4.2.6 on 2023-10-28 01:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="HistoricalCount",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("tag", models.CharField(max_length=50)),
                ("subinv", models.CharField(max_length=50)),
                ("location", models.CharField(max_length=50)),
                ("uom", models.CharField(max_length=20)),
                ("quantity", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Pending Count", "Pending Count"),
                            ("Pending Review", "Pending Review"),
                            ("Completed", "Completed"),
                        ],
                        default="Pending Count",
                        max_length=15,
                    ),
                ),
                (
                    "first_count",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=30, null=True
                    ),
                ),
                (
                    "second_count",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=30, null=True
                    ),
                ),
                (
                    "third_count",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=30, null=True
                    ),
                ),
                (
                    "fourth_count",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=30, null=True
                    ),
                ),
                (
                    "fifth_count",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=30, null=True
                    ),
                ),
                ("created_time", models.DateTimeField(blank=True, editable=False)),
                ("last_modified", models.DateTimeField(blank=True, editable=False)),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "assigned_to",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "historical count",
                "verbose_name_plural": "historical counts",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="Count",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("tag", models.CharField(max_length=50)),
                ("subinv", models.CharField(max_length=50)),
                ("location", models.CharField(max_length=50)),
                ("uom", models.CharField(max_length=20)),
                ("quantity", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Pending Count", "Pending Count"),
                            ("Pending Review", "Pending Review"),
                            ("Completed", "Completed"),
                        ],
                        default="Pending Count",
                        max_length=15,
                    ),
                ),
                (
                    "first_count",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=30, null=True
                    ),
                ),
                (
                    "second_count",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=30, null=True
                    ),
                ),
                (
                    "third_count",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=30, null=True
                    ),
                ),
                (
                    "fourth_count",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=30, null=True
                    ),
                ),
                (
                    "fifth_count",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=30, null=True
                    ),
                ),
                ("created_time", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                (
                    "assigned_to",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="assigned_counts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="counts_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
