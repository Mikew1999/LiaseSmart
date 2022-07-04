''' List of background tasks '''
from celery import Celery
from .bg_processes.check_pending_notifications import return_notifications

app = Celery()


class Config:
    ''' Celery config '''
    enable_utc = True
    timezone = 'Europe/London'


app.config_from_object(Config)


@app.task
def check_notifications():
    ''' Checks notifications and prints them '''
    notifications = return_notifications()
    for key, value in notifications:
        print(f'key: {key}, value: {value}')


if __name__ == '__main__':
    app.worker_main()
