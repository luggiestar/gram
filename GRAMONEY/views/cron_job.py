from apscheduler.schedulers.background import BackgroundScheduler

from django.db.models import Sum
from django.shortcuts import render, redirect

# from ..model_test import *
from datetime import datetime

count = 0


def cron_job():
    global count
    get_investment = Investment.objects.filter(is_active=True)
    # get_current_date = datetime.now().date()
    for i in get_investment:

        save_data = DailyEarning(investment=i, amount=i.day_earning)
        save_data.save()
        scheduler.print_jobs()


scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(cron_job, 'cron', second=30)
scheduler.start()

import time
from datetime import timedelta

# from timeloop import Timeloop
#
# from ..model_test import *
#
# tl = Timeloop()
#
#
# @tl.job(interval=timedelta(seconds=40))
# def train_model():
#     global count
#     get_investment = Investment.objects.all()
#     for i in get_investment:
#         save_data = DailyEarning(investment=i, amount=i.day_earning)
#         save_data.save()
