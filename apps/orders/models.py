import uuid
from django.db import models
from django.conf import settings


class Order(models.Model):
    STATUS_CHOICES = [
        ('open', 'Ouvert'),
        ('settled_win', 'Gagné'),
        ('settled_loss', 'Perdu'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
    )
    market = models.ForeignKey(
        'markets.Market',
        on_delete=models.CASCADE,
        related_name='orders',
    )
    outcome_idx = models.IntegerField()  # 0 ou 1
    shares = models.IntegerField()
    price_per_share_sats = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    settled_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.id} – {self.user.username} sur {self.market_id}"

    @property
    def total_cost_sats(self):
        return self.shares * self.price_per_share_sats
