from django.db import models


class Market(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=255)
    event_date = models.DateField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    price_a_sats = models.IntegerField()
    price_b_sats = models.IntegerField()
    resolved = models.BooleanField(default=False)
    winner_idx = models.IntegerField(null=True, blank=True)  # 0 ou 1
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'markets'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_option(self, idx):
        return self.option_a if idx == 0 else self.option_b

    def get_price(self, idx):
        return self.price_a_sats if idx == 0 else self.price_b_sats
