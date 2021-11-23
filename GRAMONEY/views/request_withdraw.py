from django.shortcuts import render, redirect, get_object_or_404

# from ..model_test import Withdraw, Investment

from ..models import *

def request_withdraw(request):
    get_investment = get_object_or_404(Investment, account__user=request.user)
    if request.POST:
        amount = request.POST['amount']

        save_withdraw = Withdraw.objects(
            investment=get_investment,
            amount=amount,
        )
        save_withdraw.save()

        if save_withdraw:
            return redirect('GRAMONEY:withdraw_request')
