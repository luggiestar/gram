import json
import requests
import base64

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import *


def reference_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# @receiver(post_save, sender=Investment, dispatch_uid='send_sms_to_user')
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         URL = 'https://apisms.beem.africa/v1/send'
#         api_key = '2799f1a807695012'
#         secret_key = 'YTU2NTkxZjQxZDc4NTY2NGZiZTVkYzI5ZWU1MzFmYzM4NzA4MTBkYjk5NWE4MzZmZmU0MjQ2OTU3YjJjN2IxZg===='
#         content_type = 'application/json'
#         source_addr = 'EHGETS'
#         apikey_and_apisecret = api_key + ':' + secret_key
#
#         data = []
#
#         user_detail = Investment.objects.filter(is_active=True, is_sent=False)
#
#         if user_detail:
#             for i in user_detail:
#                 '''Get name and concatenate them'''
#                 first_name = i.account.user.first_name
#                 last_name = i.account.user.last_name
#                 full_name = f"{first_name} {last_name}"
#
#                 congaturation = f"Congaturation {full_name} Your payment recieved successfully to Gramoney Investment"
#
#                 '''Get amount invested and daily amount earning'''
#                 amount = i.amount
#                 day_earning = i.day_earning
#                 amounts = f"\nAmount paid:{amount}\nEarning/day:{day_earning}"
#
#                 '''Get start time and end time'''
#                 start_time = i.start
#                 end_time = i.end
#                 time = f"\nStart date:{start_time}\nEnd date:{end_time}"
#
#                 '''Get phone detail and convert and user id as recipient_id on api'''
#                 phone = str(i.account.user.phone)
#                 phone = phone[1:10]
#                 phone = '255' + phone
#                 user_id = i.account.user.id
#
#                 reference_number = reference_generator()
#                 reference_number = f"\nRef:{reference_number}"
#
#                 # link = "\nlogin to your account via \nhttps://gramoney.herokuapp.com/"
#
#                 message_body = congaturation + amounts + reference_number + time
#
#                 print(message_body)
#                 first_request = requests.post(url=URL, data=json.dumps({
#                     'source_addr': source_addr,
#                     'schedule_time': '',
#                     'encoding': '0',
#                     'message': message_body,
#                     'recipients': [
#                         {
#                             'recipient_id': user_id,
#                             'dest_addr': phone,
#                         },
#                     ],
#                 }),
#
#                                               headers={
#                                                   'Content-Type': content_type,
#                                                   'Authorization': 'Basic ' + api_key + ':' + secret_key,
#                                               },
#
#
#                                               auth=(api_key, secret_key), verify=False)
#                 print(first_request.status_code)
#                 print(first_request.json())
#                 if first_request.status_code == 200:
#                     Investment.objects.filter(id=i.id).update(is_sent=True)
#                 return (first_request.json())
#         else:
#             print("Error")


@receiver(post_save, sender=Investment, dispatch_uid='save_invitation_earning')
def create_investment(sender, instance, created, **kwargs):
    if created:
        try:
            get_latest_balance = InvestmentTracking.objects.filter(investment__account=instance.account).order_by(
                '-id').first()
            save_balance = InvestmentTracking(
                investment=instance,
                balance=get_latest_balance.balance + instance.amount,
            )
            save_balance.save()
        except:
            save_balance = InvestmentTracking(
                investment=instance,
                balance=instance.amount

            )
            save_balance.save()
        save_referrals = InvitationEarning(investment=instance)
        save_referrals.save()


@receiver(post_save, sender=DailyEarning, dispatch_uid='update_balance_after_erning')
def create_referral(sender, instance, created, **kwargs):
    if created:
        get_latest_balance = InvestmentTracking.objects.filter(
            investment__account=instance.investment.account).order_by(
            '-id').first()
        print(get_latest_balance.balance)

        save_balance = InvestmentTracking(
            investment=instance.investment,
            total_earning=instance.amount,
            balance=get_latest_balance.balance + instance.amount
        )
        save_balance.save()


@receiver(post_save, sender=Withdraw, dispatch_uid='update_balance_after_withdraw')
def create_referral(sender, instance, created, **kwargs):
    if created:
        get_latest_balance = InvestmentTracking.objects.filter(
            investment__account=instance.investment.account).order_by(
            '-id').first()
        print(get_latest_balance.balance)

        save_balance = InvestmentTracking(
            investment=instance.investment,
            # total_referral=get_latest_balance.total_referral,
            # total_earning=instance.amount,
            total_withdraw=instance.amount,
            balance=get_latest_balance.balance - instance.amount
        )
        save_balance.save()


@receiver(post_save, sender=InvitationEarning, dispatch_uid='update_balance_after_invitation')
def create_referral(sender, instance, created, **kwargs):
    if created:
        get_latest_balance = InvestmentTracking.objects.filter(
            investment__account=instance.investment.account).order_by(
            '-id').first()
        print(get_latest_balance.balance)

        save_balance = InvestmentTracking(
            investment=instance.investment,
            total_referral=instance.amount,
            # total_earning=instance.amount,
            # total_withdraw=instance.amount,
            balance=get_latest_balance.balance + instance.amount
        )
        save_balance.save()
