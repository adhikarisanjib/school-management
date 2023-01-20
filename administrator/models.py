import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from base.models import User

GENDER_CHOICE = (
    ("Male", "Male"),
    ("Female", "Female"),
)

DAYS_OF_WEEK = (
    ("Sunday", "Sunday"),
    ("Monday", "Monday"),
    ("Tuesday", "Tuesday"),
    ("Wednesday", "Wednesday"),
    ("Thursday", "Thursday"),
    ("Friday", "Friday"),
    ("Saturday", "Saturday"),
)


def get_document(person, filename):
    return f"{person.user.id}/document/{filename}"


class AcademicSession(models.Model):
    id = models.UUIDField(
        verbose_name=_("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    batch = models.IntegerField(
        verbose_name=_("Batch"),
    )
    start_date = models.DateField(
        verbose_name=_("Start Date"),
    )
    end_date = models.DateField(
        verbose_name=_("End Date"),
    )
    is_current = models.BooleanField(
        verbose_name=_("Is Current Session"),
        default=False,
    )

    def __str__(self):
        return f"{self.start_date} {self.end_date}"

    def get_fields_and_values(self):
        return [(field, field.value_to_string(self)) for field in AcademicSession._meta.fields]

    class Meta:
        ordering = ("-batch",)
        unique_together = (("batch", "start_date", "end_date"),)


class Department(models.Model):
    id = models.UUIDField(
        verbose_name=_("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=127,
    )
    code = models.CharField(
        verbose_name=_("Code"),
        max_length=15,
    )

    def __str__(self):
        return self.name

    def get_fields_and_values(self):
        return [(field, field.value_to_string(self)) for field in Department._meta.fields]


class Course(models.Model):
    id = models.UUIDField(
        verbose_name=_("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=127,
    )
    code = models.CharField(
        verbose_name=_("Code"),
        max_length=15,
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    def get_fields_and_values(self):
        return [(field, field.value_to_string(self)) for field in Course._meta.fields]


class Class(models.Model):
    id = models.UUIDField(
        verbose_name=_("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    academic_session = models.ForeignKey(
        AcademicSession,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    semester = models.IntegerField(
        verbose_name=_("Semester"),
    )
    section = models.CharField(
        verbose_name=_("section"),
        max_length=2,
    )

    def __str__(self):
        return f"{self.course} {self.semester} {self.section}"

    def get_fields_and_values(self):
        return [(field, field.value_to_string(self)) for field in Class._meta.fields]

    class Meta:
        ordering = ("-academic_session",)
        verbose_name = "Class"
        verbose_name_plural = "Classes"


class Subject(models.Model):
    id = models.UUIDField(
        verbose_name=_("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=127,
    )
    code = models.CharField(
        verbose_name=_("Code"),
        max_length=15,
    )

    def __str__(self):
        return self.name

    def get_fields_and_values(self):
        return [(field, field.value_to_string(self)) for field in Subject._meta.fields]


class Address(models.Model):
    id = models.UUIDField(
        verbose_name=_("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    address = models.CharField(
        verbose_name=_("Address"),
        max_length=255,
    )
    city = models.CharField(
        verbose_name=_("City"),
        max_length=63,
    )
    state = models.CharField(
        verbose_name=_("State"),
        max_length=63,
    )
    country = models.CharField(
        verbose_name=_("Country"),
        max_length=63,
    )

    def __str__(self):
        return f"{self.city} {self.country}"

    def get_fields_and_values(self):
        return [(field, field.value_to_string(self)) for field in Address._meta.fields]


class Student(models.Model):
    id = models.UUIDField(
        verbose_name=_("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    current_class = models.ForeignKey(
        Class,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    gender = models.CharField(
        verbose_name=_("Gender"),
        max_length=7,
        choices=GENDER_CHOICE,
        default="Male",
    )
    dob = models.DateField(
        verbose_name=_("Date Of Birth"),
    )
    fathers_name = models.CharField(
        verbose_name=_("Father's Name"),
        max_length=127,
        blank=True,
        null=True,
    )
    fathers_contact_no = PhoneNumberField(
        verbose_name=_("Father's Contact Number"),
        blank=True,
        null=True,
    )
    mothers_name = models.CharField(
        verbose_name=_("Mother's Name"),
        max_length=127,
        blank=True,
        null=True,
    )
    mothers_contact_no = PhoneNumberField(
        verbose_name=_("Mother's Contact Number"),
        blank=True,
        null=True,
    )
    permanent_address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="student_permanent_address",
    )
    current_address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="student_current_address",
    )
    document = models.FileField(
        verbose_name=_("Any Document"),
        upload_to=get_document,
        blank=True,
        null=True,
    )
    created = models.DateTimeField(
        verbose_name=_("Created"),
        auto_now_add=True,
    )

    def __str__(self):
        return self.user.name

    def get_fields_and_values(self):
        student = [
            ("id", self.id),
            ("current_class", self.current_class),
            ("gender", self.gender),
            ("dob", self.dob),
            ("fathers_name", self.fathers_name),
            ("fathers_contact_no", self.fathers_contact_no),
            ("mothers_name", self.mothers_name),
            ("mothers_contact_no", self.mothers_contact_no),
            ("document", self.document),
            ("created", self.created),
        ]
        return student


class Staff(models.Model):
    id = models.UUIDField(
        verbose_name=_("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    gender = models.CharField(
        verbose_name=_("Gender"),
        max_length=7,
        choices=GENDER_CHOICE,
        default="Male",
    )
    dob = models.DateField(
        verbose_name=_("Date Of Birth"),
    )
    fathers_name = models.CharField(
        verbose_name=_("Father's Name"),
        max_length=127,
        blank=True,
        null=True,
    )
    permanent_address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="staff_permanent_address",
    )
    current_address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="staff_current_address",
    )
    document = models.FileField(
        verbose_name=_("Any Document"),
        upload_to=get_document,
        blank=True,
        null=True,
    )
    created = models.DateTimeField(
        verbose_name=_("Created"),
        auto_now_add=True,
    )

    def __str__(self):
        return self.user.name

    def get_fields_and_values(self):
        staff = [
            ("id", self.id),
            ("gender", self.gender),
            ("dob", self.dob),
            ("fathers_name", self.fathers_name),
            ("document", self.document),
            ("created", self.created),
        ]
        return staff


class TimeSlot(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time} {self.end_time}"

    def get_fields_and_values(self):
        return [(field, field.value_to_string(self)) for field in TimeSlot._meta.fields]


class Assign(models.Model):
    id = models.UUIDField(
        verbose_name=_("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    day = models.CharField(
        verbose_name=_("Day"),
        max_length=15,
        choices=DAYS_OF_WEEK,
    )
    timeslot = models.ForeignKey(
        TimeSlot,
        on_delete=models.CASCADE,
    )
    teacher = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    assign_class = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        verbose_name=_("Class"),
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.day} {self.assign_class} {self.timeslot} {self.teacher}"

    def get_fields_and_values(self):
        return [(field, field.value_to_string(self)) for field in Assign._meta.fields]

    class Meta:
        unique_together = (("day", "timeslot", "teacher", "assign_class"),)
