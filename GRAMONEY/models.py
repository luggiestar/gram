import random
import string

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, Group
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None

    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    NATION = (
        ('TANZANIA', 'TANZANIA'),
        ('KENYA', 'KENYA'),

    )
    phone_regex = RegexValidator(regex=r'[0][6-9][0-9]{8}', message="Phone number must be entered in the format: "
                                                                    "'0.....'. Up to 10 digits allowed.")

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=100, null=True, blank=False)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    # sex = model_test.CharField(choices=GENDER, max_length=1, null=True, blank=True)
    country = models.CharField(choices=NATION, max_length=30, null=True, blank=True)
    # group = model_test.ForeignKey(Group, on_delete=model_test.CASCADE, default=1)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # a admin user; non super-user
    is_superuser = models.BooleanField(default=False)  # a superuser

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    objects = CustomUserManager()

    def __str__(self):
        return self.email


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class Account(models.Model):
    code = models.CharField(max_length=6, null=False, unique=True)
    invite = models.CharField(max_length=6, null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)

    class Meta:
        unique_together = ('code', 'invite')

        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return "{0}-{1}".format(self.code, self.user)


class Plan(models.Model):
    PLANS = (
        ('SHORT', 'Short-term'),
        ('LONG', 'Long-term'),
    )
    name = models.CharField(choices=PLANS, max_length=6, null=False, unique=True)
    days = models.IntegerField(unique=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Investment Plan"
        verbose_name_plural = "Investment Plan"

    def __str__(self):
        return "{0}".format(self.name)


class Investment(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start = models.DateField(auto_now_add=True, editable=False)
    end = models.DateField(null=False, blank=False, editable=False)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    roi = models.DecimalField(max_digits=14, decimal_places=2, blank=False, editable=False)
    day_earning = models.DecimalField(max_digits=14, decimal_places=2, blank=False, editable=False)
    is_active = models.BooleanField(default=True)
    is_sent = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.end == datetime.today():
            self.is_active = False
        elif self.plan:
            self.end = datetime.today() + timedelta(days=self.plan.days)
            if self.plan.name == 'SHORT':
                try:
                    # get_latest_balance = InvestmentTracking.objects.filter(investment__account=self.account).order_by(
                    #     '-id').first()
                    # self.amount = get_latest_balance.balance + self.amount
                    get_roi = self.amount * decimal.Decimal(0.3)
                    self.roi = self.amount + get_roi
                    self.day_earning = get_roi / self.plan.days
                except:

                    get_roi = self.amount * decimal.Decimal(0.3)
                    self.roi = self.amount + get_roi
                    self.day_earning = get_roi / self.plan.days

            else:
                try:
                    # get_latest_balance = InvestmentTracking.objects.filter(investment__account=self.account).order_by(
                    #     '-id').first()
                    # self.amount = get_latest_balance.balance + self.amount
                    get_roi = self.amount * decimal.Decimal(0.6)
                    self.roi = self.amount + get_roi
                    self.day_earning = get_roi / self.plan.days
                except:

                    get_roi = self.amount * decimal.Decimal(0.6)
                    self.roi = self.amount + get_roi
                    self.day_earning = get_roi / self.plan.days

        return super(Investment, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Investment"
        verbose_name_plural = "Investments"

    def __str__(self):
        return "{0}-{1}".format(self.account, self.amount)


class DailyEarning(models.Model):
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0.00, editable=False)
    date = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.__class__.objects.filter(investment=self.investment).count() == self.investment.plan.days - 1:
            Investment.objects.filter(id=self.investment.id).update(is_active=False)

        elif self.investment.is_active and self.__class__.objects.filter(
                investment=self.investment).count() <= self.investment.plan.days - 1:
            self.amount = self.investment.day_earning
        else:
            return None

        return super(DailyEarning, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Daily Earning"
        verbose_name_plural = "Daily Earnings"

    def __str__(self):
        return "{0}-{1}".format(self.investment, self.amount)


class InvitationEarning(models.Model):
    investment = models.OneToOneField(Investment, on_delete=models.CASCADE)
    inviter = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0.00, editable=False)
    date = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.investment.account.invite:
            get_inviter = Account.objects.get(code=self.investment.account.invite)
            get_roi = self.investment.amount * decimal.Decimal(0.03)
            self.amount = get_roi
            self.inviter = get_inviter

        else:
            return None

        return super(InvitationEarning, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Invitation  Earning"
        verbose_name_plural = "Invitation Earnings"

    def __str__(self):
        return "{0}-{1}".format(self.investment, self.amount)


class InvestmentTracking(models.Model):
    investment = models.ForeignKey('Investment', on_delete=models.CASCADE)
    total_referral = models.DecimalField(max_digits=14, decimal_places=2, blank=False, default=0.00, editable=False)
    total_earning = models.DecimalField(max_digits=14, decimal_places=2, blank=False, default=0.00, editable=False)
    total_withdraw = models.DecimalField(max_digits=14, decimal_places=2, blank=False, default=0.00, editable=False)
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    date = models.DateField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     if self.total_earning >=1:
    #         self.balance = (self.balance+ self.total_earning + self.total_referral) - self.total_withdraw
    #
    #     return super(InvestmentTracking, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Investment Tracking"
        verbose_name_plural = "Investments Tracking"

    def __str__(self):
        return "{0}-{1}".format(self.investment, self.balance)


def id_generator(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class Withdraw(models.Model):
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE)
    payment_number = models.CharField(max_length=15, null=True, blank=True, unique=True, editable=False)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    date = models.DateField(auto_now=True)
    is_confirmed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_confirmed:
            self.payment_number = id_generator()

        return super(Withdraw, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Withdraw  Request"
        verbose_name_plural = "Withdraw Requests"

    def __str__(self):
        return "{0}-{1}".format(self.investment.account, self.amount)
