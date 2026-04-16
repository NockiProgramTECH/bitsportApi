from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'market', 'outcome_idx', 'shares', 'price_per_share_sats', 'status', 'created_at')
    list_filter = ('status', 'outcome_idx')
    search_fields = ('user__username', 'market__title')
    raw_id_fields = ('user', 'market')
