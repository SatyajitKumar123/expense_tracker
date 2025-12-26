from django.urls import path
from .views import (
    ExpenseListView,
    ExpenseCreateView,
    ExpenseUpdateView,
    ExpenseDeleteView,
)

app_name = 'expenses'

urlpatterns = [
    path('', ExpenseListView.as_view(), name='expense_list'),
    path('add/', ExpenseCreateView.as_view(), name='expense_create'),
    path('<int:pk>/edit/', ExpenseUpdateView.as_view(), name='expense_update'),
    path('<int:pk>/edit/', ExpenseDeleteView.as_view(), name='expense_delete'),
]
