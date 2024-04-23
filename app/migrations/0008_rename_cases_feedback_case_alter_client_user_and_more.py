# Generated by Django 4.2.11 on 2024-04-23 12:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0007_alter_client_user_alter_lawyer_user_feedback'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedback',
            old_name='cases',
            new_name='case',
        ),

        migrations.AlterField(
            model_name='feedback',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback', to='app.client'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='lawyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback', to='app.lawyer'),
        ),

    ]
