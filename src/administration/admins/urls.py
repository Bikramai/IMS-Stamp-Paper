from django.urls import path

from .views import (
    DashboardView,
    StockInDetailView,
    StockOutDetailView,
    TransferDetailView,
    UserListView, UserDetailView,
    UserUpdateView, UserPasswordResetView, UserCreateView, TreasuryList, TreasuryCreateView, TreasuryUpdateView,
    TreasuryDeleteView, StockInListView, StockInCreateView, StockInUpdateView, StockInDeleteView,
    StockOutListView, StockOutCreateView, StockOutUpdateView, StockOutDeleteView, TransferListView, TransferCreateView,
    TreasuryDetailView, UserDeleteView, RequestListView, RequestDetailView,
    RequestUpdateView, PasswordChangeView, TreasuryReportView, TreasuryInvoiceView, ReportDenomination,
    DistrictListView, DistrictCreateView, DistrictUpdateView, DistrictDeleteView,
    StockInJudicialListView, StockInJudicialCreateView, StockInJudicialDetailView, StockInJudicialUpdateView,
    StockInJudicialDeleteView, StockOutJudicialListView, StockOutJudicialCreateView, StockOutJudicialDetailView,
    StockOutJudicialUpdateView,
    StockOutJudicialDeleteView, TransferJudicialListView, TransferJudicialDetailView,
    RequestJudicialListView, RequestJudicialDetailView, RequestJudicialUpdateView,
    TreasuryReportJudicialView, TreasuryInvoiceJudicialView, ReportJudicialDenomination, RequestDeleteView,
    RequestJudicialDeleteView, DashboardJudicialView,
    ReportConsolidatedView
)

app_name = 'admins'
urlpatterns = [

    path('', DashboardView.as_view(), name='dashboard'),
    path('judicial/', DashboardJudicialView.as_view(), name='dashboard-judicial'),
    path('password/change/', PasswordChangeView.as_view(), name='password-change'),

    path('users/', UserListView.as_view(), name='user-list'),
    path('user/add/', UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/change/', UserUpdateView.as_view(), name='user-update'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('users/<int:pk>/detail/', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:pk>/password/reset/', UserPasswordResetView.as_view(), name='user-password-reset-view'),
]

urlpatterns += [

    path('treasury/', TreasuryList.as_view(), name='treasury-list'),
    path('treasury/add/', TreasuryCreateView.as_view(), name='treasury-create'),
    path('treasury/<int:pk>/', TreasuryDetailView.as_view(), name='treasury-detail'),
    path('treasury/<int:pk>/reports/', TreasuryReportView.as_view(), name='treasury-report'),
    path('treasury/<int:pk>/judicial/reports/', TreasuryReportJudicialView.as_view(), name='treasury-report-judicial'),
    path('treasury/<int:pk>/invoice/', TreasuryInvoiceView.as_view(), name='treasury-invoice'),
    path('treasury/<int:pk>/judicial/invoice/', TreasuryInvoiceJudicialView.as_view(),
         name='treasury-invoice-judicial'),
    path('treasury/<int:pk>/change/', TreasuryUpdateView.as_view(), name='treasury-update'),
    # path('treasury/<int:pk>/delete/', TreasuryDeleteView.as_view(), name='treasury-delete'),

]

urlpatterns += [
    path('district/', DistrictListView.as_view(), name='district-list'),
    path('district/create/', DistrictCreateView.as_view(), name='district-create'),
    path('district/<int:pk>/update/', DistrictUpdateView.as_view(), name='district-update'),
    path('district/<int:pk>/delete/', DistrictDeleteView.as_view(), name='district-delete'),
]

urlpatterns += [

    path('non-judicial/stockin/', StockInListView.as_view(), name='stock-in-list'),
    path('non-judicial/stockin/<int:pk>/detail/', StockInDetailView.as_view(), name='stock_in-detail'),
    path('non-judicial/stockin/add/', StockInCreateView.as_view(), name='stock_in-create'),
    path('non-judicial/stockin/<int:pk>/change/', StockInUpdateView.as_view(), name='stock_in-update'),
    path('non-judicial/stockin/<int:pk>/delete/', StockInDeleteView.as_view(), name='stock_in-delete'),

]

urlpatterns += [

    path('non-judicial/stockout/', StockOutListView.as_view(), name='stock-out-list'),
    path('non-judicial/stockout/add/', StockOutCreateView.as_view(), name='stock_out-create'),
    path('non-judicial/stockout/<int:pk>/detail/', StockOutDetailView.as_view(), name='stock_out-detail'),
    path('non-judicial/stockout/<int:pk>/change/', StockOutUpdateView.as_view(), name='stock_out-update'),
    path('non-judicial/stockout/<int:pk>/delete/', StockOutDeleteView.as_view(), name='stock_out-delete'),

]

urlpatterns += [

    path('non-judicial/transfer/', TransferListView.as_view(), name='transfer-list'),
    # path('non-judicial/transfer/add/', TransferCreateView.as_view(), name='transfer-create'),
    path('non-judicial/transfer/<int:pk>/detail/', TransferDetailView.as_view(), name='transfer-detail'),
    # path('non-judicial/transfer/<int:pk>/change/', TransferUpdateView.as_view(), name='transfer-update'),

]

urlpatterns += [

    path('non-judicial/request/', RequestListView.as_view(), name='request-list'),
    path('non-judicial/request/<int:pk>/detail/', RequestDetailView.as_view(), name='request-detail'),
    path('non-judicial/request/<int:pk>/change/', RequestUpdateView.as_view(), name='request-update'),
    path('non-judicial/request/<int:pk>/delete/', RequestDeleteView.as_view(), name='request-delete'),
]

urlpatterns += [

    path('judicial/stockin/', StockInJudicialListView.as_view(), name='stock-in-judicial-list'),
    path('judicial/stockin/<int:pk>/detail/', StockInJudicialDetailView.as_view(), name='stock_in_judicial-detail'),
    path('judicial/stockin/add/', StockInJudicialCreateView.as_view(), name='stock_in_judicial-create'),
    path('judicial/stockin/<int:pk>/change/', StockInJudicialUpdateView.as_view(), name='stock_in_judicial-update'),
    path('judicial/stockin/<int:pk>/delete/', StockInJudicialDeleteView.as_view(), name='stock_in_judicial-delete'),

]

urlpatterns += [

    path('judicial/stockout/', StockOutJudicialListView.as_view(), name='stock-out-judicial-list'),
    path('judicial/stockout/add/', StockOutJudicialCreateView.as_view(), name='stock_out_judicial-create'),
    path('judicial/stockout/<int:pk>/detail/', StockOutJudicialDetailView.as_view(), name='stock_out_judicial-detail'),
    path('judicial/stockout/<int:pk>/change/', StockOutJudicialUpdateView.as_view(), name='stock_out_judicial-update'),
    path('judicial/stockout/<int:pk>/delete/', StockOutJudicialDeleteView.as_view(), name='stock_out_judicial-delete'),

]

urlpatterns += [

    path('judicial/transfer/', TransferJudicialListView.as_view(), name='transfer-judicial-list'),
    # path('judicial/transfer/add/', TransferJudicialCreateView.as_view(), name='transfer_judicial-create'),
    path('judicial/transfer/<int:pk>/detail/', TransferJudicialDetailView.as_view(), name='transfer_judicial-detail'),
    # path('judicial/transfer/<int:pk>/change/', TransferJudicialUpdateView.as_view(), name='transfer_judicial-update'),

]

urlpatterns += [

    path('judicial/request/', RequestJudicialListView.as_view(), name='request_judicial-list'),
    path('judicial/request/<int:pk>/detail/', RequestJudicialDetailView.as_view(), name='request_judicial-detail'),
    path('judicial/request/<int:pk>/change/', RequestJudicialUpdateView.as_view(), name='request_judicial-update'),
    path('judicial/request/<int:pk>/delete/', RequestJudicialDeleteView.as_view(), name='request_judicial-delete'),
]

urlpatterns += [
    path('reports/non-judicial/', ReportDenomination.as_view(), name='overall-reports'),
    path('reports/judicial/', ReportJudicialDenomination.as_view(), name='overall-reports-judicial'),
    path('reports/consolidated/', ReportConsolidatedView.as_view(), name='consolidated-reports'),
]
