from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import PostCategory


@receiver(m2m_changed, sender=PostCategory)
def post_create(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        emails = set()
        categories_names = ', '.join([cat.category for cat in categories])

        for cat in categories:
            users = User.objects.filter(subscriptions__category=cat).values_list('email', flat=True)
            for user in users:
                if user:
                    emails.add(user)

        subject = f'Новый пост в категории {categories_names}.'

        text_content = (
            f'Заголовок: {instance.header}\n'
            f'Пост: {instance.is_post}\n'
            f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">Ссылка на пост</a>'
        )

        html_content = (
            f'Заголовок: {instance.header}<br>'
            f'Пост: {instance.is_post}<br><br>'
            f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">Ссылка на пост</a>'
        )

        for email in emails:
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()





