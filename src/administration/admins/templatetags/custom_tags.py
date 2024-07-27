from django import template

from src.administration.admins.models import StockIn, Transfer, StockOut
from src.administration.admins.bll import get_specific_value

register = template.Library()


@register.simple_tag
def relative_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url


@register.simple_tag()
def multiply(qty, price, *args, **kwargs):
    from django.contrib.humanize.templatetags.humanize import intcomma
    result = qty * price
    formatted_result = '{:.1f}'.format(result)  # Format result to two decimal places
    return intcomma(formatted_result)


@register.filter
def check_null(value):
    if value:
        return value
    return "-"


@register.filter
def calculate_specific_value(value):
    """ DECIMAL VALUE MUST NOT REACH BEYOND 2 NUMBERS AFTER DECIMAL POINT
    """
    return "{:.1f}".format(value * get_specific_value())


@register.filter
def get_fields_startswith(obj, prefix):
    return {k: v for k, v in obj.__dict__.items() if k.startswith(prefix)}


@register.filter
def transaction_type(transaction):
    if isinstance(transaction, StockIn):
        return "StockIn"
    elif isinstance(transaction, StockOut):
        return "StockOut"
    elif isinstance(transaction, Transfer):
        return "Transfer"
    else:
        return "Unknown"


@register.filter(name='cool_num', is_safe=False)
def cool_number(value, num_decimals=2):
    """
    Django template filter to convert regular numbers to a
    cool format (ie: 2K, 434.4K, 33M, 1.2B, 5.7T...)
    :param value: number
    :param num_decimals: Number of decimal digits
    """

    int_value = int(value)
    formatted_number = '{{:.{}f}}'.format(num_decimals)
    if int_value < 1000:
        return str(int_value)
    elif int_value < 1000000:
        return formatted_number.format(int_value/1000.0).rstrip('0').rstrip('.') + 'K'
    elif int_value < 1000000000:
        return formatted_number.format(int_value/1000000.0).rstrip('0').rstrip('.') + 'M'
    elif int_value < 1000000000000:
        return formatted_number.format(int_value/1000000000.0).rstrip('0').rstrip('.') + 'B'
    else:
        return formatted_number.format(int_value/1000000000000.0).rstrip('0').rstrip('.') + 'T'
