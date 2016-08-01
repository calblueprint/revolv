from django.contrib import admin

from .models import (
    AdminReinvestment, AdminRepayment, Payment, ProjectMontlyRepaymentConfig,
    PaymentType, RepaymentFragment, UserReinvestment, Tip
)

admin.site.register(AdminReinvestment)
admin.site.register(AdminRepayment)
admin.site.register(Payment)
admin.site.register(ProjectMontlyRepaymentConfig)
admin.site.register(PaymentType)
admin.site.register(RepaymentFragment)
admin.site.register(UserReinvestment)
admin.site.register(Tip)
