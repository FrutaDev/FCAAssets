from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.db import transaction
from datetime import date
from django.utils import timezone
from storage.models import Maintenance
import logging


logger = logging.getLogger("maintenance_scheduler")


def send_maintenance_email(maintenance, days_before):

    if days_before == 30:
        kind = "30_days"
    elif days_before == 7:
        kind = "7_days"
    else:
        kind = "due"

    return __send_email_for(maintenance, kind)


def __send_email_for(maintenance, kind):

    if kind == '30_days':
        subject = f'Recordatorio: Mantenimiento para {maintenance.machinary_maintenance.serial} en 30 días'
        template = 'storage/emails/email_sent_30_days.html'
        flag_field = 'email_sent_30_days'

    elif kind == '7_days':
        subject = f'Recordatorio: Mantenimiento para {maintenance.machinary_maintenance.serial} en 7 días'
        template = 'storage/emails/email_sent_7_days.html'
        flag_field = 'email_sent_7_days'

    else:
        subject = f'Notificación: Mantenimiento para {maintenance.machinary_maintenance.serial} es hoy'
        template = 'storage/emails/email_sent_due.html'
        flag_field = 'email_sent_due'

    context = {
        'maintenance': maintenance,
        'machinery': maintenance.machinary_maintenance,
        'days_remaining': (maintenance.maintenance_date - date.today()).days,
    }

    body = render_to_string(template, context)
    recipient_list = settings.MAINTENANCE_NOTIFICATION_ADMINS

    with transaction.atomic():
        msg = EmailMessage(
            subject=subject,
            body=body,
            to=recipient_list,
        )
        msg.content_subtype = "html"
        msg.send(fail_silently=False)

        setattr(maintenance, flag_field, True)
        maintenance.save(update_fields=[flag_field])


def job_send_maintenance_emails():
    today = timezone.now().date()

    jobs = [
        (30, "email_sent_30_days"),
        (7,  "email_sent_7_days"),
        (0,  "email_sent_due"),
    ]

    for days, flag in jobs:
        records = Maintenance.objects.filter(
            maintenance_date=today + timedelta(days=days),
            **{flag: False}
        )

        for m in records:
            try:
                send_maintenance_email(m, days)
                logger.info(f"Email enviado ({days} días) para ID={m.pk}")
            except Exception:
                logger.exception(f"Error enviando correo ({days} días) para ID={m.pk}")
 