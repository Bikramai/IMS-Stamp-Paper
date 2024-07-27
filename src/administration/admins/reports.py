from datetime import datetime

from django.db.models import Sum
from django.utils import timezone

from src.accounts.models import Treasury
from src.administration.admins.dll import ReportNonJudicial, ReportJudicial, ReportConsolidated
from src.administration.admins.models import StockIn, StockOut, Transfer, StockOutJudicial, StockInJudicial, TransferJudicial


def get_complete_reports_for_non_judicial(date, treasury_name=None, denomination="full"):

    # TREASURY QUERY
    if treasury_name:
        treasuries = Treasury.objects.filter(name__icontains=treasury_name)
    else:
        treasuries = Treasury.objects.all()

    if date:
        naive_datetime = datetime.strptime(date, '%Y-%m-%dT%H:%M')
        timezone_aware_datetime = timezone.make_aware(naive_datetime, timezone.get_current_timezone())
        date = timezone_aware_datetime
    else:
        date = timezone.now()

    treasuries_data = []
    quantities_data = ReportNonJudicial(
        "Quantities", 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0
    )
    amounts_data = ReportNonJudicial(
        "Amounts", 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0
    )
    total_amounts = 0
    total_counts = 0

    for treasury in treasuries:
        stock_in_q1 = StockIn.objects.filter(created_on__lte=date, source_treasury=treasury)
        stock_out_q1 = StockOut.objects.filter(created_on__lte=date, source_treasury=treasury)
        stock_transfer_from_q1 = Transfer.objects.filter(created_on__lte=date, source_treasury=treasury,
                                                         status="complete")
        stock_transfer_to_q1 = Transfer.objects.filter(created_on__lte=date, destination_treasury=treasury,
                                                       status="complete")

        if stock_transfer_to_q1.exists():
            stock_transfer_to_q2 = stock_transfer_to_q1.aggregate(
                s100=Sum('s100'), s150=Sum('s150'), s200=Sum('s200'), s250=Sum('s250'),
                s300=Sum('s300'), s400=Sum('s400'), s500=Sum('s500'), s750=Sum('s750'),
                s1000=Sum('s1000'), s2000=Sum('s2000'), s3000=Sum('s3000'), s5000=Sum('s5000'),
                s10000=Sum('s10000'), s25000=Sum('s25000'), s50000=Sum('s50000')
            )
        else:
            stock_transfer_to_q2 = {
                's100': 0, 's150': 0, 's200': 0, 's250': 0, 's300': 0, 's400': 0, 's500': 0, 's750': 0,
                's1000': 0, 's2000': 0, 's3000': 0, 's5000': 0, 's10000': 0, 's25000': 0, 's50000': 0
            }

        if stock_transfer_from_q1.exists():
            stock_transfer_from_q2 = stock_transfer_from_q1.aggregate(
                s100=Sum('s100'), s150=Sum('s150'), s200=Sum('s200'), s250=Sum('s250'),
                s300=Sum('s300'), s400=Sum('s400'), s500=Sum('s500'), s750=Sum('s750'),
                s1000=Sum('s1000'), s2000=Sum('s2000'), s3000=Sum('s3000'), s5000=Sum('s5000'),
                s10000=Sum('s10000'), s25000=Sum('s25000'), s50000=Sum('s50000')
            )
        else:
            stock_transfer_from_q2 = {
                's100': 0, 's150': 0, 's200': 0, 's250': 0, 's300': 0, 's400': 0, 's500': 0, 's750': 0,
                's1000': 0, 's2000': 0, 's3000': 0, 's5000': 0, 's10000': 0, 's25000': 0, 's50000': 0
            }

        if stock_in_q1.exists():
            stock_in_q2 = stock_in_q1.aggregate(
                s100=Sum('s100'), s150=Sum('s150'), s200=Sum('s200'), s250=Sum('s250'),
                s300=Sum('s300'), s400=Sum('s400'), s500=Sum('s500'), s750=Sum('s750'),
                s1000=Sum('s1000'), s2000=Sum('s2000'), s3000=Sum('s3000'), s5000=Sum('s5000'),
                s10000=Sum('s10000'), s25000=Sum('s25000'), s50000=Sum('s50000')
            )
        else:
            stock_in_q2 = {
                's100': 0, 's150': 0, 's200': 0, 's250': 0, 's300': 0, 's400': 0, 's500': 0, 's750': 0,
                's1000': 0, 's2000': 0, 's3000': 0, 's5000': 0, 's10000': 0, 's25000': 0, 's50000': 0
            }

        if stock_out_q1.exists():
            stock_out_q2 = stock_out_q1.aggregate(
                s100=Sum('s100'), s150=Sum('s150'), s200=Sum('s200'), s250=Sum('s250'),
                s300=Sum('s300'), s400=Sum('s400'), s500=Sum('s500'), s750=Sum('s750'),
                s1000=Sum('s1000'), s2000=Sum('s2000'), s3000=Sum('s3000'), s5000=Sum('s5000'),
                s10000=Sum('s10000'), s25000=Sum('s25000'), s50000=Sum('s50000')
            )
        else:
            stock_out_q2 = {
                's100': 0, 's150': 0, 's200': 0, 's250': 0, 's300': 0, 's400': 0, 's500': 0, 's750': 0,
                's1000': 0, 's2000': 0, 's3000': 0, 's5000': 0, 's10000': 0, 's25000': 0, 's50000': 0
            }

        _stock_transfer_to_model = ReportNonJudicial(
            "Stock Transfer To", stock_transfer_to_q2['s100'], stock_transfer_to_q2['s150'], stock_transfer_to_q2['s200'],
            stock_transfer_to_q2['s250'], stock_transfer_to_q2['s300'], stock_transfer_to_q2['s400'],
            stock_transfer_to_q2['s500'], stock_transfer_to_q2['s750'], stock_transfer_to_q2['s1000'],
            stock_transfer_to_q2['s2000'], stock_transfer_to_q2['s3000'], stock_transfer_to_q2['s5000'],
            stock_transfer_to_q2['s10000'], stock_transfer_to_q2['s25000'], stock_transfer_to_q2['s50000']
        )
        _stock_transfer_from_model = ReportNonJudicial(
            "Stock Transfer From", stock_transfer_from_q2['s100'], stock_transfer_from_q2['s150'],
            stock_transfer_from_q2['s200'], stock_transfer_from_q2['s250'], stock_transfer_from_q2['s300'],
            stock_transfer_from_q2['s400'], stock_transfer_from_q2['s500'], stock_transfer_from_q2['s750'],
            stock_transfer_from_q2['s1000'], stock_transfer_from_q2['s2000'], stock_transfer_from_q2['s3000'],
            stock_transfer_from_q2['s5000'], stock_transfer_from_q2['s10000'], stock_transfer_from_q2['s25000'],
            stock_transfer_from_q2['s50000']
        )
        _stock_in_model = ReportNonJudicial(
            "Stock In", stock_in_q2['s100'], stock_in_q2['s150'], stock_in_q2['s200'], stock_in_q2['s250'],
            stock_in_q2['s300'], stock_in_q2['s400'], stock_in_q2['s500'], stock_in_q2['s750'],
            stock_in_q2['s1000'], stock_in_q2['s2000'], stock_in_q2['s3000'], stock_in_q2['s5000'],
            stock_in_q2['s10000'], stock_in_q2['s25000'], stock_in_q2['s50000']
        )
        _stock_out_model = ReportNonJudicial(
            "Stock Out", stock_out_q2['s100'], stock_out_q2['s150'], stock_out_q2['s200'], stock_out_q2['s250'],
            stock_out_q2['s300'], stock_out_q2['s400'], stock_out_q2['s500'], stock_out_q2['s750'],
            stock_out_q2['s1000'], stock_out_q2['s2000'], stock_out_q2['s3000'], stock_out_q2['s5000'],
            stock_out_q2['s10000'], stock_out_q2['s25000'], stock_out_q2['s50000']
        )

        _stock_required = (_stock_in_model + _stock_transfer_to_model) - (_stock_out_model + _stock_transfer_from_model)

        # TREASURIES DATA
        treasuries_data.append(
            ReportNonJudicial(
                treasury.name, _stock_required.s100, _stock_required.s150, _stock_required.s200, _stock_required.s250,
                _stock_required.s300, _stock_required.s400, _stock_required.s500, _stock_required.s750,
                _stock_required.s1000, _stock_required.s2000, _stock_required.s3000, _stock_required.s5000,
                _stock_required.s10000, _stock_required.s25000, _stock_required.s50000
            )
        )

        # # UPDATE ARRAY OF AMOUNTS AND QUANTITIES
        quantities_data.increase(
            _stock_required.s100, _stock_required.s150, _stock_required.s200, _stock_required.s250,
            _stock_required.s300, _stock_required.s400, _stock_required.s500, _stock_required.s750,
            _stock_required.s1000, _stock_required.s2000, _stock_required.s3000, _stock_required.s5000,
            _stock_required.s10000, _stock_required.s25000, _stock_required.s50000
        )
        amounts_data.increase(
            _stock_required.s100 * 100, _stock_required.s150 * 150, _stock_required.s200 * 200,
            _stock_required.s250 * 250, _stock_required.s300 * 300, _stock_required.s400 * 400,
            _stock_required.s500 * 500, _stock_required.s750 * 750, _stock_required.s1000 * 1000,
            _stock_required.s2000 * 2000, _stock_required.s3000 * 3000, _stock_required.s5000 * 5000,
            _stock_required.s10000 * 10000, _stock_required.s25000 * 25000, _stock_required.s50000 * 50000
        )

        # TOTAL AMOUNTS AND COUNTS
        if denomination == "high":
            total_amounts += (
                    (_stock_required.s2000 * 2000) + (_stock_required.s3000 * 3000) + (_stock_required.s5000 * 5000) +
                    (_stock_required.s10000 * 10000) + (_stock_required.s25000 * 25000) +
                    (_stock_required.s50000 * 50000)
            )
            total_counts += (
                    _stock_required.s2000 + _stock_required.s3000 + _stock_required.s5000 +
                    _stock_required.s10000 + _stock_required.s25000 + _stock_required.s50000
            )

        elif denomination == "low":
            total_amounts += (
                    (_stock_required.s100 * 100) + (_stock_required.s150 * 150) + (_stock_required.s200 * 200) +
                    (_stock_required.s250 * 250) + (_stock_required.s300 * 300) + (_stock_required.s400 * 400) +
                    (_stock_required.s500 * 500) + (_stock_required.s750 * 750) + (_stock_required.s1000 * 1000)
            )
            total_counts += (
                    _stock_required.s100 + _stock_required.s150 + _stock_required.s200 + _stock_required.s250 +
                    _stock_required.s300 + _stock_required.s400 + _stock_required.s500 + _stock_required.s750 +
                    _stock_required.s1000
            )

        else:
            total_amounts += (
                    (_stock_required.s100 * 100) + (_stock_required.s150 * 150) + (_stock_required.s200 * 200) +
                    (_stock_required.s250 * 250) + (_stock_required.s300 * 300) + (_stock_required.s400 * 400) +
                    (_stock_required.s500 * 500) + (_stock_required.s750 * 750) + (_stock_required.s1000 * 1000) +
                    (_stock_required.s2000 * 2000) + (_stock_required.s3000 * 3000) + (_stock_required.s5000 * 5000) +
                    (_stock_required.s10000 * 10000) + (_stock_required.s25000 * 25000) +
                    (_stock_required.s50000 * 50000)
            )
            total_counts += (
                    _stock_required.s100 + _stock_required.s150 + _stock_required.s200 + _stock_required.s250 +
                    _stock_required.s300 + _stock_required.s400 + _stock_required.s500 + _stock_required.s750 +
                    _stock_required.s1000 + _stock_required.s2000 + _stock_required.s3000 + _stock_required.s5000 +
                    _stock_required.s10000 + _stock_required.s25000 + _stock_required.s50000
            )

    return treasuries_data, quantities_data, amounts_data, total_amounts, total_counts


def get_complete_reports_for_judicial(date, treasury_name=None, denomination="full"):

    # TREASURY QUERY
    if treasury_name:
        treasuries = Treasury.objects.filter(name__icontains=treasury_name)
    else:
        treasuries = Treasury.objects.all()

    if date:
        naive_datetime = datetime.strptime(date, '%Y-%m-%dT%H:%M')
        timezone_aware_datetime = timezone.make_aware(naive_datetime, timezone.get_current_timezone())
        date = timezone_aware_datetime
    else:
        date = timezone.now()

    treasuries_data = []
    quantities_data = ReportJudicial(
        "Quantities", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    )
    amounts_data = ReportJudicial(
        "Amounts", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    )
    total_amounts = 0
    total_counts = 0

    for treasury in treasuries:
        stock_in_q1 = StockInJudicial.objects.filter(created_on__lte=date, source_treasury=treasury)
        stock_out_q1 = StockOutJudicial.objects.filter(created_on__lte=date, source_treasury=treasury)
        stock_transfer_from_q1 = TransferJudicial.objects.filter(created_on__lte=date, source_treasury=treasury,
                                                                status="complete")
        stock_transfer_to_q1 = TransferJudicial.objects.filter(created_on__lte=date, destination_treasury=treasury,
                                                              status="complete")

        if stock_transfer_to_q1.exists():
            stock_transfer_to_q2 = stock_transfer_to_q1.aggregate(
                j25=Sum('j25'), j30=Sum('j30'), j35=Sum('j35'), j50=Sum('j50'), j60=Sum('j60'), j75=Sum('j75'),
                j100=Sum('j100'), j125=Sum('j125'), j150=Sum('j150'), j200=Sum('j200'), j500=Sum('j500'),
                j1000=Sum('j1000'), j2000=Sum('j2000'), j3000=Sum('j3000'), j5000=Sum('j5000'), j10000=Sum('j10000'),
                j15000=Sum('j15000'),
            )
        else:
            stock_transfer_to_q2 = {
                'j25': 0, 'j30': 0, 'j35': 0, 'j50': 0, 'j60': 0, 'j75': 0, 'j100': 0, 'j125': 0, 'j150': 0,
                'j200': 0, 'j500': 0, 'j1000': 0, 'j2000': 0, 'j3000': 0, 'j5000': 0, 'j10000': 0, 'j15000': 0,
            }

        if stock_transfer_from_q1.exists():
            stock_transfer_from_q2 = stock_transfer_from_q1.aggregate(
                j25=Sum('j25'), j30=Sum('j30'), j35=Sum('j35'), j50=Sum('j50'), j60=Sum('j60'), j75=Sum('j75'),
                j100=Sum('j100'), j125=Sum('j125'), j150=Sum('j150'), j200=Sum('j200'), j500=Sum('j500'),
                j1000=Sum('j1000'), j2000=Sum('j2000'), j3000=Sum('j3000'), j5000=Sum('j5000'), j10000=Sum('j10000'),
                j15000=Sum('j15000'),
            )
        else:
            stock_transfer_from_q2 = {
                'j25': 0, 'j30': 0, 'j35': 0, 'j50': 0, 'j60': 0, 'j75': 0, 'j100': 0, 'j125': 0, 'j150': 0,
                'j200': 0, 'j500': 0, 'j1000': 0, 'j2000': 0, 'j3000': 0, 'j5000': 0, 'j10000': 0, 'j15000': 0,
            }

        if stock_in_q1.exists():
            stock_in_q2 = stock_in_q1.aggregate(
                j25=Sum('j25'), j30=Sum('j30'), j35=Sum('j35'), j50=Sum('j50'), j60=Sum('j60'), j75=Sum('j75'),
                j100=Sum('j100'), j125=Sum('j125'), j150=Sum('j150'), j200=Sum('j200'), j500=Sum('j500'),
                j1000=Sum('j1000'), j2000=Sum('j2000'), j3000=Sum('j3000'), j5000=Sum('j5000'), j10000=Sum('j10000'),
                j15000=Sum('j15000'),
            )
        else:
            stock_in_q2 = {
                'j25': 0, 'j30': 0, 'j35': 0, 'j50': 0, 'j60': 0, 'j75': 0, 'j100': 0, 'j125': 0, 'j150': 0,
                'j200': 0, 'j500': 0, 'j1000': 0, 'j2000': 0, 'j3000': 0, 'j5000': 0, 'j10000': 0, 'j15000': 0,
            }

        if stock_out_q1.exists():
            stock_out_q2 = stock_out_q1.aggregate(
                j25=Sum('j25'), j30=Sum('j30'), j35=Sum('j35'), j50=Sum('j50'), j60=Sum('j60'), j75=Sum('j75'),
                j100=Sum('j100'), j125=Sum('j125'), j150=Sum('j150'), j200=Sum('j200'), j500=Sum('j500'),
                j1000=Sum('j1000'), j2000=Sum('j2000'), j3000=Sum('j3000'), j5000=Sum('j5000'), j10000=Sum('j10000'),
                j15000=Sum('j15000'),
            )
        else:
            stock_out_q2 = {
                'j25': 0, 'j30': 0, 'j35': 0, 'j50': 0, 'j60': 0, 'j75': 0, 'j100': 0, 'j125': 0, 'j150': 0,
                'j200': 0, 'j500': 0, 'j1000': 0, 'j2000': 0, 'j3000': 0, 'j5000': 0, 'j10000': 0, 'j15000': 0,
            }

        _stock_transfer_to_model = ReportJudicial(
            "Stock Transfer To", stock_transfer_to_q2['j25'], stock_transfer_to_q2['j30'], stock_transfer_to_q2['j35'],
            stock_transfer_to_q2['j50'], stock_transfer_to_q2['j60'], stock_transfer_to_q2['j75'], stock_transfer_to_q2['j100'],
            stock_transfer_to_q2['j125'], stock_transfer_to_q2['j150'], stock_transfer_to_q2['j200'], stock_transfer_to_q2['j500'],
            stock_transfer_to_q2['j1000'], stock_transfer_to_q2['j2000'], stock_transfer_to_q2['j3000'], stock_transfer_to_q2['j5000'],
            stock_transfer_to_q2['j10000'], stock_transfer_to_q2['j15000'],
        )
        _stock_transfer_from_model = ReportJudicial(
            "Stock Transfer From", stock_transfer_from_q2['j25'], stock_transfer_from_q2['j30'], stock_transfer_from_q2['j35'],
            stock_transfer_from_q2['j50'], stock_transfer_from_q2['j60'], stock_transfer_from_q2['j75'], stock_transfer_from_q2['j100'],
            stock_transfer_from_q2['j125'], stock_transfer_from_q2['j150'], stock_transfer_from_q2['j200'], stock_transfer_from_q2['j500'],
            stock_transfer_from_q2['j1000'], stock_transfer_from_q2['j2000'], stock_transfer_from_q2['j3000'], stock_transfer_from_q2['j5000'],
            stock_transfer_from_q2['j10000'], stock_transfer_from_q2['j15000'],
        )
        _stock_in_model = ReportJudicial(
            "Stock In", stock_in_q2['j25'], stock_in_q2['j30'], stock_in_q2['j35'], stock_in_q2['j50'], stock_in_q2['j60'],
            stock_in_q2['j75'], stock_in_q2['j100'], stock_in_q2['j125'], stock_in_q2['j150'], stock_in_q2['j200'],
            stock_in_q2['j500'], stock_in_q2['j1000'], stock_in_q2['j2000'], stock_in_q2['j3000'], stock_in_q2['j5000'],
            stock_in_q2['j10000'], stock_in_q2['j15000'],
        )

        _stock_out_model = ReportJudicial(
            "Stock Out", stock_out_q2['j25'], stock_out_q2['j30'], stock_out_q2['j35'], stock_out_q2['j50'], stock_out_q2['j60'],
            stock_out_q2['j75'], stock_out_q2['j100'], stock_out_q2['j125'], stock_out_q2['j150'], stock_out_q2['j200'],
            stock_out_q2['j500'], stock_out_q2['j1000'], stock_out_q2['j2000'], stock_out_q2['j3000'], stock_out_q2['j5000'],
            stock_out_q2['j10000'], stock_out_q2['j15000'],
        )

        _stock_required = (_stock_in_model + _stock_transfer_to_model) - (_stock_out_model + _stock_transfer_from_model)

        # TREASURIES DATA
        treasuries_data.append(
            ReportJudicial(
                treasury.name, _stock_required.j25, _stock_required.j30, _stock_required.j35, _stock_required.j50,
                _stock_required.j60, _stock_required.j75, _stock_required.j100, _stock_required.j125, _stock_required.j150,
                _stock_required.j200, _stock_required.j500, _stock_required.j1000, _stock_required.j2000, _stock_required.j3000,
                _stock_required.j5000, _stock_required.j10000, _stock_required.j15000,
            )
        )

        # UPDATE ARRAY OF AMOUNTS AND QUANTITIES
        quantities_data.increase(
            _stock_required.j25, _stock_required.j30, _stock_required.j35, _stock_required.j50, _stock_required.j60,
            _stock_required.j75, _stock_required.j100, _stock_required.j125, _stock_required.j150, _stock_required.j200,
            _stock_required.j500, _stock_required.j1000, _stock_required.j2000, _stock_required.j3000, _stock_required.j5000,
            _stock_required.j10000, _stock_required.j15000,
        )

        amounts_data.increase(
            _stock_required.j25 * 25, _stock_required.j30 * 30, _stock_required.j35 * 35, _stock_required.j50 * 50,
            _stock_required.j60 * 60, _stock_required.j75 * 75, _stock_required.j100 * 100, _stock_required.j125 * 125,
            _stock_required.j150 * 150, _stock_required.j200 * 200, _stock_required.j500 * 500, _stock_required.j1000 * 1000,
            _stock_required.j2000 * 2000, _stock_required.j3000 * 3000, _stock_required.j5000 * 5000, _stock_required.j10000 * 10000,
            _stock_required.j15000 * 15000,
        )

        # TOTAL AMOUNTS AND COUNTS
        if denomination == "high":
            total_amounts += (
                (_stock_required.j2000 * 2000) + (_stock_required.j3000 * 3000) + (_stock_required.j5000 * 5000) +
                (_stock_required.j10000 * 10000) + (_stock_required.j15000 * 15000)
            )
            total_counts += (
                _stock_required.j2000 + _stock_required.j3000 + _stock_required.j5000 +
                _stock_required.j10000 + _stock_required.j15000
            )

        elif denomination == "low":
            total_amounts += (
                (_stock_required.j25 * 25) + (_stock_required.j30 * 30) + (_stock_required.j35 * 35) +
                (_stock_required.j50 * 50) + (_stock_required.j60 * 60) + (_stock_required.j75 * 75) +
                (_stock_required.j100 * 100) + (_stock_required.j125 * 125) + (_stock_required.j150 * 150) +
                (_stock_required.j200 * 200) + (_stock_required.j500 * 500) + (_stock_required.j1000 * 1000)
            )
            total_counts += (
                _stock_required.j25 + _stock_required.j30 + _stock_required.j35 +
                _stock_required.j50 + _stock_required.j60 + _stock_required.j75 +
                _stock_required.j100 + _stock_required.j125 + _stock_required.j150 +
                _stock_required.j200 + _stock_required.j500 + _stock_required.j1000
            )

        else:
            total_amounts += (
                (_stock_required.j25 * 25) + (_stock_required.j30 * 30) + (_stock_required.j35 * 35) +
                (_stock_required.j50 * 50) + (_stock_required.j60 * 60) + (_stock_required.j75 * 75) +
                (_stock_required.j100 * 100) + (_stock_required.j125 * 125) + (_stock_required.j150 * 150) +
                (_stock_required.j200 * 200) + (_stock_required.j500 * 500) + (_stock_required.j1000 * 1000) +
                (_stock_required.j2000 * 2000) + (_stock_required.j3000 * 3000) + (_stock_required.j5000 * 5000) +
                (_stock_required.j10000 * 10000) + (_stock_required.j15000 * 15000)
            )
            total_counts += (
                _stock_required.j25 + _stock_required.j30 + _stock_required.j35 +
                _stock_required.j50 + _stock_required.j60 + _stock_required.j75 +
                _stock_required.j100 + _stock_required.j125 + _stock_required.j150 +
                _stock_required.j200 + _stock_required.j500 + _stock_required.j1000 +
                _stock_required.j2000 + _stock_required.j3000 + _stock_required.j5000 +
                _stock_required.j10000 + _stock_required.j15000
            )

    return treasuries_data, quantities_data, amounts_data, total_amounts, total_counts


def get_consolidated_reports(date, treasury_name=None, denomination="full"):
    t_data, q_data, a_data, t_amounts, t_counts = get_complete_reports_for_non_judicial(
        date=date,
    )
    jt_data, jq_data, ja_data, jt_amounts, jt_counts = get_complete_reports_for_judicial(
        date=date,
    )

    # REPORT
    reports = []

    for i in range(len(t_data)):
        _report = ReportConsolidated(t_data[i].treasury, t_data[i], jt_data[i])
        reports.append(_report)

    return reports, (t_counts + jt_counts), (t_amounts + jt_amounts), q_data, ja_data

