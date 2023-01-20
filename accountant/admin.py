from django.contrib import admin

from accountant.models import Fee, PaymentRecord, StudentFee

admin.site.register(Fee)
admin.site.register(StudentFee)
admin.site.register(PaymentRecord)
