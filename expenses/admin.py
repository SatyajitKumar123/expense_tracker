from django.contrib import admin
from django.db import models
from .models import Category, Expense


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'amount', 'date', 'payment_method', 'created_at')
    list_filter = ('category', 'payment_method', 'date', 'created_at')
    search_fields = ('description',)
    date_hierarchy = 'date'

    readonly_fields = ('created_at',)

    actions = ['mark_description_verified']

    def mark_description_verified(self, request, queryset):
        update_count = queryset.update(description=models.F('description') + ' (verified)')
        self.message_user(request, f"{update_count} expenses marked as verified.")
    mark_description_verified.short_description = "Append '(verified)' to description"