from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

MAJOR_CHOICES = (
    ("CE", "COMPUTER ENGINEERING"),
    ("CS", "COMPUTER SCIENCE"),
)


class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    student_number = models.CharField(unique=True, max_length=9)
    enrollment_year = models.PositiveIntegerField(validators=[MinValueValidator(1300), MaxValueValidator(1500)])
    major = models.CharField(max_length=3, choices=MAJOR_CHOICES)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Department(models.Model):
    name = models.CharField(max_length=50, unique=True)
    head_of_department = models.OneToOneField(
        to='Professor', on_delete=models.CASCADE, related_name='head_of', null=True, blank=True
    )

    def __str__(self):
        return f'{self.name}'

    def clean(self):
        if self.head_of_department and self.head_of_department.department != self:  # noqa
            raise ValidationError('The head must be a member of this department.')


class Professor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    staff_number = models.CharField(unique=True, max_length=10)
    hiring_year = models.DateField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='professors')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Course(models.Model):
    course_name = models.CharField(max_length=50)
    course_code = models.CharField(unique=True, max_length=6)
    unit_count = models.PositiveIntegerField()
    offered_by = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name="courses")

    def __str__(self):
        return f'{self.course_code}: {self.course_name} by {self.offered_by}'


class Enrollment(models.Model):
    semester = models.CharField(max_length=50)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")

    class Meta:
        unique_together = ('student', 'course', 'semester')

    def __str__(self):
        return f'{self.student} - ({self.course})'
