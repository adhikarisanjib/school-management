# Generated by Django 3.2.16 on 2023-01-17 07:13

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fee',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('tuition_fee', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Tuition Fee')),
                ('admission_fee', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Admission Fee')),
                ('exam_fee', models.DecimalField(decimal_places=2, default=0, max_digits=7, verbose_name='Exam Fee')),
                ('extra_fee', models.DecimalField(decimal_places=2, default=0, max_digits=7, verbose_name='Extra Activities')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentRecord',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Amount')),
                ('method', models.CharField(default='Account Section', max_length=31, verbose_name='Payment Method')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='date')),
            ],
        ),
        migrations.CreateModel(
            name='StudentFee',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid_amount', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Paid Amount')),
                ('previous_dues', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Previous Year Dues')),
            ],
        ),
    ]