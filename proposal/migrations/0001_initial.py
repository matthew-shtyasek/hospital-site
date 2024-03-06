# Generated by Django 4.2 on 2024-03-04 21:21

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
            name='Days',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название')),
                ('image', models.ImageField(upload_to='post/%Y/%m/%d/', verbose_name='Изображение')),
                ('fio', models.CharField(max_length=150, verbose_name='ФИО')),
                ('experience', models.IntegerField(verbose_name='Стаж')),
                ('category', models.CharField(max_length=150, verbose_name='Категория')),
                ('phone_number', models.CharField(max_length=11, verbose_name='Номер телефона')),
            ],
            options={
                'verbose_name': 'Врач',
                'verbose_name_plural': 'Врачи',
            },
        ),
        migrations.CreateModel(
            name='WorkSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_start', models.DateTimeField(verbose_name='Начало времени')),
                ('datetime_end', models.DateTimeField(verbose_name='Конец времени')),
            ],
        ),
        migrations.CreateModel(
            name='WorkDaysSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proposal.days', verbose_name='День')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proposal.post', verbose_name='Доктор')),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proposal.workschedule', verbose_name='График')),
            ],
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Ожидание', 'Ожидание'), ('Принято', 'Принято'), ('Отклонено', 'Отклонено')], default='Ожидание', max_length=9, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('visit_time', models.DateTimeField(verbose_name='Время посещения')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposals', to='proposal.post', verbose_name='Доктор')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Заявки',
                'ordering': ['-created_at'],
            },
        ),
    ]