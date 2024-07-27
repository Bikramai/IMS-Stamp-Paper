from django.db.models.signals import pre_delete
from django.dispatch import receiver

from src.accounts.models import Treasury


@receiver(pre_delete, sender=Treasury)
def pre_treasury_delete(sender, instance, **kwargs):

    instance.stockin_set.filter(source_treasury=instance).delete()
    instance.stockout_set.filter(source_treasury=instance).delete()
    instance.get_all_transfers().delete()
    instance.get_all_transfers_judicial().delete()

