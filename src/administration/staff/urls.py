from django.urls import path

from .views import (
    DashboardView, UserDetailView, StockInListView, StockInCreateView, StockOutListView,
    StockOutCreateView, TransferListView, TransferCreateView, UserListView, StockInDetailView, StockOutDetailView,
    TransferDetailView, PasswordChangeView, StockInJudicialCreateView,
    StockOutJudicialDetailView, StockOutJudicialCreateView, StockOutJudicialListView, StockInJudicialDetailView,
    StockInJudicialListView, TransferJudicialDetailView, TransferJudicialListView, TransferJudicialCreateView
)
from ..admins.views import TreasuryDetailView

app_name = 'staff'
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('password/change/', PasswordChangeView.as_view(), name='password-change'),

    path('user/', UserListView.as_view(), name='user-list'),
    path('user/<int:pk>/detail/', UserDetailView.as_view(), name='user-detail'),
]

urlpatterns += [
    path('treasury/<int:pk>/', TreasuryDetailView.as_view(), name='treasury-detail'),
]

urlpatterns += [
    path('non_judicial/stockin/', StockInListView.as_view(), name='stock-in-list'),
    path('non_judicial/stockin/<int:pk>/detail/', StockInDetailView.as_view(), name='stock_in-detail'),
    path('non_judicial/stockin/add/', StockInCreateView.as_view(), name='stock_in-create'),
]

urlpatterns += [
    path('non_judicial/stockout/', StockOutListView.as_view(), name='stock-out-list'),
    path('non_judicial/stockout/add/', StockOutCreateView.as_view(), name='stock_out-create'),
    path('non_judicial/stockout/<int:pk>/detail/', StockOutDetailView.as_view(), name='stock_out-detail'),
]

urlpatterns += [
    path('non_judicial/transfer/', TransferListView.as_view(), name='transfer-list'),
    path('non_judicial/transfer/add/', TransferCreateView.as_view(), name='transfer-create'),
    path('non_judicial/transfer/<int:pk>/detail/', TransferDetailView.as_view(), name='transfer-detail'),
]


urlpatterns += [
    path('judicial/stockin/', StockInJudicialListView.as_view(), name='stock-in-judicial-list'),
    path('judicial/stockin/<int:pk>/detail/', StockInJudicialDetailView.as_view(), name='stock_in_judicial-detail'),
    path('judicial/stockin/add/', StockInJudicialCreateView.as_view(), name='stock_in_judicial-create'),

]

urlpatterns += [
    path('judicial/stockout/', StockOutJudicialListView.as_view(), name='stock-out-judicial-list'),
    path('judicial/stockout/add/', StockOutJudicialCreateView.as_view(), name='stock_out_judicial-create'),
    path('judicial/stockout/<int:pk>/detail/', StockOutJudicialDetailView.as_view(), name='stock_out_judicial-detail'),
]

urlpatterns += [
    path('judicial/transfer/', TransferJudicialListView.as_view(), name='transfer-judicial-list'),
    path('judicial/transfer/add/', TransferJudicialCreateView.as_view(), name='transfer_judicial-create'),
    path('judicial/transfer/<int:pk>/detail/', TransferJudicialDetailView.as_view(), name='transfer_judicial-detail'),
]

