import logging
from datetime import timedelta, datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution


from NewsPaper import settings
from news.models import Post, Subscription

logger = logging.getLogger(__name__)

# Эта функция рассылает сообщения пользователям, но они могут видеть других пользователей кому были отправлены такие же сообщения
# def my_job():
#     categories = Category.objects.all()
#     today = datetime.now()
#     week_later = today - timedelta(weeks=1)
#     for category in categories:
#         users = User.objects.filter(subscriptions__category=category).values_list('email', flat=True)
#         emails = [email for email in users if email]
#         posts = Post.objects.filter(time_in__gt=week_later)
#         context = '\n'.join([f"{p.header} - {p.content}" for p in posts][:10])
#         send_mail("Рассылка", context, None, emails)


def my_job():
    subscriptions = Subscription.objects.all()
    today = datetime.now()
    later_week = today - timedelta(weeks=1)
    for sub in subscriptions:
        if sub.user.email:
            header = f"Рассылка по категории {sub.category}"
            posts = Post.objects.filter(time_in__gte=later_week, category=sub.category)[:10]
            context = '\n'.join([f'"http://127.0.0.1:8000{post.get_absolute_url()} Ссылка на пост \n'
                                 f'Заголовок{post.header} - Содержание{post.preview()}' for post in posts])
            user = sub.user.email
            send_mail(header, context, None, [user])


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week='fry', hour='18'),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info('Added job "my_job".')

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
