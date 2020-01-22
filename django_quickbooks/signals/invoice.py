from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver

from django_quickbooks import get_realm_model, QUICKBOOKS_ENUMS
from django_quickbooks.signals import invoice_created, invoice_updated, qbd_task_create

RealmModel = get_realm_model()


@receiver(invoice_created)
def create_qbd_invoice(sender, qbd_model_mixin_obj, schema_name, *args, **kwargs):
    qbd_task_create.send(
        sender=qbd_model_mixin_obj.__class__,
        qb_operation=QUICKBOOKS_ENUMS.OPP_ADD,
        qb_resource=QUICKBOOKS_ENUMS.RESOURCE_INVOICE,
        object_id=qbd_model_mixin_obj.id,
        content_type=ContentType.objects.get_for_model(qbd_model_mixin_obj),
        schema_name=schema_name,
    )


@receiver(invoice_updated)
def update_qbd_invoice(sender, qbd_model_mixin_obj, schema_name, *args, **kwargs):
    qbd_task_create.send(
        sender=qbd_model_mixin_obj.__class__,
        qb_operation=QUICKBOOKS_ENUMS.OPP_MOD,
        qb_resource=QUICKBOOKS_ENUMS.RESOURCE_INVOICE,
        object_id=qbd_model_mixin_obj.id,
        content_type=ContentType.objects.get_for_model(qbd_model_mixin_obj),
        schema_name=schema_name,
    )
