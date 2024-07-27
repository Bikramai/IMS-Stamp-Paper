from django.contrib import admin
from .models import (
    StockIn, StockOut, Transfer, Transaction, StockInJudicial, StockOutJudicial, TransactionJudicial, TransferJudicial
)


""" NON JUDICIAL """


@admin.register(StockIn)
class StockInAdmin(admin.ModelAdmin):
    list_display = ['source_treasury', 'amount', 'quantity', 'user', 'status', 'created_on']
    list_filter = ['status']
    search_fields = ['source_treasury__name']
    fieldsets = (
        (None, {'fields': ('source_treasury', 'amount', 'quantity', 'user', 'status')}),
        ('Non Judicial', {'fields': (
        's100', 's150', 's200', 's250', 's300', 's400', 's500', 's750', 's1000', 's2000', 's3000', 's5000', 's10000',
        's25000', 's50000')}),
    )


@admin.register(StockOut)
class StockOutAdmin(admin.ModelAdmin):
    list_display = ['source_treasury', 'amount', 'quantity', 'user', 'challan_number', 'status', 'created_on']
    list_filter = ['status']
    search_fields = ['source_treasury__name']
    fieldsets = (
        (None, {'fields': ('source_treasury', 'amount', 'quantity', 'user', 'status')}),
        ('Non Judicial', {'fields': (
        's100', 's150', 's200', 's250', 's300', 's400', 's500', 's750', 's1000', 's2000', 's3000', 's5000', 's10000',
        's25000', 's50000')}),
        ('Extra Details',
         {'fields': ('name', 'phone', 'challan_number', 'challan_date', 'type_of_transaction', 'serial_number')}),
    )


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ['source_treasury', 'destination_treasury', 'amount', 'quantity', 'user', 'status', 'created_on']
    list_filter = ['status']
    search_fields = ['source_treasury__name', 'destination_treasury__name']
    fieldsets = (
        (None, {'fields': ('source_treasury', 'destination_treasury', 'amount', 'quantity', 'user', 'status')}),
        ('Non Judicial', {'fields': (
        's100', 's150', 's200', 's250', 's300', 's400', 's500', 's750', 's1000', 's2000', 's3000', 's5000', 's10000',
        's25000', 's50000')}),

    )


""" JUDICIAL """


@admin.register(StockInJudicial)
class StockInJudicialAdmin(admin.ModelAdmin):
    list_display = ['source_treasury', 'amount', 'quantity', 'user', 'status', 'created_on']
    list_filter = ['status']
    search_fields = ['source_treasury__name']
    fieldsets = (
        (None, {'fields': ('source_treasury', 'amount', 'quantity', 'user', 'status')}),
        ('Judicial',
         {'fields': ('j30', 'j35', 'j50', 'j100', 'j500', 'j1000', 'j2000', 'j3000', 'j5000', 'j10000', 'j15000')}),
    )


@admin.register(StockOutJudicial)
class StockOutJudicialAdmin(admin.ModelAdmin):
    list_display = ['source_treasury', 'amount', 'quantity', 'user', 'challan_number', 'status', 'created_on']
    list_filter = ['status']
    search_fields = ['source_treasury__name']
    fieldsets = (
        (None, {'fields': ('source_treasury', 'amount', 'quantity', 'user', 'status')}),
        ('Judicial',
         {'fields': ('j30', 'j35', 'j50', 'j100', 'j500', 'j1000', 'j2000', 'j3000', 'j5000', 'j10000', 'j15000')}),
        ('Extra Details',
         {'fields': ('name', 'phone', 'challan_number', 'challan_date', 'type_of_transaction', 'serial_number')}),
    )


@admin.register(TransferJudicial)
class TransferJudicialAdmin(admin.ModelAdmin):
    list_display = ['source_treasury', 'destination_treasury', 'amount', 'quantity', 'user', 'status', 'created_on']
    list_filter = ['status']
    search_fields = ['source_treasury__name', 'destination_treasury__name']
    fieldsets = (
        (None, {'fields': ('source_treasury', 'destination_treasury', 'amount', 'quantity', 'user', 'status')}),
        ('Judicial', {'fields': ('j30', 'j35', 'j50', 'j100', 'j500', 'j1000', 'j2000', 'j3000', 'j5000', 'j10000',
                                 'j15000')}),

    )
