from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from django.db.models import F
from django.conf import settings
from django.utils import timezone
from .models import Market

@receiver(post_save, sender=Market)
def handle_market_resolution(sender, instance, created, **kwargs):
    """
    Déclenché chaque fois qu'un Marché est sauvegardé.
    Si le marché est marqué comme résolu, on traite les paiements.
    """
    # On ne traite que si le marché est résolu et qu'un gagnant est défini
    if instance.resolved and instance.winner_idx is not None:
        from apps.orders.models import Order
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        
        # On utilise une transaction atomique pour garantir l'intégrité des données
        with transaction.atomic():
            # On récupère tous les ordres 'open' pour ce marché spécifique
            # select_for_update() verrouille les lignes pour éviter les accès concurrents
            open_orders = Order.objects.filter(
                market=instance, 
                status='open'
            ).select_for_update()
            
            now = timezone.now()
            
            for order in open_orders:
                if order.outcome_idx == instance.winner_idx:
                    # Calcul du gain (Parts * Payout par part)
                    payout = order.shares * settings.PAYOUT_PER_SHARE_SATS
                    
                    # Créditer le solde de l'utilisateur
                    User.objects.filter(pk=order.user_id).update(
                        balance_sats=F('balance_sats') + payout
                    )
                    
                    order.status = 'settled_win'
                else:
                    # Le pari est perdu
                    order.status = 'settled_loss'
                
                # Mise à jour de l'ordre
                order.settled_at = now
                order.save(update_fields=['status', 'settled_at'])
