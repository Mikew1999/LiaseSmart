''' List of background tasks '''
from celery import Celery

app = Celery()


class Config:
    ''' Celery config '''
    enable_utc = True
    timezone = 'Europe/London'


app.config_from_object(Config)

if __name__ == '__main__':
    app.worker_main()
