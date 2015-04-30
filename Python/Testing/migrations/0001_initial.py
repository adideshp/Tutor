# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('creation_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Free_Radicals',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(max_length=30)),
                ('creation_time', models.DateTimeField(auto_now=True)),
                ('class_associated', models.ForeignKey(to='Testing.Class')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_text', models.CharField(max_length=300)),
                ('explanation', models.CharField(max_length=100)),
                ('options', models.CharField(max_length=200)),
                ('hint', models.CharField(max_length=100)),
                ('difficulty', models.CharField(max_length=100)),
                ('points', models.IntegerField()),
                ('creation_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question_Summary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_taken', models.IntegerField(default=0)),
                ('attempted', models.BooleanField(default=False)),
                ('correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(related_name='Question_Solved_Summary', to='Testing.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('creation_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('test_name', models.CharField(max_length=50)),
                ('pass_criteria', models.IntegerField()),
                ('total_time', models.IntegerField(default=0)),
                ('creation_time', models.DateTimeField(auto_now=True)),
                ('assoicated_class', models.ForeignKey(related_name='Class_Test', to='Testing.Class')),
            ],
        ),
        migrations.CreateModel(
            name='Test_Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('test', models.ForeignKey(related_name='Test_Report', to='Testing.Test')),
            ],
        ),
        migrations.CreateModel(
            name='Test_Summary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_time', models.DateTimeField()),
                ('end_time', models.DateTimeField(auto_now=True)),
                ('marks_scored', models.IntegerField(default=0)),
                ('total_marks', models.IntegerField(default=0)),
                ('total_questions', models.IntegerField(default=0)),
                ('solved_count', models.IntegerField(default=0)),
                ('correct_count', models.IntegerField(default=0)),
                ('unsolved_count', models.IntegerField(default=0)),
                ('test', models.ForeignKey(related_name='Test_Solved_Summary', to='Testing.Test')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('creation_time', models.DateTimeField(auto_now=True)),
                ('subject', models.ForeignKey(to='Testing.Subject')),
            ],
        ),
        migrations.CreateModel(
            name='User_Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(default=0)),
                ('user_type', models.IntegerField(default=0)),
                ('picture', models.ImageField(upload_to=b'profile_images', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='test_summary',
            name='user',
            field=models.ForeignKey(related_name='User_Test_Summary', to='Testing.User_Profile'),
        ),
        migrations.AddField(
            model_name='test_report',
            name='test_summary',
            field=models.ForeignKey(related_name='Summary_Test_Report', to='Testing.Test_Summary'),
        ),
        migrations.AddField(
            model_name='test_report',
            name='topper',
            field=models.ForeignKey(related_name='Topper', to='Testing.User_Profile'),
        ),
        migrations.AddField(
            model_name='test',
            name='owner',
            field=models.ForeignKey(to='Testing.User_Profile'),
        ),
        migrations.AddField(
            model_name='test',
            name='questions',
            field=models.ManyToManyField(to='Testing.Question'),
        ),
        migrations.AddField(
            model_name='question_summary',
            name='test_summary',
            field=models.ForeignKey(related_name='Questions', to='Testing.Test_Summary'),
        ),
        migrations.AddField(
            model_name='question_summary',
            name='user',
            field=models.ForeignKey(related_name='User_Question_Summary', to='Testing.User_Profile'),
        ),
        migrations.AddField(
            model_name='question',
            name='owner',
            field=models.ForeignKey(to='Testing.User_Profile'),
        ),
        migrations.AddField(
            model_name='class',
            name='instructor',
            field=models.ForeignKey(related_name='User_Profile_Instructor', to='Testing.User_Profile'),
        ),
        migrations.AddField(
            model_name='class',
            name='students',
            field=models.ManyToManyField(related_name='User_Profile_Students', to='Testing.User_Profile'),
        ),
    ]
