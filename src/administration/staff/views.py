from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.core.paginator import Paginator
from django.db.models import Sum, F, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView
)

from src.accounts.decorators import staff_required_decorator, member_required_decorator
from src.accounts.models import User, Treasury
from src.administration.admins.bll import (
    stockin_create_calculation, stockout_create_calculation, transfers_create_calculation,
    treasury_denomination_count_and_amount, treasury_low_denomination_count_and_amount,
    treasury_high_denomination_count_and_amount, stockin_judicial_create_calculation,
    stockout_judicial_create_calculation
)
from .filters import StockInFilter, StockOutFilter, TransferFilter, StockInJudicialFilter, StockOutJudicialFilter, \
    TransferJudicialFilter
from .forms import StockInForm, StockOutForm, TransferForm, StockInJudicialForm, StockOutJudicialForm, \
    TransferJudicialForm
from src.administration.admins.models import StockIn, StockOut, Transfer, StockInJudicial, StockOutJudicial, \
    TransferJudicial

member_required = member_required_decorator()
staff_required = staff_required_decorator()


@method_decorator(member_required, name='dispatch')
class DashboardView(TemplateView):
    """
    Registrations: Today, Month, Year (PAID/UNPAID)
    Subscriptions: Today, Month, Year (TYPES)
    Withdrawals  : Today, Month, Year (CALCULATE)
    """
    template_name = 'staff/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        return context


@method_decorator(member_required, name='dispatch')
class PasswordChangeView(View):
    template_name = 'staff/change_password.html'

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


@method_decorator(member_required, name='dispatch')
class UserDetailView(DetailView):
    model = User
    template_name = 'staff/user_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(User.objects.filter(treasury=self.request.user.treasury), id=self.kwargs['pk'])


@method_decorator(member_required, name='dispatch')
class UserListView(ListView):
    model = User
    template_name = 'staff/user_list.html'

    def get_queryset(self):
        return User.objects.filter(treasury=self.request.user.treasury)


""" TRANSACTIONS """


@method_decorator(member_required, name='dispatch')
class StockInListView(ListView):
    template_name = 'staff/stock_in_list.html'
    paginate_by = 50

    def get_queryset(self):
        return StockIn.objects.filter(source_treasury=self.request.user.treasury)

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


@method_decorator(member_required, name='dispatch')
class StockInCreateView(CreateView):
    model = StockIn
    form_class = StockInForm
    template_name = 'staff/stockin_form.html'
    success_url = reverse_lazy('staff:stock-in-list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(
                request, f"Be careful {request.user.get_name_or_username()} - you do not have permission "
                         f"to access this feature. Your actions are being monitored, and violations of "
                         f"security protocols will result in severe consequences."
            )
            return redirect('staff:stock-in-list')
        return super(StockInCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.source_treasury = self.request.user.treasury
        form.instance.status = "complete"
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        stockin_create_calculation(self.object)
        messages.success(self.request, "StockIn Record Successfully Added")
        return reverse("staff:stock-in-list")


@method_decorator(member_required, name='dispatch')
class StockInDetailView(DetailView):
    model = StockIn
    template_name = 'staff/stockin_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(StockIn, id=self.kwargs['pk'], source_treasury=self.request.user.treasury)


@method_decorator(member_required, name='dispatch')
class StockOutListView(ListView):
    template_name = 'staff/stock_out_list.html'
    paginate_by = 50

    def get_queryset(self):
        return StockOut.objects.filter(source_treasury=self.request.user.treasury)

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


@method_decorator(member_required, name='dispatch')
class StockOutCreateView(CreateView):
    model = StockOut
    form_class = StockOutForm
    template_name = 'staff/stockout_form.html'
    success_url = reverse_lazy('staff:stock-out-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.source_treasury = self.request.user.treasury
        form.instance.status = "complete"
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        stockout_create_calculation(self.object)
        messages.success(self.request, "StockOut Record Successfully Created")
        return reverse("staff:stock-out-list")


@method_decorator(member_required, name='dispatch')
class StockOutDetailView(DetailView):
    model = StockOut
    template_name = 'staff/stockout_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(StockOut, id=self.kwargs['pk'], source_treasury=self.request.user.treasury)


@method_decorator(member_required, name='dispatch')
class TransferListView(ListView):
    template_name = 'staff/transfer_list.html'
    paginate_by = 50

    def get_queryset(self):
        return Transfer.objects.filter(destination_treasury=self.request.user.treasury)

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


@method_decorator(member_required, name='dispatch')
class TransferCreateView(CreateView):
    model = Transfer
    form_class = TransferForm
    template_name = 'staff/transfer_form.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(
                request, f"Be careful {request.user.get_name_or_username()} - you do not have permission "
                         f"to access this feature. Your actions are being monitored, and violations of "
                         f"security protocols will result in severe consequences."
            )
            return redirect('staff:transfer-list')
        return super(TransferCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.destination_treasury = self.request.user.treasury
        form.instance.status = "pending"
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "Transfer Record Successfully Added")
        return reverse("staff:transfer-list")


@method_decorator(member_required, name='dispatch')
class TransferDetailView(DetailView):
    model = Transfer
    template_name = 'staff/transfer_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Transfer, id=self.kwargs['pk'], destination_treasury=self.request.user.treasury)


"""Judicial"""


@method_decorator(member_required, name='dispatch')
class StockInJudicialListView(ListView):
    template_name = 'staff/stockinjudicial_list.html'
    paginate_by = 50

    def get_queryset(self):
        return StockInJudicial.objects.filter(source_treasury=self.request.user.treasury)

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


@method_decorator(member_required, name='dispatch')
class StockInJudicialCreateView(CreateView):
    model = StockInJudicial
    form_class = StockInJudicialForm
    template_name = 'staff/stockinjudicial_form.html'
    success_url = reverse_lazy('staff:stock-in-judicial-list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(
                request, f"Be careful {request.user.get_name_or_username()} - you do not have permission "
                         f"to access this feature. Your actions are being monitored, and violations of "
                         f"security protocols will result in severe consequences."
            )
            return redirect('staff:stock-in-judicial-list')
        return super(StockInJudicialCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.source_treasury = self.request.user.treasury
        form.instance.status = "complete"
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        stockin_judicial_create_calculation(self.object)
        messages.success(self.request, "StockIn Record Successfully Added")
        return reverse("staff:stock-in-judicial-list")


@method_decorator(member_required, name='dispatch')
class StockInJudicialDetailView(DetailView):
    model = StockInJudicial
    template_name = 'staff/stockinjudicial_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(StockInJudicial, id=self.kwargs['pk'], source_treasury=self.request.user.treasury)


@method_decorator(member_required, name='dispatch')
class StockOutJudicialListView(ListView):
    template_name = 'staff/stockoutjudicial_list.html'
    paginate_by = 50

    def get_queryset(self):
        return StockOutJudicial.objects.filter(source_treasury=self.request.user.treasury)

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


@method_decorator(member_required, name='dispatch')
class StockOutJudicialCreateView(CreateView):
    model = StockOutJudicial
    form_class = StockOutJudicialForm
    template_name = 'staff/stockoutjudicial_form.html'
    success_url = reverse_lazy('staff:stock-out-judicial-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.source_treasury = self.request.user.treasury
        form.instance.status = "complete"
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        stockout_judicial_create_calculation(self.object)
        messages.success(self.request, "StockOut Record Successfully Created")
        return reverse("staff:stock-out-judicial-list")


@method_decorator(member_required, name='dispatch')
class StockOutJudicialDetailView(DetailView):
    model = StockOutJudicial
    template_name = 'staff/stockoutjudicial_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(StockOut, id=self.kwargs['pk'], source_treasury=self.request.user.treasury)


@method_decorator(member_required, name='dispatch')
class TransferJudicialListView(ListView):
    template_name = 'staff/transferjudicial_list.html'
    paginate_by = 50

    def get_queryset(self):
        return TransferJudicial.objects.filter(destination_treasury=self.request.user.treasury)

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


@method_decorator(member_required, name='dispatch')
class TransferJudicialCreateView(CreateView):
    model = TransferJudicial
    form_class = TransferJudicialForm
    template_name = 'staff/transferjudicial_form.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(
                request, f"Be careful {request.user.get_name_or_username()} - you do not have permission "
                         f"to access this feature. Your actions are being monitored, and violations of "
                         f"security protocols will result in severe consequences."
            )
            return redirect('staff:transfer-judicial-list')
        return super(TransferJudicialCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.destination_treasury = self.request.user.treasury
        form.instance.status = "pending"
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "Transfer Record Successfully Added")
        return reverse("staff:transfer-judicial-list")


@method_decorator(member_required, name='dispatch')
class TransferJudicialDetailView(DetailView):
    model = TransferJudicial
    template_name = 'staff/transferjudicial_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(TransferJudicial, id=self.kwargs['pk'],
                                 destination_treasury=self.request.user.treasury)
