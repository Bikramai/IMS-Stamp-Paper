from django.core.exceptions import ValidationError
from django.db import models

from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


def validate_cnic(value):
    if len(str(value)) != 13:
        raise ValidationError("CNIC must contains 13 digits without any dashes '-' ")

    if not str(value).isdigit():
        raise ValidationError("CNIC must contains only digits")

    return value


""" TRANSACTION NON JUDICIAL """


class Transaction(models.Model):
    STATUS_CHOICE = (
        ('pending', 'Pending'),
        ('working', 'Working'),
        ('complete', 'Complete'),
        ('cancelled', 'Cancelled'),
    )
    source_treasury = models.ForeignKey(
        'accounts.Treasury', on_delete=models.SET_NULL, null=True, blank=False,
        verbose_name='Treasury',
    )

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

    amount = models.FloatField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey('accounts.User', models.SET_NULL, null=True, blank=True)

    created_on = models.DateTimeField(blank=True, null=False,
                                      help_text="Leave it blank to get the current date and time.")
    status = models.CharField(default='pending', max_length=100, choices=STATUS_CHOICE)

    class Meta:
        ordering = ['-created_on']
        abstract = True

    def save(self, *args, **kwargs):
        total = self.s100 * 100 + self.s150 * 150 + self.s200 * 200 + self.s250 * 250 + self.s300 * 300 + self.s400 * 400 + self.s500 * 500 + self.s750 * 750 + self.s1000 * 1000 + self.s2000 * 2000 + self.s3000 * 3000 + self.s5000 * 5000 + self.s10000 * 10000 + self.s25000 * 25000 + self.s50000 * 50000
        count = self.s100 + self.s150 + self.s200 + self.s250 + self.s300 + self.s400 + self.s500 + self.s750 + self.s1000 + self.s2000 + self.s3000 + self.s5000 + self.s10000 + self.s25000 + self.s50000
        self.amount = total
        self.quantity = count

        if self.created_on is None:
            self.created_on = timezone.now()

        super().save(*args, **kwargs)


class StockIn(Transaction):
    class Meta:
        verbose_name = "Stock In (Non Judicial)"
        verbose_name_plural = "Stock In (Non Judicial)"
        ordering = ['-created_on']

    def __str__(self):
        return str(self.source_treasury)


class StockOut(Transaction):
    name = models.CharField(max_length=255, verbose_name="Purchaser Name", null=True, blank=True)
    challan_number = models.CharField(
        max_length=13, verbose_name="Challan Number", null=True, blank=True,
    )
    challan_date = models.DateField(verbose_name="Challan Date", null=True, blank=True)
    phone = PhoneNumberField(region='PK', verbose_name="Purchaser Phone", null=True, blank=True)
    type_of_transaction = models.CharField(max_length=255, null=True, blank=True)
    serial_number = models.CharField(max_length=255, null=True, blank=True, verbose_name="Serial Number")

    class Meta:
        verbose_name = "Stock Out (Non Judicial)"
        verbose_name_plural = "Stock Out (Non Judicial)"
        ordering = ['-created_on']

    def __str__(self):
        return str(self.source_treasury)


class Transfer(Transaction):
    source_treasury = models.ForeignKey('accounts.Treasury', on_delete=models.SET_NULL, null=True, blank=False,
                                        related_name='source_transfers_non_judicial')
    destination_treasury = models.ForeignKey('accounts.Treasury', on_delete=models.SET_NULL, null=True, blank=False,
                                             related_name='destination_transfers_non_judicial')

    class Meta:
        verbose_name = "Transfer (Non Judicial)"
        verbose_name_plural = "Transfer (Non Judicial)"
        ordering = ['-created_on']

    def __str__(self):
        return str(self.source_treasury)


""" TRANSACTION JUDICIAL """


class TransactionJudicial(models.Model):
    STATUS_CHOICE = (
        ('pending', 'Pending'),
        ('working', 'Working'),
        ('complete', 'Complete'),
        ('cancelled', 'Cancelled'),
    )
    source_treasury = models.ForeignKey(
        'accounts.Treasury', on_delete=models.SET_NULL, null=True, blank=False,
        verbose_name='Treasury',
    )

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

    amount = models.FloatField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey('accounts.User', models.SET_NULL, null=True, blank=True)

    created_on = models.DateTimeField(blank=True, null=False,
                                      help_text="Leave it blank to get the current date and time.")
    status = models.CharField(default='pending', max_length=100, choices=STATUS_CHOICE)

    class Meta:
        ordering = ['-created_on']
        abstract = True

    def save(self, *args, **kwargs):
        total = self.j25 * 25 + self.j30 * 30 + self.j35 * 35 + self.j50 * 50 + self.j60 * 60 + self.j75 * 75 + self.j100 * 100 + self.j125 * 125 + self.j150 * 150 + self.j200 * 200 + self.j500 * 500 + self.j1000 * 1000 + self.j2000 * 2000 + self.j3000 * 3000 + self.j5000 * 5000 + self.j10000 * 10000 + self.j15000 * 15000
        count = self.j25 + self.j30 + self.j35 + self.j50 + self.j60 + self.j75 + self.j100 + self.j125 + self.j150 + self.j200 + self.j500 + self.j1000 + self.j2000 + self.j3000 + self.j5000 + self.j10000 + self.j15000

        self.amount = total
        self.quantity = count

        if self.created_on is None:
            self.created_on = timezone.now()

        super().save(*args, **kwargs)


class StockInJudicial(TransactionJudicial):
    class Meta:
        verbose_name = "Stock In (Judicial)"
        verbose_name_plural = "Stock In (Judicial)"
        ordering = ['-created_on']

    def __str__(self):
        return str(self.source_treasury)


class StockOutJudicial(TransactionJudicial):
    name = models.CharField(max_length=255, verbose_name="Purchaser Name", null=True, blank=True)
    challan_number = models.CharField(
        max_length=13, verbose_name="Challan Number", null=True, blank=True,
    )
    challan_date = models.DateField(verbose_name="Challan Date", null=True, blank=True)
    phone = PhoneNumberField(region='PK', verbose_name="Purchaser Phone", null=True, blank=True)
    type_of_transaction = models.CharField(max_length=255, null=True, blank=True)
    serial_number = models.CharField(max_length=255, null=True, blank=True, verbose_name="Serial Number")

    class Meta:
        verbose_name = "Stock Out (Judicial)"
        verbose_name_plural = "Stock Out (Judicial)"
        ordering = ['-created_on']

    def __str__(self):
        return str(self.source_treasury)


class TransferJudicial(TransactionJudicial):
    source_treasury = models.ForeignKey('accounts.Treasury', on_delete=models.SET_NULL, null=True, blank=False,
                                        related_name='source_transfers_judicial')
    destination_treasury = models.ForeignKey('accounts.Treasury', on_delete=models.SET_NULL, null=True, blank=False,
                                             related_name='destination_transfers_judicial')

    class Meta:
        verbose_name = "Transfer (Judicial)"
        verbose_name_plural = "Transfer (Judicial)"
        ordering = ['-created_on']

    def __str__(self):
        return str(self.source_treasury)
