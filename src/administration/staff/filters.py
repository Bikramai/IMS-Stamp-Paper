import django_filters
from django_filters.widgets import RangeWidget

from src.administration.admins.models import Transaction, StockIn, StockOut, Transfer, StockInJudicial, \
    StockOutJudicial, TransferJudicial


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
        fields = ['created_on']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


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
        fields = ['created_on']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


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
        fields = ['source_treasury', 'created_on']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.fields['source_treasury'].empty_label = "Source Treasury"


class StockInJudicialFilter(django_filters.FilterSet):
    created_on = django_filters.DateFromToRangeFilter(
        field_name='created_on',
        label='Created On',
        widget=django_filters.widgets.RangeWidget(
            attrs={'type': 'date'}
        )
    )

    class Meta:
        model = StockInJudicial
        fields = ['created_on']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class StockOutJudicialFilter(django_filters.FilterSet):
    created_on = django_filters.DateFromToRangeFilter(
        field_name='created_on',
        label='Created On',
        widget=django_filters.widgets.RangeWidget(
            attrs={'type': 'date'}
        )
    )

    class Meta:
        model = StockOutJudicial
        fields = ['created_on']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TransferJudicialFilter(django_filters.FilterSet):
    created_on = django_filters.DateFromToRangeFilter(
        field_name='created_on',
        label='Created On',
        widget=django_filters.widgets.RangeWidget(
            attrs={'type': 'date'}
        )
    )

    class Meta:
        model = TransferJudicial
        fields = ['source_treasury', 'created_on']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.fields['source_treasury'].empty_label = "Source Treasury"
