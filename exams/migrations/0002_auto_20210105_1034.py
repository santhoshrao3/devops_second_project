# Generated by Django 3.1.5 on 2021-01-05 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='is_correct',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='questions',
            name='option1',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='questions',
            name='option2',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='questions',
            name='option3',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.DeleteModel(
            name='Answers',
        ),
    ]
