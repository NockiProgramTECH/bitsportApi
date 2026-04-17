from django.db import models
from django.conf import settings


class Market(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=255)
    event_date = models.DateField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    price_a_sats = models.IntegerField()
    price_b_sats = models.IntegerField()
    votes_a = models.IntegerField(default=1)  # Initialisé à 1 pour éviter div par zero et avoir 50/50
    votes_b = models.IntegerField(default=1)
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

    def update_prices(self):
        """
        Calcule les prix dynamiquement.
        Par défaut, si votes_a == votes_b, cote = 10.
        Cote = Payout / Prix. Donc Prix = Payout / 10.
        Si le pourcentage augmente, la cote diminue (donc le prix augmente).
        """
        total_votes = self.votes_a + self.votes_b
        payout = getattr(settings, 'PAYOUT_PER_SHARE_SATS', 10000)
        
        # Formule : Prix = (Payout / 5) * (Votes / TotalVotes)
        # Si Votes/TotalVotes = 0.5, Prix = Payout / 10
        self.price_a_sats = int((payout / 5) * (self.votes_a / total_votes))
        self.price_b_sats = int((payout / 5) * (self.votes_b / total_votes))
        
        # Sécurité pour ne pas avoir de prix nul ou trop élevé
        self.price_a_sats = max(1, min(self.price_a_sats, payout - 1))
        self.price_b_sats = max(1, min(self.price_b_sats, payout - 1))
        self.save()
