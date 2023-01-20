import datetime
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from administrator.models import Course, Student


class Fee(models.Model):
    id = models.UUIDField(
        verbose_name=_("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )
    tuition_fee = models.DecimalField(
        verbose_name=_("Tuition Fee"),
        max_digits=9,
        decimal_places=2,
        default=0,
    )
    admission_fee = models.DecimalField(
        verbose_name=_("Admission Fee"),
        max_digits=9,
        decimal_places=2,
        default=0,
    )
    exam_fee = models.DecimalField(
        verbose_name=_("Exam Fee"),
        max_digits=7,
        decimal_places=2,
        default=0,
    )
    extra_fee = models.DecimalField(
        verbose_name=_("Extra Activities"),
        max_digits=7,
        decimal_places=2,
        default=0,
    )

    def __str__(self):
        return f"{self.course}"

    def get_total_fee(self):
        return self.tuition_fee + self.exam_fee + self.admission_fee + self.extra_fee

    def get_payable_fee(self):
        month = datetime.date.today().month

        tutition_fee_upto_now = (self.tuition_fee / 12) * month
        exam_fee_upto_now = self.exam_fee if month < 3 else (self.exam_fee * 2) if month < 8 else (self.exam_fee * 3)

        return tutition_fee_upto_now + exam_fee_upto_now + self.admission_fee + self.extra_fee


class StudentFee(models.Model):
    id = models.UUIDField(
        verbose_name=_("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
    )
    paid_amount = models.DecimalField(
        verbose_name=("Paid Amount"),
        max_digits=9,
        decimal_places=2,
        default=0,
    )
    previous_dues = models.DecimalField(
        verbose_name=("Previous Year Dues"),
        max_digits=9,
        decimal_places=2,
        default=0,
    )

    def __str__(self):
        return f"{self.student.user.name} {self.paid_amount}"

    def pay_fee(self, amount):
        amount = float(amount)
        dues = float(self.previous_dues)
        if amount <= dues:
            self.previous_dues = float(self.previous_dues) - amount
        else:
            amount = amount - dues
            self.previous_dues = 0.0
            self.paid_amount = float(self.paid_amount) + amount
        self.save()


class PaymentRecord(models.Model):
    id = models.UUIDField(
        verbose_name=_("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        verbose_name=_("Amount"),
        max_digits=9,
        decimal_places=2,
        default=0,
    )
    method = models.CharField(
        verbose_name=_("Payment Method"),
        max_length=31,
        default="Account Section",
    )
    date = models.DateTimeField(
        verbose_name=_("date"),
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.student.user.name} {self.amount}"
