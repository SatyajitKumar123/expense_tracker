from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Sum
from django.utils import timezone

from .models import Expense, Category
from .forms import ExpenseForm


class ExpenseListView(ListView):
    model = Expense
    template_name = 'expenses/expense_list.html'
    context_object_name = 'expenses'
    paginate_by = 10  # pagination

    def get_queryset(self):
        qs = super().get_queryset()

        # Simple filter by category and date range via query params
        category_id = self.request.GET.get('category')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if category_id:
            qs = qs.filter(category_id=category_id)

        if start_date:
            qs = qs.filter(date__gte=start_date)

        if end_date:
            qs = qs.filter(date__lte=end_date)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = context['expenses']

        # total of filtered expenses
        total = queryset.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

        context['total_amount'] = total
        context['categories'] = Category.objects.all()
        context['today'] = timezone.now().date()
        return context


class ExpenseCreateView(CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expenses:expense_list')


class ExpenseUpdateView(UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expenses:expense_list')


class ExpenseDeleteView(DeleteView):
    model = Expense
    template_name = 'expenses/expense_confirm_delete.html'
    success_url = reverse_lazy('expenses:expense_list')
