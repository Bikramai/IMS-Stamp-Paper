import django_filters
from django.forms import TextInput
from django_filters.widgets import RangeWidget

from src.accounts.models import User, Treasury
from src.administration.admins.models import Transaction, StockIn, StockOut, Transfer


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'username'}), lookup_expr='icontains')
    first_name = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'first name'}),
                                           lookup_expr='icontains')
    last_name = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'last name'}), lookup_expr='icontains')
    email = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'email'}), lookup_expr='icontains')

    class Meta:
        model = User
        fields = {'treasury'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.fields['treasury'].empty_label = "Treasury"


class TreasuryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'Name'}), lookup_expr='icontains')

    class Meta:
        model = Treasury
        fields = [
            'name', 'city',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.fields['city'].empty_label = "District"


class StockInFilter(django_filters.FilterSet):
    created_on = django_filters.DateFromToRangeFilter(
        field_name='created_on',
        label='Created On',
        widget=django_filters.widgets.RangeWidget(
            attrs={'type': 'date'}
        )
    )

    class Meta:
        model = StockIn
        fields = ['source_treasury', 'created_on']
        ordering_fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.fields['source_treasury'].empty_label = "Treasury"


class StockOutFilter(django_filters.FilterSet):
    created_on = django_filters.DateFromToRangeFilter(
        field_name='created_on',
        label='Created On',
        widget=django_filters.widgets.RangeWidget(
            attrs={'type': 'date'}
        )
    )

    class Meta:
        model = StockOut
        fields = ['source_treasury', 'created_on']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.fields['source_treasury'].empty_label = "Treasury"


class TransferFilter(django_filters.FilterSet):
    created_on = django_filters.DateFromToRangeFilter(
        field_name='created_on',
        label='Created On',
        widget=django_filters.widgets.RangeWidget(
            attrs={'type': 'date'}
        )
    )

    class Meta:
        model = Transfer
        fields = ['source_treasury', 'destination_treasury', 'created_on']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.fields['source_treasury'].empty_label = "Source Treasury"
        self.form.fields['destination_treasury'].empty_label = "Destination Treasury"


class StockInJudicialFilter(django_filters.FilterSet):
    created_on = django_filters.DateFromToRangeFilter(
        field_name='created_on',
        label='Created On',
        widget=django_filters.widgets.RangeWidget(
            attrs={'type': 'date'}
        )
    )

    class Meta:
        model = StockIn
        fields = ['source_treasury', 'created_on']
        ordering_fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.fields['source_treasury'].empty_label = "Treasury"


class StockOutJudicialFilter(django_filters.FilterSet):
    created_on = django_filters.DateFromToRangeFilter(
        field_name='created_on',
        label='Created On',
        widget=django_filters.widgets.RangeWidget(
            attrs={'type': 'date'}
        )
    )

    class Meta:
        model = StockOut
        fields = ['source_treasury', 'created_on']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.fields['source_treasury'].empty_label = "Treasury"


class TransferJudicialFilter(django_filters.FilterSet):
    created_on = django_filters.DateFromToRangeFilter(
        field_name='created_on',
        label='Created On',
        widget=django_filters.widgets.RangeWidget(
            attrs={'type': 'date'}
        )
    )

    class Meta:
        model = Transfer
        fields = ['source_treasury', 'destination_treasury', 'created_on']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.fields['source_treasury'].empty_label = "Source Treasury"
        self.form.fields['destination_treasury'].empty_label = "Destination Treasury"
