# Generated by Django 4.0.1 on 2022-01-13 19:22

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DFSong',
            fields=[
                ('id', models.CharField(max_length=250, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=1000)),
                ('artist', models.CharField(default='', max_length=1000)),
                ('songUrl', models.URLField()),
                ('imageUrl', models.URLField()),
                ('lyric', models.TextField()),
                ('likes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='SongEmbedding',
            fields=[
                ('song_id', models.CharField(max_length=250, primary_key=True, serialize=False)),
                ('embedding', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(default=0), size=None)),
            ],
        ),
        migrations.CreateModel(
            name='RecommendedSong',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recommends_songs_id', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=250), size=None), size=None)),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='songsapi.dfsong')),
            ],
        ),
    ]
