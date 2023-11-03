from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# define a tuple of possible choices for major field
MAJOR_CHOICES = (
    ("CE", "COMPUTER ENGINEERING"),
    ("CS", "COMPUTER SCIENCE"),
)


class Student(models.Model):  # define the fields for the student model
    first_name = models.CharField(max_length=50)  # first name is a string with maximum length of 50 characters
    last_name = models.CharField(max_length=50)  # last name is a string with maximum length of 50 characters
    student_number = models.CharField(unique=True,
                                      max_length=9)  # student number is a unique string with maximum length of 9 characters
    # enrollment year is a positive integer that is between 1300 and 1500 Hejri Shamsi
    enrollment_year = models.PositiveIntegerField(validators=[MinValueValidator(1300), MaxValueValidator(1500)])
    # major can be chosen among choices that are mentioned before as tuples
    major = models.CharField(max_length=3, choices=MAJOR_CHOICES)

    # this function returns first and last name of student instead of object name
    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Department(models.Model):  # define the fields for the department model
    # two department can't have same name
    name = models.CharField(max_length=50, unique=True)
    # head_of_department is a one-to-one relation with professor model
    head_of_department = models.OneToOneField(
        to='Professor', on_delete=models.CASCADE, related_name='head_of', null=True, blank=True
    )

    # this function displays department name instead of object name
    def __str__(self):
        return f'{self.name}'

    # this function validates the head_of_department field
    def clean(self):
        if self.head_of_department and self.head_of_department.department != self:  # noqa
            raise ValidationError('The head must be a member of this department.')


class Professor(models.Model):  # define the fields for the professor model
    first_name = models.CharField(max_length=50)  # first name is a string with maximum length of 50 characters
    last_name = models.CharField(max_length=50)  # last name is a string with maximum length of 50 characters
    staff_number = models.CharField(unique=True,
                                    max_length=10)  # staff number is a unique string with maximum length of 10 characters
    hiring_year = models.DateField()  # hiring year is a date field
    # the department that this professor is member of it
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='professors')

    # this function returns first and last name of Professor instead of object name
    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Course(models.Model):  # define the fields for the course model
    course_name = models.CharField(max_length=50)  # course name is a string with maximum length of 50 characters
    course_code = models.CharField(unique=True,
                                   max_length=6)  # course code is a unique string with maximum length of 6 characters
    unit_count = models.PositiveIntegerField()  # unit count is a positive integer
    # offered_by is a foreign key relation with professor model
    offered_by = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name="courses")

    # this function returns first and last name of student instead of object name
    def __str__(self):
        return f'{self.course_code}: {self.course_name} by {self.offered_by}'


class Enrollment(models.Model):  # define the fields for the enrollment model
    semester = models.CharField(max_length=50)  # semester is a string with maximum length of 50 characters
    student = models.ForeignKey(Student, on_delete=models.CASCADE,
                                related_name="enrollments")  # student is a foreign key relation with student model
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name="enrollments")  # course is a foreign key relation with course model

    # define a unique constraint for the combination of student, course and semester
    class Meta:
        unique_together = ('student', 'course', 'semester')

    # this function returns first and last name of student that enrolled a specific course
    def __str__(self):
        return f'{self.student} - ({self.course})'


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
