from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, Submit
from django import forms
from django.forms import ModelForm
from django.utils import timezone
from src.administration.admins.models import StockIn, StockOut, Transfer, StockInJudicial, StockOutJudicial, \
    TransferJudicial


class Row(Div):
    css_class = "row"


non_judicial_field_names = [
    's100', 's150', 's200', 's250', 's300', 's400', 's500', 's750', 's1000', 's2000', 's3000', 's5000', 's10000',
    's25000', 's50000'
]

judicial_field_names = [
    'j25', 'j30', 'j35', 'j50', 'j60', 'j75', 'j100', 'j125', 'j150', 'j200', 'j500', 'j1000', 'j2000', 'j3000',
    'j5000', 'j10000', 'j15000'
]


class StockInForm(forms.ModelForm):
    class Meta:
        model = StockIn
        fields = [
            's100', 's150', 's200', 's250', 's300', 's400', 's500',
            's750', 's1000', 's2000', 's3000', 's5000', 's10000', 's25000', 's50000', 'created_on'
        ]
        widgets = {
            'created_on': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('s100', css_class='col-sm-4 '),
                Column('s150', css_class='col-sm-4 '),
                Column('s200', css_class='col-sm-4 '),
                Column('s250', css_class='col-sm-4 '),
                Column('s300', css_class='col-sm-4 '),
                Column('s400', css_class='col-sm-4 '),
                Column('s500', css_class='col-sm-4 '),
                Column('s750', css_class='col-sm-4 '),
                Column('s1000', css_class='col-sm-4 '),
                Column('s2000', css_class='col-sm-4 '),
                Column('s3000', css_class='col-sm-4 '),
                Column('s5000', css_class='col-sm-4 '),
                Column('s10000', css_class='col-sm-4 '),
                Column('s25000', css_class='col-sm-4 '),
                Column('s50000', css_class='col-sm-4 '),
                Column('created_on', css_class='col-sm-12')

            ),
            Submit('submit', 'Submit', css_class='btn btn-primary float-right')
        )

    def clean_created_on(self):
        created_on = self.cleaned_data['created_on']
        if not created_on:
            created_on = timezone.now()
        else:
            if created_on.date() < timezone.now().date():
                raise forms.ValidationError("⏰🚀 Oops! Time-traveling detected! You can't add a record in the past.")
        return created_on

    def clean(self):
        cleaned_data = super().clean()

        if all(field_value == 0 for field_name, field_value in cleaned_data.items() if field_name.startswith('s')):
            raise forms.ValidationError("At least one item is required to process this transaction")

        return cleaned_data


class StockOutForm(ModelForm):
    class Meta:
        model = StockOut
        fields = ['s100', 's150', 's200', 's250', 's300', 's400', 's500',
                  's750', 's1000',
                  's2000', 's3000', 's5000', 's10000', 's25000', 's50000', 'created_on',
                  'name', 'challan_number', 'challan_date', 'phone', 'type_of_transaction', 'serial_number'
                  ]
        widgets = {
            'created_on': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'challan_date': forms.DateTimeInput(attrs={'type': 'date'}),
        }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('s100', css_class='col-sm-4 '),
                Column('s150', css_class='col-sm-4 '),
                Column('s200', css_class='col-sm-4 '),
                Column('s250', css_class='col-sm-4 '),
                Column('s300', css_class='col-sm-4 '),
                Column('s400', css_class='col-sm-4 '),
                Column('s500', css_class='col-sm-4 '),
                Column('s750', css_class='col-sm-4 '),
                Column('s1000', css_class='col-sm-4 '),
                Column('s2000', css_class='col-sm-4 '),
                Column('s3000', css_class='col-sm-4 '),
                Column('s5000', css_class='col-sm-4 '),
                Column('s10000', css_class='col-sm-4 '),
                Column('s25000', css_class='col-sm-4 '),
                Column('s50000', css_class='col-sm-4 '),
                Column('created_on', css_class='col-sm-12'),
                Column('name', css_class='col-sm-4'),
                Column('phone', css_class='col-sm-4'),
                Column('type_of_transaction', css_class='col-sm-4'),
                Column('challan_number', css_class='col-sm-4'),
                Column('challan_date', css_class='col-sm-4'),
                Column('serial_number', css_class='col-sm-4'),
            ),
            Submit('submit', 'Submit', css_class='btn btn-primary float-right')
        )

    def clean(self):
        cleaned_data = super().clean()
        treasury = self.request.user.treasury

        # Check if all fields from s100 to s50000 contain zero
        if all(field_value == 0 for field_name, field_value in cleaned_data.items() if field_name.startswith('s')):
            raise forms.ValidationError("At least one item is required to process this transaction")

        for field_name in non_judicial_field_names:
            field_value = cleaned_data.get(field_name)
            treasury_field = getattr(treasury, field_name)
            if field_value > treasury_field:
                self.add_error(field_name, f"Requested Quantity is Greater than avaliable stock ( {treasury_field} )")
        return cleaned_data


class TransferForm(ModelForm):
    class Meta:
        model = Transfer
        fields = ['s100', 's150', 's200', 's250', 's300', 's400', 's500',
                  's750', 's1000',
                  's2000', 's3000', 's5000', 's10000', 's25000', 's50000', 'created_on']
        widgets = {
            'created_on': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('s100', css_class='col-sm-4 '),
                Column('s150', css_class='col-sm-4 '),
                Column('s200', css_class='col-sm-4 '),
                Column('s250', css_class='col-sm-4 '),
                Column('s300', css_class='col-sm-4 '),
                Column('s400', css_class='col-sm-4 '),
                Column('s500', css_class='col-sm-4 '),
                Column('s750', css_class='col-sm-4 '),
                Column('s1000', css_class='col-sm-4 '),
                Column('s2000', css_class='col-sm-4 '),
                Column('s3000', css_class='col-sm-4 '),
                Column('s5000', css_class='col-sm-4 '),
                Column('s10000', css_class='col-sm-4 '),
                Column('s25000', css_class='col-sm-4 '),
                Column('s50000', css_class='col-sm-4 '),
                Column('created_on', css_class='col-sm-12')
            ),
            Submit('submit', 'Submit', css_class='btn btn-primary float-right')
        )

    def clean(self):
        cleaned_data = super().clean()
        # Check if all fields from s100 to s50000 contain zero
        if all(field_value == 0 for field_name, field_value in cleaned_data.items() if field_name.startswith('s')):
            raise forms.ValidationError("At least one item is required to process this transaction")
        return cleaned_data

    def clean_created_on(self):
        created_on = self.cleaned_data['created_on']
        if created_on:

            if created_on.date() < timezone.now().date():
                raise forms.ValidationError("Date cannot be in the past")
        return created_on


class StockInJudicialForm(forms.ModelForm):
    class Meta:
        model = StockInJudicial
        fields = [
            'j25', 'j30', 'j35', 'j50', 'j60', 'j75', 'j100', 'j125', 'j150', 'j200',
            'j500', 'j1000', 'j2000', 'j3000', 'j5000', 'j10000', 'j15000', 'created_on'
        ]
        widgets = {
            'created_on': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('j25', css_class='col-sm-4 '),
                Column('j30', css_class='col-sm-4 '),
                Column('j35', css_class='col-sm-4 '),
                Column('j50', css_class='col-sm-4 '),
                Column('j60', css_class='col-sm-4 '),
                Column('j75', css_class='col-sm-4 '),
                Column('j100', css_class='col-sm-4 '),
                Column('j125', css_class='col-sm-4 '),
                Column('j150', css_class='col-sm-4 '),
                Column('j200', css_class='col-sm-4 '),
                Column('j500', css_class='col-sm-4 '),
                Column('j1000', css_class='col-sm-4 '),
                Column('j2000', css_class='col-sm-4 '),
                Column('j3000', css_class='col-sm-4 '),
                Column('j5000', css_class='col-sm-4 '),
                Column('j10000', css_class='col-sm-4 '),
                Column('j15000', css_class='col-sm-4 '),

                Column('created_on', css_class='col-sm-12 '),

            ),
            Submit('submit', 'Submit', css_class='btn btn-primary float-right')
        )

    def clean_created_on(self):
        created_on = self.cleaned_data['created_on']
        if created_on:
            if created_on.date() < timezone.now().date():
                raise forms.ValidationError("⏰🚀 Oops! Time-traveling detected! You can't add a record in the past.")
        return created_on

    def clean(self):
        cleaned_data = super().clean()

        if all(field_value == 0 for field_name, field_value in cleaned_data.items() if field_name.startswith('j')):
            raise forms.ValidationError("At least one item is required to process this transaction")

        return cleaned_data


class StockOutJudicialForm(ModelForm):
    class Meta:
        model = StockOutJudicial
        fields = [
            'j25', 'j30', 'j35', 'j50', 'j60', 'j75', 'j100', 'j125', 'j150', 'j200',
            'j500', 'j1000', 'j2000', 'j3000', 'j5000', 'j10000', 'j15000', 'created_on',
            'name', 'challan_number', 'challan_date', 'phone', 'type_of_transaction', 'serial_number'
        ]
        widgets = {
            'created_on': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'challan_date': forms.DateTimeInput(attrs={'type': 'date'}),
        }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('j25', css_class='col-sm-4 '),
                Column('j30', css_class='col-sm-4 '),
                Column('j35', css_class='col-sm-4 '),
                Column('j50', css_class='col-sm-4 '),
                Column('j60', css_class='col-sm-4 '),
                Column('j75', css_class='col-sm-4 '),
                Column('j100', css_class='col-sm-4 '),
                Column('j125', css_class='col-sm-4 '),
                Column('j150', css_class='col-sm-4 '),
                Column('j200', css_class='col-sm-4 '),
                Column('j500', css_class='col-sm-4 '),
                Column('j1000', css_class='col-sm-4 '),
                Column('j2000', css_class='col-sm-4 '),
                Column('j3000', css_class='col-sm-4 '),
                Column('j5000', css_class='col-sm-4 '),
                Column('j10000', css_class='col-sm-4 '),
                Column('j15000', css_class='col-sm-4 '),

                Column('created_on', css_class='col-sm-12'),
                Column('name', css_class='col-sm-4'),
                Column('phone', css_class='col-sm-4'),
                Column('type_of_transaction', css_class='col-sm-4'),
                Column('challan_number', css_class='col-sm-4'),
                Column('challan_date', css_class='col-sm-4'),
                Column('serial_number', css_class='col-sm-4'),

            ),
            Submit('submit', 'Submit', css_class='btn btn-primary float-right')
        )

    def clean(self):
        cleaned_data = super().clean()
        treasury = self.request.user.treasury

        if all(field_value == 0 for field_name, field_value in cleaned_data.items() if field_name.startswith('s')):
            raise forms.ValidationError("At least one item is required to process this transaction")

        for field_name in judicial_field_names:
            field_value = cleaned_data.get(field_name)
            treasury_field = getattr(treasury, field_name)
            if field_value > treasury_field:
                self.add_error(field_name, f"Requested Quantity is Greater than avaliable stock ( {treasury_field} )")
        return cleaned_data


class TransferJudicialForm(ModelForm):
    class Meta:
        model = TransferJudicial
        fields = ['j25', 'j30', 'j35', 'j50', 'j60', 'j75', 'j100', 'j125', 'j150', 'j200',
                  'j500', 'j1000', 'j2000', 'j3000', 'j5000', 'j10000', 'j15000', 'created_on']
        widgets = {
            'created_on': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('j25', css_class='col-sm-4 '),
                Column('j30', css_class='col-sm-4 '),
                Column('j35', css_class='col-sm-4 '),
                Column('j50', css_class='col-sm-4 '),
                Column('j60', css_class='col-sm-4 '),
                Column('j75', css_class='col-sm-4 '),
                Column('j100', css_class='col-sm-4 '),
                Column('j125', css_class='col-sm-4 '),
                Column('j150', css_class='col-sm-4 '),
                Column('j200', css_class='col-sm-4 '),
                Column('j500', css_class='col-sm-4 '),
                Column('j1000', css_class='col-sm-4 '),
                Column('j2000', css_class='col-sm-4 '),
                Column('j3000', css_class='col-sm-4 '),
                Column('j5000', css_class='col-sm-4 '),
                Column('j10000', css_class='col-sm-4 '),
                Column('j15000', css_class='col-sm-4 '),
                Column('created_on', css_class='col-sm-12 '),

            ),
            Submit('submit', 'Submit', css_class='btn btn-primary float-right')
        )

    def clean(self):
        cleaned_data = super().clean()
        # Check if all fields from s100 to s50000 contain zero
        if all(field_value == 0 for field_name, field_value in cleaned_data.items() if field_name.startswith('j')):
            raise forms.ValidationError("At least one item is required to process this transaction")
        return cleaned_data

    def clean_created_on(self):
        created_on = self.cleaned_data['created_on']
        if created_on:

            if created_on.date() < timezone.now().date():
                raise forms.ValidationError("Date cannot be in the past")
        return created_on
