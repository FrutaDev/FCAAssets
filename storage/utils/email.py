from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.db import transaction
from datetime import date
from storage.models import Maintenance
from django.conf import settings

def send_maintenance_email():
    today = now().date()
    
    queryset = Maintenance.objects.filter(
        is_approved=True,
        upcoming_maintenance__isnull=False
    )

    for maintenance in queryset:
        days_until_maintenance = (maintenance.upcoming_maintenance - today).days

        if days_until_maintenance == 30 and not maintenance.email_sent_30_days:
            __send_email_for(maintenance, kind='30_days')

        if days_until_maintenance == 7 and not maintenance.email_sent_30_days:
            __send_email_for(maintenance, kind='7_days')

        if days_until_maintenance == 0 and not maintenance.email_sent_30_days:
            __send_email_for(maintenance, kind='due')


    def __send_email_for(maintenance, kind):
        subject = ''
        template = ''

        if kind == '30_days':
            subject = f'Recordatorio: Mantenimiento para {maintenance.machinary_maintenance.serial} en 30 días'
            template = 'emails/maintenance_30_days.html'
            flag_field = 'email_sent_30_days'
        elif kind == '7_days':
            subject = f'Recordatorio: Mantenimiento para {maintenance.machinary_maintenance.serial} en 15 días'
            template = 'emails/maintenance_15_days.html'
            flag_field = 'email_sent_7_days'
        else:
            subject = f'Notificación: Mantenimiento para {maintenance.machinary_maintenance.serial} es hoy'
            template = 'emails/maintenance_due.html'
            flag_field = 'email_sent_due'

        context = {
            'maintenance': maintenance,
            'machinery': maintenance.machinary_maintenance,
            'days_remaining': (maintenance.upcoming_maintenance - date.today()).days,
        }
        body = render_to_string(template, context)


        recipient_list = settings.MAINTENANCE_NOTIFICATION_ADMINS

        try:
            with transaction.atomic():
                email = EmailMessage(
                    subject=subject,
                    body=body,
                    to=recipient_list,
                )
                email.content_subtype = "html"
                email.send(fail_silently=False)

                setattr(maintenance, flag_field, True)
                maintenance.save(update_fields=[flag_field])
        except Exception as e:
            print(f"Error sending email for maintenance {maintenance.id}: {e}")