# Generated by Django 4.2.7 on 2023-11-02 22:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=50)),
                ('course_code', models.CharField(max_length=6, unique=True)),
                ('unit_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('student_number', models.CharField(max_length=9, unique=True)),
                ('enrollment_year', models.DateField()),
                ('major', models.CharField(choices=[('CE', 'COMPUTER ENGINEERING'), ('CS', 'COMPUTER SCIENCE')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('staff_number', models.CharField(max_length=10, unique=True)),
                ('hiring_year', models.DateField()),
                ('department', models.CharField(choices=[('CE', 'COMPUTER ENGINEERING'), ('CS', 'COMPUTER SCIENCE')], max_length=3)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='professor', to='university.course')),
            ],
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(max_length=50)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollment', to='university.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollment', to='university.student')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('head_of_department', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='head_of_department', to='university.professor')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='offered_by',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='university.professor'),
        ),
    ]
