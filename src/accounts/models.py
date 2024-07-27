from datetime import date

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_resized import ResizedImageField
from phonenumber_field.modelfields import PhoneNumberField

from src.administration.admins.models import (
    StockIn, StockOut, Transfer, StockOutJudicial, StockInJudicial, TransferJudicial
)

from django.db.models import Sum

"""
At the start please be careful to start migrations
--------------------------------------------------

STEP: 1 comment current_subscription [FIELD] in model [USER]
STEP: 1 py manage.py makemigrations accounts
STEP: 2 py manage.py migrate
Then do next ...

"""

judicial_stamps = ['j30', 'j35', 'j50', 'j100', 'j500', 'j1000', 'j2000', 'j3000', 'j5000', 'j10000', 'j15000']
non_judicial_stamps = ['s100', 's150', 's200', 's250', 's300', 's400', 's500', 's750', 's1000', 's2000', 's3000',
                       's5000', 's10000', 's25000', 's50000']
all_stamps = judicial_stamps + non_judicial_stamps


def validate_cnic(value):
    if len(str(value)) != 13:
        raise ValidationError("CNIC must contains 13 digits without any dashes '-' ")
    return value


def phone_number_validator(value):
    if 13 < len(value) < 1:
        raise ValidationError("Phone number must contains less than 13 digits")
    return value


def numbers_only(value):
    if not value.isdigit():
        raise ValidationError("Only numbers are allowed")
    return value


def validate_age(value):
    if value > date.today():
        raise ValidationError("You are a time traveler! Please provide a valid date of birth.")
    elif value.year > date.today().year - 8:
        raise ValidationError("User looks child. Can you double-check date of birth?")
    elif value.year < date.today().year - 100:
        raise ValidationError("User is too old to use such a cutting-edge IMS, time for some retirement plans?")


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=200)
    profile_image = ResizedImageField(
        upload_to='accounts/images/profiles/', null=True, blank=True, size=[250, 250], quality=75, force_format='PNG',
        help_text='size of logo must be 250*250 and format must be png image file', crop=['middle', 'center']
    )

    dob = models.DateField(null=True, blank=False, verbose_name="Date of Birth", validators=[validate_age])
    designation = models.CharField(max_length=200, null=True, blank=False)
    treasury = models.ForeignKey('Treasury', on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True, region='PK')
    cnic = models.CharField(max_length=13, help_text='Enter cnic Number without - ', null=True,
                            validators=[validate_cnic, numbers_only])

    class Meta:
        ordering = ['-id']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.first_name} {self.last_name}' if self.first_name or self.last_name else self.username

    def delete(self, *args, **kwargs):
        self.profile_image.delete(save=True)
        super(User, self).delete(*args, **kwargs)

    # ✅
    def get_total_stock_in_count(self):
        return self.stockin_set.count()

    # 🆕
    def get_total_stock_in_count_judicial(self):
        return self.stockinjudicial_set.count()

    # ✅
    def get_total_stock_out_count(self):
        return self.stockout_set.count()

    # 🆕
    def get_total_stock_out_count_judicial(self):
        return self.stockoutjudicial_set.count()

    # ✅
    def get_total_transfer_count(self):
        return self.transfer_set.filter(status='complete').count()

    # 🆕
    def get_total_transfer_count_judicial(self):
        return self.transferjudicial_set.filter(status='complete').count()

    def get_short_name(self):
        return self.get_name_or_username()[0] if not self.profile_image else self.profile_image

    def get_name_or_username(self):
        return f'{self.first_name} {self.last_name}' if self.first_name or self.last_name else self.username


class City(models.Model):
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'District'
        verbose_name_plural = 'Districts'

    def __str__(self):
        return self.name


class Treasury(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.OneToOneField(
        City, null=True, blank=False, on_delete=models.SET_NULL, verbose_name='District'
    )
    phone_number = models.CharField(max_length=20, null=True, blank=True,
                                    validators=[phone_number_validator, numbers_only])
    email = models.EmailField(max_length=100, null=True, blank=True)

    # NON JUDICIAL STAMPS
    s100 = models.PositiveIntegerField(default=0)
    s150 = models.PositiveIntegerField(default=0)
    s200 = models.PositiveIntegerField(default=0)
    s250 = models.PositiveIntegerField(default=0)
    s300 = models.PositiveIntegerField(default=0)
    s400 = models.PositiveIntegerField(default=0)
    s500 = models.PositiveIntegerField(default=0)
    s750 = models.PositiveIntegerField(default=0)
    s1000 = models.PositiveIntegerField(default=0)
    s2000 = models.PositiveIntegerField(default=0)
    s3000 = models.PositiveIntegerField(default=0)
    s5000 = models.PositiveIntegerField(default=0)
    s10000 = models.PositiveIntegerField(default=0)
    s25000 = models.PositiveIntegerField(default=0)
    s50000 = models.PositiveIntegerField(default=0)

    # JUDICIAL STAMPS
    j25 = models.PositiveIntegerField(default=0)
    j30 = models.PositiveIntegerField(default=0)
    j35 = models.PositiveIntegerField(default=0)
    j50 = models.PositiveIntegerField(default=0)
    j60 = models.PositiveIntegerField(default=0)
    j75 = models.PositiveIntegerField(default=0)
    j100 = models.PositiveIntegerField(default=0)
    j125 = models.PositiveIntegerField(default=0)
    j150 = models.PositiveIntegerField(default=0)
    j200 = models.PositiveIntegerField(default=0)
    j500 = models.PositiveIntegerField(default=0)
    j1000 = models.PositiveIntegerField(default=0)
    j2000 = models.PositiveIntegerField(default=0)
    j3000 = models.PositiveIntegerField(default=0)
    j5000 = models.PositiveIntegerField(default=0)
    j10000 = models.PositiveIntegerField(default=0)
    j15000 = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['city__name']
        verbose_name_plural = 'Treasuries'

    def __str__(self):
        return self.name

    # ✅
    def get_all_transfers(self):
        return Transfer.objects.filter(destination_treasury=self)

    # 🆕
    def get_all_transfers_judicial(self):
        return TransferJudicial.objects.filter(destination_treasury=self)

    # ✅
    def get_staff(self):
        return User.objects.filter(treasury=self)

    # COUNTS -----------------------------------------------------------------------------------------------------------

    # ✅
    def get_staff_count(self):
        return User.objects.filter(treasury=self).count()

    # ✅
    def get_transactions_stock_in_count(self):
        return StockIn.objects.filter(source_treasury=self).count()

    # 🆕
    def get_transactions_stock_in_count_judicial(self):
        return StockInJudicial.objects.filter(source_treasury=self).count()

    # ✅
    def get_transactions_stock_out_count(self):
        return StockOut.objects.filter(source_treasury=self).count()

    # 🆕
    def get_transactions_stock_out_count_judicial(self):
        return StockOutJudicial.objects.filter(source_treasury=self).count()

    # ✅
    def get_transactions_transfers_count(self):
        return Transfer.objects.filter(destination_treasury=self, status='complete').count()

    # 🆕
    def get_transactions_transfers_count_judicial(self):
        return TransferJudicial.objects.filter(destination_treasury=self, status='complete').count()

    # AMOUNTS ----------------------------------------------------------------------------------------------------------

    # ✅
    def get_transfer_amount(self):
        return Transfer.objects.filter(destination_treasury=self, status='complete').aggregate(Sum('amount'))[
            'amount__sum'] or 0

    # 🆕
    def get_transfer_amount_judicial(self):
        return TransferJudicial.objects.filter(destination_treasury=self, status='complete').aggregate(Sum('amount'))[
            'amount__sum'] or 0

    # ✅
    def get_stock_out_amount(self):
        return StockOut.objects.filter(source_treasury=self).aggregate(Sum('amount'))['amount__sum'] or 0

    # 🆕
    def get_stock_out_amount_judicial(self):
        return StockOutJudicial.objects.filter(source_treasury=self).aggregate(Sum('amount'))['amount__sum'] or 0

    # ✅
    def get_stock_in_amount(self):
        return StockIn.objects.filter(source_treasury=self).aggregate(Sum('amount'))['amount__sum'] or 0

    # 🆕
    def get_stock_in_amount_judicial(self):
        return StockInJudicial.objects.filter(source_treasury=self).aggregate(Sum('amount'))['amount__sum'] or 0

    # DENOMINATION COUNTS AND AMOUNTS ----------------------------------------------------------------------------------

    # ✅
    def get_denomination_count(self):
        return self.get_low_denomination_count() + self.get_high_denomination_count()

    # 🆕
    def get_denomination_count_judicial(self):
        return self.get_low_denomination_count_judicial() + self.get_high_denomination_count_judicial()

    # ✅
    def get_low_denomination_count(self):
        return self.s100 + self.s150 + self.s200 + self.s250 + self.s300 + self.s400 + self.s500 + self.s750 + self.s1000

    # 🆕
    def get_low_denomination_count_judicial(self):
        return (
                self.j25 + self.j30 + self.j35 + self.j50 + self.j60 + self.j75 + self.j100 + self.j125 + self.j150 + self.j200 +
                self.j500 + self.j1000)

    # ✅
    def get_high_denomination_count(self):
        return self.s2000 + self.s3000 + self.s5000 + self.s10000 + self.s25000 + self.s50000

    # 🆕
    def get_high_denomination_count_judicial(self):
        return self.j2000 + self.j3000 + self.j5000 + self.j10000 + self.j15000

    # ✅
    def get_denomination_amount(self):
        return self.get_low_denomination_amount() + self.get_high_denomination_amount()

    # 🆕
    def get_denomination_amount_judicial(self):
        return self.get_low_denomination_amount_judicial() + self.get_high_denomination_amount_judicial()

    # ✅
    def get_low_denomination_amount(self):
        return self.s100 * 100 + self.s150 * 150 + self.s200 * 200 + self.s250 * 250 + self.s300 * 300 + self.s400 * 400 + self.s500 * 500 + self.s750 * 750 + self.s1000 * 1000

    # 🆕
    def get_low_denomination_amount_judicial(self):
        return self.j25 * 25 + self.j30 * 30 + self.j35 * 35 + self.j50 * 50 + self.j60 * 60 + self.j75 * 75 + self.j100 * 100 + self.j125 * 125 + self.j150 * 150 + self.j200 * 200 + self.j500 * 500 + self.j1000 * 1000

    # ✅
    def get_high_denomination_amount(self):
        return self.s2000 * 2000 + self.s3000 * 3000 + self.s5000 * 5000 + self.s10000 * 10000 + self.s25000 * 25000 + self.s50000 * 50000

    # 🆕
    def get_high_denomination_amount_judicial(self):
        return self.j2000 * 2000 + self.j3000 * 3000 + self.j5000 * 5000 + self.j10000 * 10000 + self.j15000 * 15000


@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="user_registered")
def on_user_registration(sender, instance, created, **kwargs):
    """
    :TOPIC if user creates at any point the statistics model will be initialized
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    pass
