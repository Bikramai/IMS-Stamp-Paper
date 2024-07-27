from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def member_required_decorator(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/accounts/login/'):
    '''
    Decorator for views that checks that the logged-in user is a student,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.treasury,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def staff_required_decorator(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/accounts/login/'):
    '''
    Decorator for views that checks that the logged-in user is a student,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def admin_decorators(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/accounts/login/'):
    '''
    Decorator for views that checks that the logged-in user is a student,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_staff and u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
