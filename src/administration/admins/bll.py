from src.accounts.models import Treasury
from src.administration.admins.models import Transaction, StockIn, StockOut, Transfer, StockInJudicial, \
    StockOutJudicial, TransferJudicial
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from django.db.models import Sum


def get_specific_value():
    return 27.423


def treasury_denomination_count_and_amount(treasury):
    return treasury.get_denomination_count(), treasury.get_denomination_amount()


def treasury_denomination_count_and_amount_judicial(treasury):
    return treasury.get_denomination_count_judicial(), treasury.get_denomination_amount_judicial()


def treasury_low_denomination_count_and_amount(treasury):
    return treasury.get_low_denomination_count(), treasury.get_low_denomination_amount()


def treasury_low_denomination_count_and_amount_judicial(treasury):
    return treasury.get_low_denomination_count_judicial(), treasury.get_low_denomination_amount_judicial()


def treasury_high_denomination_count_and_amount(treasury):
    return treasury.get_high_denomination_count(), treasury.get_high_denomination_amount()


def treasury_high_denomination_count_and_amount_judicial(treasury):
    return treasury.get_high_denomination_count_judicial(), treasury.get_high_denomination_amount_judicial()


def all_denomination_count_and_amount():
    count = 0
    amount = 0

    for treasury in Treasury.objects.all():
        count_, amount_ = treasury_denomination_count_and_amount(treasury)
        count += count_
        amount += amount_

    return count, amount


def all_denomination_count_and_amount_judicial():
    count = 0
    amount = 0

    for treasury in Treasury.objects.all():
        count_, amount_ = treasury_denomination_count_and_amount_judicial(treasury)
        count += count_
        amount += amount_

    return count, amount


def all_low_denomination_count_and_amount():
    count = 0
    amount = 0

    for treasury in Treasury.objects.all():
        count_, amount_ = treasury_low_denomination_count_and_amount(treasury)
        count += count_
        amount += amount_

    return count, amount


def all_low_denomination_count_and_amount_judicial():
    count = 0
    amount = 0

    for treasury in Treasury.objects.all():
        count_, amount_ = treasury_low_denomination_count_and_amount_judicial(treasury)
        count += count_
        amount += amount_

    return count, amount


def all_high_denomination_count_and_amount():
    count = 0
    amount = 0

    for treasury in Treasury.objects.all():
        count_, amount_ = treasury_high_denomination_count_and_amount(treasury)
        count += count_
        amount += amount_

    return count, amount


def all_high_denomination_count_and_amount_judicial():
    count = 0
    amount = 0

    for treasury in Treasury.objects.all():
        count_, amount_ = treasury_high_denomination_count_and_amount_judicial(treasury)
        count += count_
        amount += amount_

    return count, amount


def get_denomination_query(query=None):
    if query == 'low':
        return all_low_denomination_count_and_amount()

    if query == 'high':
        return all_high_denomination_count_and_amount()

    return all_denomination_count_and_amount()


def get_denomination_query_judicial(query=None):
    if query == 'low':
        return all_low_denomination_count_and_amount_judicial()

    if query == 'high':
        return all_high_denomination_count_and_amount_judicial()

    return all_denomination_count_and_amount_judicial()


def get_dict_total_of_each_column_for_all_treasuries():
    """
    Calculates the total of each column from S100 to S900.
    Returns: A tuple containing the total of each column from S100 to S900.
    Example: total_s100, total_s200, total_s250, .... , total_s5000
    Return dictionary:
    """
    total_s100 = 0
    total_s150 = 0
    total_s200 = 0
    total_s250 = 0
    total_s300 = 0
    total_s400 = 0
    total_s500 = 0
    total_s750 = 0
    total_s1000 = 0
    total_s2000 = 0
    total_s3000 = 0
    total_s5000 = 0
    total_s10000 = 0
    total_s25000 = 0
    total_s50000 = 0

    for treasury in Treasury.objects.all():
        total_s100 += treasury.s100
        total_s150 += treasury.s150
        total_s200 += treasury.s200
        total_s250 += treasury.s250
        total_s300 += treasury.s300
        total_s400 += treasury.s400
        total_s500 += treasury.s500
        total_s750 += treasury.s750
        total_s1000 += treasury.s1000
        total_s2000 += treasury.s2000
        total_s3000 += treasury.s3000
        total_s5000 += treasury.s5000
        total_s10000 += treasury.s10000
        total_s25000 += treasury.s25000
        total_s50000 += treasury.s50000

    context = {
        'total_s100': total_s100,
        'total_s150': total_s150,
        'total_s200': total_s200,
        'total_s250': total_s250,
        'total_s300': total_s300,
        'total_s400': total_s400,
        'total_s500': total_s500,
        'total_s750': total_s750,
        'total_s1000': total_s1000,
        'total_s2000': total_s2000,
        'total_s3000': total_s3000,
        'total_s5000': total_s5000,
        'total_s10000': total_s10000,
        'total_s25000': total_s25000,
        'total_s50000': total_s50000,
    }
    return context


def get_dict_total_of_each_column_for_all_treasuries_judicial():
    """
    judicial [30 35 50 100 500 1000 2000 3000 5000, 10000, 15000]
    """
    # JUDICIAL STAMPS
    total_j25 = 0
    total_j30 = 0
    total_j35 = 0
    total_j50 = 0
    total_j60 = 0
    total_j75 = 0
    total_j100 = 0
    total_j125 = 0
    total_j150 = 0
    total_j200 = 0
    total_j500 = 0
    total_j1000 = 0
    total_j2000 = 0
    total_j3000 = 0
    total_j5000 = 0
    total_j10000 = 0
    total_j15000 = 0

    for treasury in Treasury.objects.all():
        total_j25 += treasury.j25
        total_j30 += treasury.j30
        total_j35 += treasury.j35
        total_j50 += treasury.j50
        total_j60 += treasury.j60
        total_j75 += treasury.j75
        total_j100 += treasury.j100
        total_j125 += treasury.j125
        total_j150 += treasury.j150
        total_j200 += treasury.j200
        total_j500 += treasury.j500
        total_j1000 += treasury.j1000
        total_j2000 += treasury.j2000
        total_j3000 += treasury.j3000
        total_j5000 += treasury.j5000
        total_j10000 += treasury.j10000
        total_j15000 += treasury.j15000

    context = {
        "total_j25": total_j25,
        "total_j30": total_j30,
        "total_j35": total_j35,
        "total_j50": total_j50,
        "total_j60": total_j60,
        "total_j75": total_j75,
        "total_j100": total_j100,
        "total_j125": total_j125,
        "total_j150": total_j150,
        "total_j200": total_j200,
        "total_j500": total_j500,
        "total_j1000": total_j1000,
        "total_j2000": total_j2000,
        "total_j3000": total_j3000,
        "total_j5000": total_j5000,
        "total_j10000": total_j10000,
        "total_j15000": total_j15000,
    }
    return context


""" OVERALL STATISTICS """


def get_overall_stock_in_quantity_and_amount():
    result = StockIn.objects.aggregate(quantity=Sum('quantity'), amount=Sum('amount'))
    quantity = 0
    amount = 0

    try:
        quantity = int(result['quantity']) if result['quantity'] else 0
        amount = int(result['amount']) if result['amount'] else 0
    except (TypeError, ValueError):
        pass

    return quantity, amount


def get_overall_stock_in_quantity_and_amount_judicial():
    result = StockInJudicial.objects.aggregate(quantity=Sum('quantity'), amount=Sum('amount'))
    quantity = 0
    amount = 0

    try:
        quantity = int(result['quantity']) if result['quantity'] else 0
        amount = int(result['amount']) if result['amount'] else 0
    except (TypeError, ValueError):
        pass

    return quantity, amount


def get_overall_stock_out_quantity_and_amount():
    result = StockOut.objects.aggregate(quantity=Sum('quantity'), amount=Sum('amount'))
    quantity = 0
    amount = 0

    try:
        quantity = int(result['quantity']) if result['quantity'] else 0
        amount = int(result['amount']) if result['amount'] else 0
    except (TypeError, ValueError):
        pass

    return quantity, amount


def get_overall_stock_out_quantity_and_amount_judicial():
    result = StockOutJudicial.objects.aggregate(quantity=Sum('quantity'), amount=Sum('amount'))
    quantity = 0
    amount = 0

    try:
        quantity = int(result['quantity']) if result['quantity'] else 0
        amount = int(result['amount']) if result['amount'] else 0
    except (TypeError, ValueError):
        pass

    return quantity, amount


def get_overall_transfer_quantity_and_amount():
    result = Transfer.objects.aggregate(quantity=Sum('quantity'), amount=Sum('amount'))
    quantity = 0
    amount = 0

    try:
        quantity = int(result['quantity']) if result['quantity'] else 0
        amount = int(result['amount']) if result['amount'] else 0
    except (TypeError, ValueError):
        pass

    return quantity, amount


def get_overall_transfer_quantity_and_amount_judicial():
    result = TransferJudicial.objects.aggregate(quantity=Sum('quantity'), amount=Sum('amount'))
    quantity = 0
    amount = 0

    try:
        quantity = int(result['quantity']) if result['quantity'] else 0
        amount = int(result['amount']) if result['amount'] else 0
    except (TypeError, ValueError):
        pass

    return quantity, amount


""" TREASURY STATISTICS"""


def calculate_treasury_total(treasury):
    transactions = Transaction.objects.filter(source_treasury=treasury)
    total = transactions.aggregate(Sum('get_total_amount'))
    return total


def calculate_treasury_count(cls, treasury):
    transactions = cls.objects.filter(source_treasury=treasury)
    count = transactions.count()
    return count


"""STOCK IN STOCK OUT AND TRANSFER  (CALCULATIONS AND VAIDATION """

non_judicial_field_names = [
    's100', 's150', 's200', 's250', 's300', 's400', 's500', 's750', 's1000', 's2000', 's3000', 's5000', 's10000',
    's25000', 's50000'
]

judicial_field_names = [
    'j25', 'j30', 'j35', 'j50', 'j60', 'j75', 'j100', 'j125', 'j150', 'j200', 'j500', 'j1000', 'j2000', 'j3000',
    'j5000',
    'j10000', 'j15000'
]


def stockin_create_calculation(obj):
    source_treasury = Treasury.objects.get(name=obj.source_treasury.name)
    for field_name in non_judicial_field_names:
        field_value = getattr(obj, field_name)
        setattr(source_treasury, field_name, getattr(source_treasury, field_name) + field_value)
        source_treasury.save()


def stockout_create_calculation(obj):
    source_treasury = Treasury.objects.get(pk=obj.source_treasury.pk)
    for field_name in non_judicial_field_names:
        field_value = getattr(obj, field_name)
        setattr(source_treasury, field_name, getattr(source_treasury, field_name) - field_value)
        source_treasury.save()


def transfers_create_calculation(obj):
    source_treasury = Treasury.objects.get(pk=obj.source_treasury.pk)
    destination_treasury = Treasury.objects.get(pk=obj.destination_treasury.pk)
    for field_name in non_judicial_field_names:
        field_value = getattr(obj, field_name)
        setattr(source_treasury, field_name, getattr(source_treasury, field_name) - field_value)
        setattr(destination_treasury, field_name, getattr(destination_treasury, field_name) + field_value)
        source_treasury.save()
        destination_treasury.save()


def stockin_judicial_create_calculation(obj):
    source_treasury = Treasury.objects.get(name=obj.source_treasury.name)
    for field_name in judicial_field_names:
        field_value = getattr(obj, field_name)
        setattr(source_treasury, field_name, getattr(source_treasury, field_name) + field_value)
        source_treasury.save()


def stockout_judicial_create_calculation(obj):
    source_treasury = Treasury.objects.get(pk=obj.source_treasury.pk)
    for field_name in judicial_field_names:
        field_value = getattr(obj, field_name)
        setattr(source_treasury, field_name, getattr(source_treasury, field_name) - field_value)
        source_treasury.save()


def transfers_judicial_create_calculation(obj):
    source_treasury = Treasury.objects.get(pk=obj.source_treasury.pk)
    destination_treasury = Treasury.objects.get(pk=obj.destination_treasury.pk)
    for field_name in judicial_field_names:
        field_value = getattr(obj, field_name)
        setattr(source_treasury, field_name, getattr(source_treasury, field_name) - field_value)
        setattr(destination_treasury, field_name, getattr(destination_treasury, field_name) + field_value)
        source_treasury.save()
        destination_treasury.save()


"""_____________________________Dashboard calculations ______________________________"""


def get_monthly_counts(model, year):
    return (
        model.objects.filter(
            created_on__year=year,
            created_on__month__gte=1,
            created_on__month__lte=12
        )
        .annotate(month=ExtractMonth('created_on'))
        .values('month')
        .annotate(total=Count('id'))
        .order_by('month')
    )


def get_monthly_amounts(model, year):
    return (
        model.objects.filter(
            created_on__year=year,
            created_on__month__gte=1,
            created_on__month__lte=12
        )
        .annotate(month=ExtractMonth('created_on'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )


def get_monthly_counts_treasury(model, year, treasury, is_transfer=False):
    if is_transfer:
        return (
            model.objects.filter(
                created_on__year=year,
                created_on__month__gte=1,
                created_on__month__lte=12,
                destination_treasury=treasury,
                status='complete'
            )
            .annotate(month=ExtractMonth('created_on'))
            .values('month')
            .annotate(total=Count('id'))
            .order_by('month')
        )
    else:
        return (
            model.objects.filter(
                created_on__year=year,
                created_on__month__gte=1,
                created_on__month__lte=12,
                source_treasury=treasury
            )
            .annotate(month=ExtractMonth('created_on'))
            .values('month')
            .annotate(total=Count('id'))
            .order_by('month')
        )


def get_monthly_amounts_treasury(model, year, treasury, is_transfer=False):
    if is_transfer:
        return (
            model.objects.filter(
                created_on__year=year,
                created_on__month__gte=1,
                created_on__month__lte=12,
                destination_treasury=treasury,
                status='complete'
            )
            .annotate(month=ExtractMonth('created_on'))
            .values('month')
            .annotate(total=Sum('amount'))
            .order_by('month')
        )
    else:
        return (
            model.objects.filter(
                created_on__year=year,
                created_on__month__gte=1,
                created_on__month__lte=12,
                source_treasury=treasury
            )
            .annotate(month=ExtractMonth('created_on'))
            .values('month')
            .annotate(total=Sum('amount'))
            .order_by('month')
        )


def get_counts_list(counts):
    counts_list = [0] * 12
    for entry in counts:
        month = entry['month']
        total = entry['total']
        counts_list[month - 1] = total
    return counts_list


def get_sum_and_amount_list_for_all_denominations():
    """
    GET SUM AND TOTAL AMOUNTS OF EACH FIELD FROM s100 - s50000 FOR ALL TREASURES i.e
    sum(S100), sum(150), sum(150), ....... sum(5000)
    sum(s100*price), ........ sum(s50000*price)

    give each of them to to me in context = {} i.e
    {
    'sum100':'',
    'sum150':'',
    .
    .
    'sum50000':'',
    'amount100':'',
    'amount150':'',
    .
    .
    'amount50000':'',
    }
    """
    denominations = [f's{i}' for i in range(100, 50001, 50)]

    # Calculate sums for each field from s100 to s50000
    sums = {}
    amounts = {}

    for denomination in denominations:
        if hasattr(Treasury, denomination):
            sums[denomination] = Treasury.objects.aggregate(sum=Sum(denomination))['sum']
            price = int(denomination[1:])  # Extract the denomination value (e.g., 100, 150, etc.)
            amounts[denomination] = sums[denomination] * price

    # Create a context dictionary
    context = {
        'sums': sums,
        'amounts': amounts,
    }
    return sums, amounts


def get_sum_and_amount_list_for_all_denominations_judicial():
    """['j25', '30', 'j35', 'j50', 'j60', 'j100', 'j125', 'j150', 'j200', 'j500', 'j1000', 'j2000', 'j3000', 'j5000',
        'j10000', 'j15000']"""
    denominations = [
        'j25', 'j30', 'j35', 'j50', 'j60', 'j75', 'j100', 'j125', 'j150', 'j200', 'j500', 'j1000', 'j2000', 'j3000',
        'j5000',
        'j10000', 'j15000']
    sums = {}
    amounts = {}
    for denomination in denominations:
        if hasattr(Treasury, denomination):
            sums[denomination] = Treasury.objects.aggregate(sum=Sum(denomination))['sum']
            price = int(denomination[1:])
            amounts[denomination] = sums[denomination] * price

    return sums, amounts


""" REMOVE STOCK IN FROM INVENTORY """


def calculate_on_stock_in_removed(stock_in):
    treasury = stock_in.source_treasury
    treasury.s100 -= stock_in.s100
    treasury.s150 -= stock_in.s150
    treasury.s200 -= stock_in.s200
    treasury.s250 -= stock_in.s250
    treasury.s300 -= stock_in.s300
    treasury.s400 -= stock_in.s400
    treasury.s500 -= stock_in.s500
    treasury.s750 -= stock_in.s750
    treasury.s1000 -= stock_in.s1000
    treasury.s2000 -= stock_in.s2000
    treasury.s3000 -= stock_in.s3000
    treasury.s5000 -= stock_in.s5000
    treasury.s10000 -= stock_in.s10000
    treasury.s25000 -= stock_in.s25000
    treasury.s50000 -= stock_in.s50000
    treasury.save()


def calculate_on_stock_out_removed(stock_out):
    treasury = stock_out.source_treasury
    treasury.s100 += stock_out.s100
    treasury.s150 += stock_out.s150
    treasury.s200 += stock_out.s200
    treasury.s250 += stock_out.s250
    treasury.s300 += stock_out.s300
    treasury.s400 += stock_out.s400
    treasury.s500 += stock_out.s500
    treasury.s750 += stock_out.s750
    treasury.s1000 += stock_out.s1000
    treasury.s2000 += stock_out.s2000
    treasury.s3000 += stock_out.s3000
    treasury.s5000 += stock_out.s5000
    treasury.s10000 += stock_out.s10000
    treasury.s25000 += stock_out.s25000
    treasury.s50000 += stock_out.s50000
    treasury.save()


def calculate_on_stock_in_removed_judicial(stock_in):
    treasury = stock_in.source_treasury
    treasury.j25 -= stock_in.j25
    treasury.j30 -= stock_in.j30
    treasury.j35 -= stock_in.j35
    treasury.j50 -= stock_in.j50
    treasury.j60 -= stock_in.j60
    treasury.j75 -= stock_in.j75
    treasury.j100 -= stock_in.j100
    treasury.j125 -= stock_in.j125
    treasury.j150 -= stock_in.j150
    treasury.j200 -= stock_in.j200
    treasury.j500 -= stock_in.j500
    treasury.j1000 -= stock_in.j1000
    treasury.j2000 -= stock_in.j2000
    treasury.j3000 -= stock_in.j3000
    treasury.j5000 -= stock_in.j5000
    treasury.j10000 -= stock_in.j10000
    treasury.j15000 -= stock_in.j15000
    treasury.save()


def calculate_on_stock_out_removed_judicial(stock_out):
    treasury = stock_out.source_treasury
    treasury.j25 -= stock_out.j25
    treasury.j30 -= stock_out.j30
    treasury.j35 -= stock_out.j35
    treasury.j50 -= stock_out.j50
    treasury.j60 -= stock_out.j60
    treasury.j75 -= stock_out.j75
    treasury.j100 -= stock_out.j100
    treasury.j125 -= stock_out.j125
    treasury.j150 -= stock_out.j150
    treasury.j200 -= stock_out.j200
    treasury.j500 -= stock_out.j500
    treasury.j1000 -= stock_out.j1000
    treasury.j2000 -= stock_out.j2000
    treasury.j3000 -= stock_out.j3000
    treasury.j5000 -= stock_out.j5000
    treasury.j10000 -= stock_out.j10000
    treasury.j15000 -= stock_out.j15000
    treasury.save()
