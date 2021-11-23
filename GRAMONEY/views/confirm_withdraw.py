from django.shortcuts import render, redirect, get_object_or_404

# from ..model_test import  Withdraw
from ..models import *


def confirm_withdraw(request, withdraw):
    get_withdraw = get_object_or_404(Withdraw, id=withdraw)
    update = Withdraw.objects.filter(id=get_withdraw.id).update(is_confirmed=True)
    if update:
        return redirect('GRAMONEY:withdraw_request')
