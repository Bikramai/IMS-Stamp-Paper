from datetime import datetime

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import (
    TemplateView, ListView, DeleteView, DetailView, UpdateView, CreateView
)

from src.accounts.decorators import admin_decorators
from src.accounts.models import User, Treasury, City
from src.administration.admins.bll import (
    get_counts_list,
    get_monthly_counts,
    stockin_create_calculation,
    stockout_create_calculation,
    transfers_create_calculation, get_monthly_amounts, get_monthly_counts_treasury, get_monthly_amounts_treasury,
    treasury_denomination_count_and_amount, treasury_low_denomination_count_and_amount,
    treasury_high_denomination_count_and_amount, get_denomination_query, get_overall_stock_in_quantity_and_amount,
    get_overall_transfer_quantity_and_amount, get_overall_stock_out_quantity_and_amount,
    get_dict_total_of_each_column_for_all_treasuries, get_sum_and_amount_list_for_all_denominations,
    calculate_on_stock_out_removed, calculate_on_stock_in_removed, stockin_judicial_create_calculation,
    transfers_judicial_create_calculation, stockout_judicial_create_calculation,
    treasury_denomination_count_and_amount_judicial, treasury_low_denomination_count_and_amount_judicial,
    treasury_high_denomination_count_and_amount_judicial, get_dict_total_of_each_column_for_all_treasuries_judicial,
    get_sum_and_amount_list_for_all_denominations_judicial, get_denomination_query_judicial,
    calculate_on_stock_out_removed_judicial, calculate_on_stock_in_removed_judicial,
    get_overall_stock_in_quantity_and_amount_judicial, get_overall_stock_out_quantity_and_amount_judicial,
    get_overall_transfer_quantity_and_amount_judicial
)
from src.administration.admins.dll import ReportNonJudicial
from src.administration.admins.filters import UserFilter, TreasuryFilter, StockInFilter, StockOutFilter, TransferFilter, \
    StockInJudicialFilter, StockOutJudicialFilter, TransferJudicialFilter
from src.administration.admins.forms import UserForm, UserUpdateForm, TreasuryForm, StockInForm, StockOutForm, \
    TransferForm, RequestUpdateForm, StockInJudicialForm, StockOutJudicialForm, TransferJudicialForm, \
    RequestUpdateJudicialForm
from src.administration.admins.models import (StockIn, StockOut, Transfer, StockInJudicial, StockOutJudicial,
                                              TransferJudicial, Transaction)
from src.administration.admins.reports import get_complete_reports_for_non_judicial, get_complete_reports_for_judicial, \
    get_consolidated_reports
from src.administration.staff.views import staff_required

field_names = ['s100', 's150', 's200', 's250', 's300', 's400', 's500', 's1000', 's2000', 's3000', 's5000', 's10000',
               's25000', 's50000']


@method_decorator(admin_decorators, name='dispatch')
class DashboardView(TemplateView):
    """
    Registrations: Today, Month, Year (PAID/UNPAID)
    Subscriptions: Today, Month, Year (TYPES)
    Withdrawals  : Today, Month, Year (CALCULATE)
    """
    template_name = 'admins/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        current_year = datetime.now().year

        """ CORE STATS """
        sts_stock_in_quantity, sts_stock_in_amount = get_overall_stock_in_quantity_and_amount()
        sts_stock_out_quantity, sts_stock_out_amount = get_overall_stock_out_quantity_and_amount()
        sts_transfer_quantity, sts_transfer_amount = get_overall_transfer_quantity_and_amount()

        context['sts_stock_in_amount'] = sts_stock_in_amount
        context['sts_stock_out_amount'] = sts_stock_out_amount
        context['sts_transfer_amount'] = sts_transfer_amount

        """ GRAPHS STATS """
        transfer_counts = get_monthly_counts(Transfer, current_year)
        stock_in_counts = get_monthly_counts(StockIn, current_year)
        stock_out_counts = get_monthly_counts(StockOut, current_year)
        transfer_amounts = get_monthly_amounts(Transfer, current_year)
        stock_in_amounts = get_monthly_amounts(StockIn, current_year)
        stock_out_amounts = get_monthly_amounts(StockOut, current_year)

        context['transfer_count'] = get_counts_list(transfer_counts)
        context['stockin_count'] = get_counts_list(stock_in_counts)
        context['stockout_count'] = get_counts_list(stock_out_counts)
        context['transfer_amount'] = get_counts_list(transfer_amounts)
        context['stockin_amount'] = get_counts_list(stock_in_amounts)
        context['stockout_amount'] = get_counts_list(stock_out_amounts)

        context['total_treasury'] = Treasury.objects.count()
        context['total_staff'] = User.objects.exclude(is_superuser=True).count()
        context['treasuries'] = Treasury.objects.all()
        context['dashboard'] = "non-judicial"

        return context


class DashboardJudicialView(TemplateView):
    """
    Registrations: Today, Month, Year (PAID/UNPAID)
    Subscriptions: Today, Month, Year (TYPES)
    Withdrawals  : Today, Month, Year (CALCULATE)
    """
    template_name = 'admins/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardJudicialView, self).get_context_data(**kwargs)
        current_year = datetime.now().year

        """ CORE STATS """
        sts_stock_in_quantity, sts_stock_in_amount = get_overall_stock_in_quantity_and_amount_judicial()
        sts_stock_out_quantity, sts_stock_out_amount = get_overall_stock_out_quantity_and_amount_judicial()
        sts_transfer_quantity, sts_transfer_amount = get_overall_transfer_quantity_and_amount_judicial()

        context['sts_stock_in_amount'] = sts_stock_in_amount
        context['sts_stock_out_amount'] = sts_stock_out_amount
        context['sts_transfer_amount'] = sts_transfer_amount

        """ GRAPHS STATS """
        transfer_counts = get_monthly_counts(TransferJudicial, current_year)
        stock_in_counts = get_monthly_counts(StockInJudicial, current_year)
        stock_out_counts = get_monthly_counts(StockOutJudicial, current_year)
        transfer_amounts = get_monthly_amounts(TransferJudicial, current_year)
        stock_in_amounts = get_monthly_amounts(StockInJudicial, current_year)
        stock_out_amounts = get_monthly_amounts(StockOutJudicial, current_year)

        context['transfer_count'] = get_counts_list(transfer_counts)
        context['stockin_count'] = get_counts_list(stock_in_counts)
        context['stockout_count'] = get_counts_list(stock_out_counts)
        context['transfer_amount'] = get_counts_list(transfer_amounts)
        context['stockin_amount'] = get_counts_list(stock_in_amounts)
        context['stockout_amount'] = get_counts_list(stock_out_amounts)

        context['total_treasury'] = Treasury.objects.count()
        context['total_staff'] = User.objects.exclude(is_superuser=True).count()
        context['treasuries'] = Treasury.objects.all()
        context['dashboard'] = "judicial"

        return context


@method_decorator(admin_decorators, name='dispatch')
class PasswordChangeView(View):
    template_name = 'admins/change_password.html'

    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password updated successfully!')
            return redirect('admins:dashboard')
        return render(request, self.template_name, context={'form': form})


""" USERS """


@method_decorator(admin_decorators, name='dispatch')
class UserListView(ListView):
    model = User
    template_name = 'admins/user_list.html'

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        user_filter = UserFilter(self.request.GET, queryset=User.objects.filter())
        context['user_filter_form'] = user_filter.form

        paginator = Paginator(user_filter.qs, 50)
        page_number = self.request.GET.get('page')
        user_page_object = paginator.get_page(page_number)

        context['user_list'] = user_page_object
        return context


@method_decorator(admin_decorators, name='dispatch')
class UserDetailView(DetailView):
    model = User
    template_name = 'admins/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(admin_decorators, name='dispatch')
class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'admins/user_create.html'

    def get_success_url(self):
        return reverse('admins:user-list', )


@method_decorator(admin_decorators, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'admins/user_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().is_superuser:
            messages.warning(request, "You are not allowed access admin accounts")
            return redirect("admins:user-detail", self.get_object().pk)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('admins:user-detail', kwargs={'pk': self.object.pk})


@method_decorator(admin_decorators, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    template_name = 'admins/user_confirm_delete.html'
    success_url = reverse_lazy('admins:user-list')

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().is_superuser:
            messages.warning(request, "You are not allowed access admin accounts")
            return redirect("admins:user-detail", self.get_object().pk)
        return super().dispatch(request, *args, **kwargs)


@method_decorator(admin_decorators, name='dispatch')
class UserPasswordResetView(View):

    def dispatch(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        if user.is_superuser:
            messages.warning(request, "You are not allowed access admin accounts")
            return redirect("admins:user-detail", user.pk)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = AdminPasswordChangeForm(user=user)
        return render(request, 'admins/admin_password_reset.html', {'form': form, 'user': user})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = AdminPasswordChangeForm(data=request.POST, user=user)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, f"{user.get_full_name()} password changed successfully.")
            return redirect('admins:user-detail', pk=user.pk)
        return render(request, 'admins/admin_password_reset.html', {'form': form, 'user': user})


""" CITY """


@method_decorator(admin_decorators, name='dispatch')
class DistrictListView(ListView):
    model = City
    template_name = 'admins/district_list.html'
    context_object_name = 'cities'


@method_decorator(admin_decorators, name='dispatch')
class DistrictCreateView(CreateView):
    model = City
    template_name = 'admins/district_form.html'
    fields = ['name', 'state']
    success_url = reverse_lazy('admins:district-list')


@method_decorator(admin_decorators, name='dispatch')
class DistrictUpdateView(UpdateView):
    model = City
    template_name = 'admins/district_form.html'
    fields = ['name', 'state']
    success_url = reverse_lazy('admins:district-list')


@method_decorator(admin_decorators, name='dispatch')
class DistrictDeleteView(DeleteView):
    model = City
    template_name = 'admins/district_confirm_delete.html'
    success_url = reverse_lazy('admins:district-list')


""" TREASURY """


@method_decorator(admin_decorators, name='dispatch')
class TreasuryList(ListView):
    template_name = 'admins/treasury_list.html'
    queryset = Treasury.objects.all()

    def get_context_data(self, **kwargs):
        context = super(TreasuryList, self).get_context_data(**kwargs)
        object_filter = TreasuryFilter(self.request.GET, queryset=Treasury.objects.filter())

        object_list = object_filter.qs
        paginator = Paginator(object_list, 50)
        page_number = self.request.GET.get('page')
        page_object = paginator.get_page(page_number)

        context['filter_form'] = object_filter.form
        context['object_list'] = page_object
        return context


@method_decorator(staff_required, name='dispatch')
class TreasuryDetailView(DetailView):
    model = Treasury
    template_name = 'admins/treasury_detail.html'

    def get_object(self, queryset=None):
        obj = get_object_or_404(Treasury, pk=self.kwargs['pk'])

        if self.request.user.is_superuser:
            return obj

        if self.request.user.treasury == obj:
            return obj

        raise Http404

    def get_context_data(self, **kwargs):
        context = super(TreasuryDetailView, self).get_context_data(**kwargs)

        # GRAPHS
        current_year = datetime.now().year

        # GRAPHS STATS
        transfer_counts = get_monthly_counts_treasury(Transfer, current_year, self.object, True)
        stock_in_counts = get_monthly_counts_treasury(StockIn, current_year, self.object)
        stock_out_counts = get_monthly_counts_treasury(StockOut, current_year, self.object)

        transfer_amounts = get_monthly_amounts_treasury(Transfer, current_year, self.object, True)
        stock_in_amounts = get_monthly_amounts_treasury(StockIn, current_year, self.object)
        stock_out_amounts = get_monthly_amounts_treasury(StockOut, current_year, self.object)

        context['transfer_count'] = get_counts_list(transfer_counts)
        context['stockin_count'] = get_counts_list(stock_in_counts)
        context['stockout_count'] = get_counts_list(stock_out_counts)

        context['transfer_amount'] = get_counts_list(transfer_amounts)
        context['stockin_amount'] = get_counts_list(stock_in_amounts)
        context['stockout_amount'] = get_counts_list(stock_out_amounts)

        transfer_counts_judicial = get_monthly_counts_treasury(TransferJudicial, current_year, self.object, True)
        stock_in_counts_judicial = get_monthly_counts_treasury(StockInJudicial, current_year, self.object)
        stock_out_counts_judicial = get_monthly_counts_treasury(StockOutJudicial, current_year, self.object)

        transfer_amounts_judicial = get_monthly_amounts_treasury(TransferJudicial, current_year, self.object, True)
        stock_in_amounts_judicial = get_monthly_amounts_treasury(StockInJudicial, current_year, self.object)
        stock_out_amounts_judicial = get_monthly_amounts_treasury(StockOutJudicial, current_year, self.object)

        context['transfer_count_judicial'] = get_counts_list(transfer_counts_judicial)
        context['stockin_count_judicial'] = get_counts_list(stock_in_counts_judicial)
        context['stockout_count_judicial'] = get_counts_list(stock_out_counts_judicial)

        context['transfer_amount_judicial'] = get_counts_list(transfer_amounts_judicial)
        context['stockin_amount_judicial'] = get_counts_list(stock_in_amounts_judicial)
        context['stockout_amount_judicial'] = get_counts_list(stock_out_amounts_judicial)

        return context


@method_decorator(staff_required, name='dispatch')
class TreasuryReportView(DetailView):
    model = Treasury
    template_name = 'admins/treasury_reports.html'

    def get_context_data(self, **kwargs):
        context = super(TreasuryReportView, self).get_context_data(**kwargs)
        all_count, all_amount = treasury_denomination_count_and_amount(self.object)
        low_count, low_amount = treasury_low_denomination_count_and_amount(self.object)
        high_count, high_amount = treasury_high_denomination_count_and_amount(self.object)

        context['all_count'] = all_count
        context['all_amount'] = all_amount
        context['low_count'] = low_count
        context['low_amount'] = low_amount
        context['high_count'] = high_count
        context['high_amount'] = high_amount
        context['report_type'] = "Non Judicial"

        return context


@method_decorator(staff_required, name='dispatch')
class TreasuryReportJudicialView(DetailView):
    model = Treasury
    template_name = 'admins/treasury_reports_judicial.html'

    def get_context_data(self, **kwargs):
        context = super(TreasuryReportJudicialView, self).get_context_data(**kwargs)
        all_count, all_amount = treasury_denomination_count_and_amount_judicial(self.object)
        low_count, low_amount = treasury_low_denomination_count_and_amount_judicial(self.object)
        high_count, high_amount = treasury_high_denomination_count_and_amount_judicial(self.object)

        context['all_count'] = all_count
        context['all_amount'] = all_amount
        context['low_count'] = low_count
        context['low_amount'] = low_amount
        context['high_count'] = high_count
        context['high_amount'] = high_amount
        context['report_type'] = "Judicial"

        return context


@method_decorator(staff_required, name='dispatch')
class TreasuryInvoiceView(DetailView):
    model = Treasury
    template_name = 'admins/treasury_invoice.html'

    def get_context_data(self, **kwargs):
        context = super(TreasuryInvoiceView, self).get_context_data(**kwargs)
        report_type = self.request.GET.get('type') or None
        count, amount = treasury_denomination_count_and_amount(self.object)

        if report_type == 'low':
            count, amount = treasury_low_denomination_count_and_amount(self.object)
        elif report_type == 'high':
            count, amount = treasury_high_denomination_count_and_amount(self.object)

        context['count'] = count
        context['amount'] = amount
        context['type'] = report_type
        context['report_type'] = "Non Judicial"

        return context


@method_decorator(staff_required, name='dispatch')
class TreasuryInvoiceJudicialView(DetailView):
    model = Treasury
    template_name = 'admins/treasury_invoice_judicial.html'

    def get_context_data(self, **kwargs):
        context = super(TreasuryInvoiceJudicialView, self).get_context_data(**kwargs)
        report_type = self.request.GET.get('type') or None
        count, amount = treasury_denomination_count_and_amount_judicial(self.object)

        if report_type == 'low':
            count, amount = treasury_low_denomination_count_and_amount_judicial(self.object)
        elif report_type == 'high':
            count, amount = treasury_high_denomination_count_and_amount_judicial(self.object)

        context['count'] = count
        context['amount'] = amount
        context['type'] = report_type
        context['report_type'] = "Judicial"

        return context


@method_decorator(admin_decorators, name='dispatch')
class TreasuryCreateView(CreateView):
    model = Treasury
    form_class = TreasuryForm
    template_name = 'admins/treasury_form.html'
    success_url = reverse_lazy('admins:treasury-list')


@method_decorator(admin_decorators, name='dispatch')
class TreasuryUpdateView(UpdateView):
    model = Treasury
    form_class = TreasuryForm
    template_name = 'admins/treasury_update_form.html'
    success_url = reverse_lazy('admins:treasury-list')


@method_decorator(admin_decorators, name='dispatch')
class TreasuryDeleteView(DeleteView):
    model = Treasury
    template_name = 'admins/treasury_confirm_delete.html'
    success_url = reverse_lazy('admins:treasury-list')


""" STOCK IN """


@method_decorator(admin_decorators, name='dispatch')
class StockInListView(ListView):
    template_name = 'admins/stockin_list.html'
    paginate_by = 50

    def get_queryset(self):
        return StockIn.objects.filter()

    def get_context_data(self, **kwargs):
        context = super(StockInListView, self).get_context_data(**kwargs)
        object_filter = StockInFilter(self.request.GET, queryset=self.get_queryset())
        context['filter_form'] = object_filter.form
        object_list = object_filter.qs
        paginator = Paginator(object_list, 50)
        page_number = self.request.GET.get('page')
        page_object = paginator.get_page(page_number)
        context['object_list'] = page_object
        return context


@method_decorator(admin_decorators, name='dispatch')
class StockInCreateView(CreateView):
    model = StockIn
    form_class = StockInForm
    template_name = 'admins/stockin_form.html'
    success_url = reverse_lazy('admins:stock-in-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = "complete"
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        stockin_create_calculation(self.object)
        messages.success(self.request, "StockIn Record Successfully Added")
        return reverse("admins:stock-in-list")


@method_decorator(admin_decorators, name='dispatch')
class StockInDetailView(DetailView):
    model = StockIn
    template_name = 'admins/stockin_detail.html'


@method_decorator(admin_decorators, name='dispatch')
class StockInUpdateView(UpdateView):
    model = StockIn
    form_class = StockInForm
    template_name = 'admins/stockin_update_form.html'

    def get_success_url(self):
        messages.success(self.request, "StockIn Record Successfully Updated")
        return reverse("admins:stock-in-list")


@method_decorator(admin_decorators, name='dispatch')
class StockInDeleteView(DeleteView):
    model = StockIn
    template_name = 'admins/stockin_confirm_delete.html'
    success_url = reverse_lazy('admins:stock-in-list')

    def get_success_url(self):
        calculate_on_stock_in_removed(self.object)
        messages.success(self.request, "StockIn Record Successfully Deleted")
        return reverse("admins:stock-in-list")


""" STOCK OUT """


@method_decorator(admin_decorators, name='dispatch')
class StockOutListView(ListView):
    template_name = 'admins/stockout_list.html'
    paginate_by = 50

    def get_queryset(self):
        return StockOut.objects.filter()

    def get_context_data(self, **kwargs):
        context = super(StockOutListView, self).get_context_data(**kwargs)
        object_filter = StockOutFilter(self.request.GET, queryset=self.get_queryset())
        context['filter_form'] = object_filter.form
        object_list = object_filter.qs
        paginator = Paginator(object_list, 50)
        page_number = self.request.GET.get('page')
        page_object = paginator.get_page(page_number)
        context['object_list'] = page_object
        return context


@method_decorator(admin_decorators, name='dispatch')
class StockOutDetailView(DetailView):
    model = StockOut
    template_name = 'admins/stockout_detail.html'


@method_decorator(admin_decorators, name='dispatch')
class StockOutCreateView(CreateView):
    model = StockOut
    form_class = StockOutForm
    template_name = 'admins/stockout_form.html'
    success_url = reverse_lazy('admins:stock-out-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = "complete"
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        stockout_create_calculation(self.object)
        messages.success(self.request, "StockOut Record Successfully Created")
        return reverse("admins:stock-out-list")


@method_decorator(admin_decorators, name='dispatch')
class StockOutUpdateView(UpdateView):
    model = StockOut
    form_class = StockOutForm
    template_name = 'admins/stockout_update_form.html'

    def get_success_url(self):
        messages.success(self.request, "StockOut Record Successfully Updated")
        return reverse("admins:stock-out-list")


@method_decorator(admin_decorators, name='dispatch')
class StockOutDeleteView(DeleteView):
    model = StockOut
    template_name = 'admins/stockout_confirm_delete.html'

    def get_success_url(self):
        calculate_on_stock_out_removed(self.object)
        messages.success(self.request, "StockOut Record Successfully Deleted")
        return reverse("admins:stock-out-list")


""" TRANSFERS """


@method_decorator(admin_decorators, name='dispatch')
class TransferListView(ListView):
    template_name = 'admins/transfer_list.html'
    paginate_by = 50

    def get_queryset(self):
        return Transfer.objects.filter(status="complete")

    def get_context_data(self, **kwargs):
        context = super(TransferListView, self).get_context_data(**kwargs)
        object_filter = TransferFilter(self.request.GET, queryset=self.get_queryset())
        context['filter_form'] = object_filter.form
        object_list = object_filter.qs
        paginator = Paginator(object_list, 50)
        page_number = self.request.GET.get('page')
        page_object = paginator.get_page(page_number)
        context['object_list'] = page_object
        return context


@method_decorator(admin_decorators, name='dispatch')
class TransferCreateView(CreateView):
    model = Transfer
    form_class = TransferForm
    template_name = 'admins/transfer_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = "complete"
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        transfers_create_calculation(self.object)
        messages.success(self.request, "Transfer Record Successfully Added")
        return reverse("admins:transfer-list")


@method_decorator(admin_decorators, name='dispatch')
class TransferDetailView(DetailView):
    model = Transfer
    template_name = 'admins/transfer_detail.html'


@method_decorator(admin_decorators, name='dispatch')
class TransferUpdateView(UpdateView):
    model = Transfer
    form_class = TransferForm
    template_name = 'admins/transfer_update_form.html'

    def get_success_url(self):
        messages.success(self.request, "Transfer Record Successfully Updated")
        return reverse("admins:transfer-list")


@method_decorator(admin_decorators, name='dispatch')
class RequestListView(ListView):
    template_name = 'admins/request_list.html'
    paginate_by = 50

    def get_queryset(self):
        return Transfer.objects.exclude(status="complete")

    def get_context_data(self, **kwargs):
        context = super(RequestListView, self).get_context_data(**kwargs)
        object_filter = TransferFilter(self.request.GET, queryset=self.get_queryset())
        context['filter_form'] = object_filter.form
        object_list = object_filter.qs
        paginator = Paginator(object_list, 50)
        page_number = self.request.GET.get('page')
        page_object = paginator.get_page(page_number)
        context['object_list'] = page_object
        return context


@method_decorator(admin_decorators, name='dispatch')
class RequestDetailView(DetailView):
    model = Transfer
    template_name = 'admins/request_detail.html'


@method_decorator(admin_decorators, name='dispatch')
class RequestCreateView(DeleteView):
    model = Transfer
    template_name = 'admins/transfer_confirm_delete.html'


@method_decorator(admin_decorators, name='dispatch')
class RequestUpdateView(View):
    model = Transfer
    form_class = RequestUpdateForm
    template_name = 'admins/request_update_form.html'

    def get(self, request, pk, *args, **kwargs):
        transfer_request = get_object_or_404(Transfer.objects.exclude(status="completed"), pk=pk)
        context = {
            'form': self.form_class(instance=transfer_request),
            'pk': pk
        }
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):

        # INIT
        transfer_request = get_object_or_404(Transfer.objects.exclude(status="completed"), pk=pk)
        form = self.form_class(request.POST, instance=transfer_request)

        # VALIDATION`
        if form.is_valid():
            status = form.cleaned_data.get('status')

            if status == "complete":
                transfers_create_calculation(transfer_request)
                messages.success(request, "Transfer Request completed successfully")

                form.save()
                return redirect("admins:transfer-detail", pk)
            else:
                messages.success(request, "Transfer Request Successfully Updated")

                form.save()
                return redirect("admins:request-detail", pk)

        context = {'form': form, 'pk': pk}
        return render(request, self.template_name, context)


@method_decorator(admin_decorators, name='dispatch')
class RequestDeleteView(DeleteView):
    model = Transfer
    template_name = 'admins/transfer_confirm_delete.html'
    success_url = reverse_lazy('admins:request-list')

    def get_object(self, queryset=None):
        obj = get_object_or_404(Transfer.objects.filter(status='cancelled'), id=self.kwargs['pk'])
        return obj


""" STOCK IN (Judicial) """


@method_decorator(admin_decorators, name='dispatch')
class StockInJudicialListView(ListView):
    template_name = 'admins/stockinjudicial_list.html'
    paginate_by = 50

    def get_queryset(self):
        return StockInJudicial.objects.filter()

    def get_context_data(self, **kwargs):
        context = super(StockInJudicialListView, self).get_context_data(**kwargs)
        object_filter = StockInJudicialFilter(self.request.GET, queryset=self.get_queryset())
        context['filter_form'] = object_filter.form
        object_list = object_filter.qs
        paginator = Paginator(object_list, 50)
        page_number = self.request.GET.get('page')
        page_object = paginator.get_page(page_number)
        context['object_list'] = page_object
        return context


@method_decorator(admin_decorators, name='dispatch')
class StockInJudicialCreateView(CreateView):
    model = StockInJudicial
    form_class = StockInJudicialForm
    template_name = 'admins/stockinjudicial_form.html'
    success_url = reverse_lazy('admins:stock-in-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = "complete"
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        stockin_judicial_create_calculation(self.object)
        messages.success(self.request, "StockIn Record Successfully Added")
        return reverse("admins:stock-in-judicial-list")


@method_decorator(admin_decorators, name='dispatch')
class StockInJudicialDetailView(DetailView):
    model = StockInJudicial
    template_name = 'admins/stockinjudicial_detail.html'


@method_decorator(admin_decorators, name='dispatch')
class StockInJudicialUpdateView(UpdateView):
    model = StockInJudicial
    form_class = StockInJudicialForm
    template_name = 'admins/stockinjudicial_update_form.html'

    def get_success_url(self):
        messages.success(self.request, "StockIn Record Successfully Updated")
        return reverse("admins:stock-in-judicial-list")


@method_decorator(admin_decorators, name='dispatch')
class StockInJudicialDeleteView(DeleteView):
    model = StockInJudicial
    template_name = 'admins/stockinjudicial_confirm_delete.html'
    success_url = reverse_lazy('admins:stock-in-list')

    def get_success_url(self):
        calculate_on_stock_in_removed_judicial(self.object)
        messages.success(self.request, "StockIn Record Successfully Deleted")
        return reverse("admins:stock-in-judicial-list")


""" STOCK OUT (Judicial)  """


@method_decorator(admin_decorators, name='dispatch')
class StockOutJudicialListView(ListView):
    template_name = 'admins/stockoutjudicial_list.html'
    paginate_by = 50

    def get_queryset(self):
        return StockOutJudicial.objects.filter()

    def get_context_data(self, **kwargs):
        context = super(StockOutJudicialListView, self).get_context_data(**kwargs)
        object_filter = StockOutJudicialFilter(self.request.GET, queryset=self.get_queryset())
        context['filter_form'] = object_filter.form
        object_list = object_filter.qs
        paginator = Paginator(object_list, 50)
        page_number = self.request.GET.get('page')
        page_object = paginator.get_page(page_number)
        context['object_list'] = page_object
        return context


@method_decorator(admin_decorators, name='dispatch')
class StockOutJudicialDetailView(DetailView):
    model = StockOutJudicial
    template_name = 'admins/stockoutjudicial_detail.html'


@method_decorator(admin_decorators, name='dispatch')
class StockOutJudicialCreateView(CreateView):
    model = StockOutJudicial
    form_class = StockOutJudicialForm
    template_name = 'admins/stockoutjudicial_form.html'
    success_url = reverse_lazy('admins:stock-out-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = "complete"
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        stockout_judicial_create_calculation(self.object)
        messages.success(self.request, "StockOut Record Successfully Created")
        return reverse("admins:stock-out-judicial-list")


@method_decorator(admin_decorators, name='dispatch')
class StockOutJudicialUpdateView(UpdateView):
    model = StockOutJudicial
    form_class = StockOutJudicialForm
    template_name = 'admins/stockoutjudicial_update_form.html'

    def get_success_url(self):
        messages.success(self.request, "StockOut Record Successfully Updated")
        return reverse("admins:stock-out-judicial-list")


@method_decorator(admin_decorators, name='dispatch')
class StockOutJudicialDeleteView(DeleteView):
    model = StockOutJudicial
    template_name = 'admins/stockoutjudicial_confirm_delete.html'

    def get_success_url(self):
        calculate_on_stock_out_removed_judicial(self.object)
        messages.success(self.request, "StockOut Record Successfully Deleted")
        return reverse("admins:stock-out-judicial-list")


""" TRANSFERS (Judicial) """


@method_decorator(admin_decorators, name='dispatch')
class TransferJudicialListView(ListView):
    template_name = 'admins/transferjudicial_list.html'
    paginate_by = 50

    def get_queryset(self):
        return TransferJudicial.objects.filter(status="complete")

    def get_context_data(self, **kwargs):
        context = super(TransferJudicialListView, self).get_context_data(**kwargs)
        object_filter = TransferJudicialFilter(self.request.GET, queryset=self.get_queryset())
        context['filter_form'] = object_filter.form
        object_list = object_filter.qs
        paginator = Paginator(object_list, 50)
        page_number = self.request.GET.get('page')
        page_object = paginator.get_page(page_number)
        context['object_list'] = page_object
        return context


@method_decorator(admin_decorators, name='dispatch')
class TransferJudicialCreateView(CreateView):
    model = TransferJudicial
    form_class = TransferJudicialForm
    template_name = 'admins/transferjudicial_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = "complete"
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        transfers_judicial_create_calculation(self.object)
        messages.success(self.request, "Transfer Record Successfully Added")
        return reverse("admins:transfer-judicial-list")


@method_decorator(admin_decorators, name='dispatch')
class TransferJudicialDetailView(DetailView):
    model = TransferJudicial
    template_name = 'admins/transferjudicial_detail.html'


@method_decorator(admin_decorators, name='dispatch')
class TransferJudicialUpdateView(UpdateView):
    model = TransferJudicial
    form_class = TransferJudicialForm
    template_name = 'admins/transfer_update_form.html'

    def get_success_url(self):
        messages.success(self.request, "Transfer Record Successfully Updated")
        return reverse("admins:transfer-judicial-list")


@method_decorator(admin_decorators, name='dispatch')
class RequestJudicialListView(ListView):
    template_name = 'admins/requestjudicial_list.html'
    paginate_by = 50

    def get_queryset(self):
        return TransferJudicial.objects.exclude(status="complete")

    def get_context_data(self, **kwargs):
        context = super(RequestJudicialListView, self).get_context_data(**kwargs)
        object_filter = TransferJudicialFilter(self.request.GET, queryset=self.get_queryset())
        context['filter_form'] = object_filter.form
        object_list = object_filter.qs
        paginator = Paginator(object_list, 50)
        page_number = self.request.GET.get('page')
        page_object = paginator.get_page(page_number)
        context['object_list'] = page_object
        return context


@method_decorator(admin_decorators, name='dispatch')
class RequestJudicialDetailView(DetailView):
    model = TransferJudicial
    template_name = 'admins/requestjudicial_detail.html'


@method_decorator(admin_decorators, name='dispatch')
class RequestJudicialDeleteView(DeleteView):
    model = TransferJudicial
    template_name = 'admins/transferjudicial_confirm_delete.html'
    success_url = reverse_lazy('admins:request_judicial-list')

    def get_object(self, queryset=None):
        obj = get_object_or_404(TransferJudicial.objects.filter(status='cancelled'), id=self.kwargs['pk'])
        return obj


@method_decorator(admin_decorators, name='dispatch')
class RequestJudicialUpdateView(View):
    model = TransferJudicial
    form_class = RequestUpdateJudicialForm
    template_name = 'admins/requestjudicial_update_form.html'

    def get(self, request, pk, *args, **kwargs):
        transfer_request = get_object_or_404(TransferJudicial.objects.exclude(status="completed"), pk=pk)
        context = {
            'form': self.form_class(instance=transfer_request),
            'pk': pk
        }
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):

        # INIT
        transfer_request = get_object_or_404(TransferJudicial.objects.exclude(status="completed"), pk=pk)
        form = self.form_class(request.POST, instance=transfer_request)

        # VALIDATION`
        if form.is_valid():
            status = form.cleaned_data.get('status')

            if status == "complete":
                transfers_judicial_create_calculation(transfer_request)
                messages.success(request, "Transfer Request completed successfully")

                form.save()
                return redirect("admins:transfer_judicial-detail", pk)
            else:
                messages.success(request, "Transfer Request Successfully Updated")

                form.save()
                return redirect("admins:request_judicial-detail", pk)

        context = {'form': form, 'pk': pk}
        return render(request, self.template_name, context)


""" REPORTING (Judicial) """


@method_decorator(admin_decorators, name='dispatch')
class ReportDenomination(ListView):
    queryset = Treasury.objects.all()
    template_name = 'admins/report_denomination_list.html'

    def get_context_data(self, **kwargs):
        context = super(ReportDenomination, self).get_context_data(**kwargs)
        query = self.request.GET.get('type') or None
        treasury = self.request.GET.get('treasury') or None
        date = self.request.GET.get('date') or None

        # count, amount = get_denomination_query(query)
        # totals = get_dict_total_of_each_column_for_all_treasuries()
        # sums, amounts = get_sum_and_amount_list_for_all_denominations()

        t_data, q_data, a_data, t_amounts, t_counts = get_complete_reports_for_non_judicial(
            date=date, denomination=query, treasury_name=treasury
        )

        context['count'] = t_counts
        context['amount'] = t_amounts
        context['query'] = query
        context['object_list'] = t_data
        context['sums'] = q_data
        context['amounts'] = a_data

        return context


@method_decorator(admin_decorators, name='dispatch')
class ReportJudicialDenomination(ListView):
    queryset = Treasury.objects.all()
    template_name = 'admins/report_denomination_list_judicial.html'

    def get_context_data(self, **kwargs):
        context = super(ReportJudicialDenomination, self).get_context_data(**kwargs)
        query = self.request.GET.get('type') or None
        treasury = self.request.GET.get('treasury') or None
        date = self.request.GET.get('date') or None

        # count, amount = get_denomination_query_judicial(query)
        # totals = get_dict_total_of_each_column_for_all_treasuries_judicial()
        # sums, amounts = get_sum_and_amount_list_for_all_denominations_judicial()

        t_data, q_data, a_data, t_amounts, t_counts = get_complete_reports_for_judicial(
            date=date, denomination=query, treasury_name=treasury
        )

        context['count'] = t_counts
        context['amount'] = t_amounts
        context['query'] = query
        context['object_list'] = t_data
        context['sums'] = q_data
        context['amounts'] = a_data

        return context


@method_decorator(admin_decorators, name='dispatch')
class ReportConsolidatedView(TemplateView):
    template_name = 'admins/report_consolidated.html'

    def get_context_data(self, **kwargs):
        context = super(ReportConsolidatedView, self).get_context_data(**kwargs)
        date = self.request.GET.get('date') or None
        # 2024-05-02T17:52 this is data format convert to 2024-05-02 for date format
        reports, counts, amounts, nj_qty_list, j_qty_list = get_consolidated_reports(date=date)

        context['object_list'] = reports
        context['date'] = date.split("T")[0] if date else None
        context['njq'] = nj_qty_list
        context['jq'] = j_qty_list
        context['m_cost'] = 27.423

        return context
