from django.db.models import Sum
from django.shortcuts import render, redirect

# from ..model_test import *
from ..models import *


def userHome(request):
    try:
        get_code = Account.objects.get(user=request.user)
        get_investment = Investment.objects.filter(account__user=request.user).order_by('-id').first()
        get_total = DailyEarning.objects.filter(investment=get_investment).aggregate(total=Sum('amount'))
        get_total_referral = InvitationEarning.objects.filter(inviter=get_investment.account).aggregate(
            total=Sum('amount'))
    except:
        get_investment = 0
        get_total = 0
        get_total_referral = 0
        get_code = ""

    context = {
        'investment': get_investment,
        'earning': get_total,
        'code': get_code,
        'invitation': get_total_referral
    }
    return render(request, 'user/home.html', context)
