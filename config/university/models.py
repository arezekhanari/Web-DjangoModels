from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

MAJOR_CHOICES = (
    ("CE", "COMPUTER ENGINEERING"),
    ("CS", "COMPUTER SCIENCE"),
)


# Student Model
class Student(models.Model):
    # First name of the student
    first_name = models.CharField(max_length=50)

    # Last name of the student
    last_name = models.CharField(max_length=50)

    # Unique student number
    student_number = models.CharField(unique=True, max_length=9)

    # Year of enrollment, validated between 1300 and 1500
    enrollment_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1300), MaxValueValidator(1500)])

    # Major of the student (Computer Engineering or Computer Science)
    major = models.CharField(max_length=3, choices=MAJOR_CHOICES)

# Department Model


class Department(models.Model):
    # Name of the department
    name = models.CharField(max_length=50, unique=True)

    # Head of the department (One-to-One relationship with Professor)
    head_of_department = models.OneToOneField(
        to='Professor', on_delete=models.CASCADE, related_name='head_of', null=True, blank=True
    )


# Professor Model
class Professor(models.Model):
    # First name of the professor
    first_name = models.CharField(max_length=50)

    # Last name of the professor
    last_name = models.CharField(max_length=50)

    # Unique staff number
    staff_number = models.CharField(unique=True, max_length=10)

    # Hiring year of the professor
    hiring_year = models.DateField()

    # Department to which the professor belongs
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name='professors')


# Course Model
class Course(models.Model):
    # Name of the course
    course_name = models.CharField(max_length=50)

    # Unique course code
    course_code = models.CharField(unique=True, max_length=6)

    # Unit count for the course
    unit_count = models.PositiveIntegerField()

    # Professor offering the course
    offered_by = models.ForeignKey(
        Professor, on_delete=models.CASCADE, related_name="courses")


# Enrollment Model
class Enrollment(models.Model):
    # Semester of enrollment
    semester = models.CharField(max_length=50)

    # Student enrolled in the course
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="enrollments")

    # Course in which the student is enrolled
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="enrollments")

    # Ensure uniqueness based on student, course, and semester
    class Meta:
        unique_together = ('student', 'course', 'semester')


# Assignment Model
class Assignment(models.Model):
    # Title of the assignment
    title = models.CharField(max_length=100)

    # Description of the assignment
    description = models.TextField()

    # Due date for the assignment
    due_date = models.DateTimeField()

    # Maximum score achievable for the assignment
    max_score = models.PositiveIntegerField()

    # Course to which the assignment is associated
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="assignments")


# Classroom Model
class Classroom(models.Model):
    # Name or identifier for the classroom
    name = models.CharField(max_length=50)

    # Maximum seating capacity of the classroom
    seating_capacity = models.PositiveIntegerField()

    # Building or location where the classroom is situated
    location = models.CharField(max_length=100)

    # Description of the classroom (optional)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# ClassroomUsage Model
class ClassroomUsage(models.Model):
    # The course for which the classroom is scheduled
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="classroom_usages")

    # The classroom scheduled for the course
    classroom = models.ForeignKey(
        Classroom, on_delete=models.CASCADE, related_name="classroom_usages")

    # Date and time when the classroom will be used for the course
    scheduled_datetime = models.DateTimeField()

    def __str__(self):
        return f'{self.course} in {self.classroom} at {self.scheduled_datetime}'
