from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'first_name', 'last_name', 'phone', 'country', 'is_active', 'is_staff',
                    'is_superuser', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups',
                                    'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)


class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'invite')


admin.site.register(Account, AccountAdmin)


class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'days', 'created_by')
    search_field = ['name', 'days']


admin.site.register(Plan, PlanAdmin)


class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('account', 'plan', 'amount', 'start', 'end', 'is_active', 'is_sent')
    search_field = ['account']
    # list_filter = ['plan']


admin.site.register(Investment, InvestmentAdmin)


class DailyEarningAdmin(admin.ModelAdmin):
    list_display = ('investment', 'amount', 'date')
    search_field = ['account', 'date']


admin.site.register(DailyEarning, DailyEarningAdmin)


class InvitationEarningAdmin(admin.ModelAdmin):
    list_display = ('investment', 'inviter', 'amount', 'date')
    search_field = ['investment', 'inviter']


admin.site.register(InvitationEarning, InvitationEarningAdmin)


class WithdrawAdmin(admin.ModelAdmin):
    list_display = ('investment', 'amount', 'payment_number', 'is_confirmed')
    search_field = ['payment_number']


admin.site.register(Withdraw, WithdrawAdmin)


class InvestmentTrackingAdmin(admin.ModelAdmin):
    list_display = ('investment', 'total_referral', 'total_earning', 'total_withdraw', 'balance')
    search_field = ['investment']


admin.site.register(InvestmentTracking, InvestmentTrackingAdmin)
