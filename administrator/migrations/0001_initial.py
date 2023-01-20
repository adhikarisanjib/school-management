# Generated by Django 3.2.16 on 2023-01-17 07:13

import administrator.models
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicSession',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch', models.IntegerField(verbose_name='Batch')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(verbose_name='End Date')),
                ('is_current', models.BooleanField(default=False, verbose_name='Is Current Session')),
            ],
            options={
                'ordering': ('-batch',),
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255, verbose_name='Address')),
                ('city', models.CharField(max_length=63, verbose_name='City')),
                ('state', models.CharField(max_length=63, verbose_name='State')),
                ('country', models.CharField(max_length=63, verbose_name='Country')),
            ],
        ),
        migrations.CreateModel(
            name='Assign',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('Sunday', 'Sunday'), ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday')], max_length=15, verbose_name='Day')),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(max_length=2, verbose_name='section')),
                ('semester', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Class',
                'verbose_name_plural': 'Classes',
                'ordering': ('-academic_session',),
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127, verbose_name='Name')),
                ('code', models.CharField(max_length=15, verbose_name='Code')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127, verbose_name='Name')),
                ('code', models.CharField(max_length=15, verbose_name='Code')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=7, verbose_name='Gender')),
                ('dob', models.DateField(verbose_name='Date Of Birth')),
                ('fathers_name', models.CharField(blank=True, max_length=127, null=True, verbose_name="Father's Name")),
                ('document', models.FileField(blank=True, null=True, upload_to=administrator.models.get_document, verbose_name='Any Document')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127, verbose_name='Name')),
                ('code', models.CharField(max_length=15, verbose_name='Code')),
            ],
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=7, verbose_name='Gender')),
                ('dob', models.DateField(verbose_name='Date Of Birth')),
                ('fathers_name', models.CharField(blank=True, max_length=127, null=True, verbose_name="Father's Name")),
                ('fathers_contact_no', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name="Father's Contact Number")),
                ('mothers_name', models.CharField(blank=True, max_length=127, null=True, verbose_name="Mother's Name")),
                ('mothers_contact_no', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name="Mother's Contact Number")),
                ('document', models.FileField(blank=True, null=True, upload_to=administrator.models.get_document, verbose_name='Any Document')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('current_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student_current_address', to='administrator.address')),
                ('current_class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='administrator.class')),
                ('permanent_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student_permanent_address', to='administrator.address')),
            ],
        ),
    ]