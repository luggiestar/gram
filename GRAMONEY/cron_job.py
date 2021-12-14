from models import *
count = 0

def cron_job():
    global count
    global mylist
    get_investment = Investment.objects.filter(is_active=True)
    # get_current_date = datetime.now().date()
    for i in get_investment:
        save_data = DailyEarning(investment=i, amount=i.day_earning)
        save_data.save()
        print(i)

print(cron_job())
