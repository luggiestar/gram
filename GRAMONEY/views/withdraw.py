from django.db.models import Sum
from django.shortcuts import render, redirect

# from ..model_test import *
from ..models import *


def withdraw_request(request):
    try:
        get_withdraw = Withdraw.objects.filter(is_confirmed=False)
        get_withdraw_confirmed = Withdraw.objects.filter(is_confirmed=True).count()
        get_withdraw_confirmed_total = Withdraw.objects.filter(is_confirmed=True).aggregate(total=Sum('amount'))
        get_withdraw_unconfirmed = Withdraw.objects.filter(is_confirmed=False).count
        get_withdraw_unconfirmed_total = Withdraw.objects.filter(is_confirmed=False).aggregate(total=Sum('amount'))

    except:
        get_withdraw = 0
        get_withdraw_confirmed = 0
        get_withdraw_confirmed_total = 0
        get_withdraw_unconfirmed = 0
        get_withdraw_unconfirmed_total = 0

    context = {
        'withdraw': get_withdraw,
        'withdraw_count': get_withdraw_confirmed,
        'unwithdraw_count': get_withdraw_unconfirmed,
        'withdraw_total': get_withdraw_confirmed_total,
        'unwithdraw_total': get_withdraw_unconfirmed_total
    }
    return render(request, 'user/withdraw_request.html', context)
