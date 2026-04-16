from django.contrib import admin
from .models import Market


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'event_date', 'price_a_sats', 'price_b_sats', 'resolved', 'winner_idx')
    list_filter = ('resolved',)
    search_fields = ('title',)
