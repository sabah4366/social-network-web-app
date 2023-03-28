# Generated by Django 4.1.2 on 2023-03-27 17:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('profile_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('bio', models.CharField(blank=True, max_length=250, null=True)),
                ('phone_no', models.IntegerField(blank=True, max_length=10, null=True, unique=True)),
                ('profile_pic', models.ImageField(default='profile/photos/profile.png', upload_to='profile/photos')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]