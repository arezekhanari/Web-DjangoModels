from django.db import models

# Create your models here.

MAJOR_CHOICES = (
    ("CE", "COMPUTER ENGINEERING"),
    ("CS", "COMPUTER SCIENCE"),
)


class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    student_number = models.CharField(unique=True, max_length=9)
    enrollment_year = models.DateField()
    major = models.CharField(max_length=3, choices=MAJOR_CHOICES)

    def __str__(self):
        return (f'{self.first_name}-{self.last_name}: with student number: {self.student_number} '
                f'and enrollment year: {self.enrollment_year} is studying in major: {self.major}')


class Professor(models.Model):
    # course = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="professor")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    staff_number = models.CharField(unique=True, max_length=10)
    hiring_year = models.DateField()
    department = models.CharField(max_length=3, choices=MAJOR_CHOICES)

    def __str__(self):
        return f'{self.first_name}-{self.last_name}: with staff number: {self.staff_number}'


class Course(models.Model):
    course_name = models.CharField(max_length=50)
    course_code = models.CharField(unique=True, max_length=6)
    unit_count = models.IntegerField()
    offered_by = models.OneToOneField(Professor, on_delete=models.CASCADE, related_name="courses")

    def __str__(self):
        return f'{self.course_name}-{self.course_code}: with unit_count: {self.unit_count}: offered_by: {self.offered_by}'


class Enrollment(models.Model):
    semester = models.CharField(max_length=50)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollment")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollment")

    def __str__(self):
        return f'{self.student.first_name}-{self.student.last_name} has the {self.course.course_name} in semester {self.semester}'


class Department(models.Model):
    head_of_department = models.OneToOneField(Professor, on_delete=models.CASCADE, related_name="head_of_department")
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.head_of_department.first_name}-{self.head_of_department.last_name} is head of the {self.name} department'
