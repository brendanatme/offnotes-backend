from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("notes", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="folder",
            name="user",
            field=models.ForeignKey(
                to=settings.AUTH_USER_MODEL,
                related_name="folders",
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                help_text="The user this folder belongs to",
            ),
        ),
        migrations.AddField(
            model_name="note",
            name="user",
            field=models.ForeignKey(
                to=settings.AUTH_USER_MODEL,
                related_name="notes",
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                help_text="The user this note belongs to",
            ),
        ),
    ]
