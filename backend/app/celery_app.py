from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)
celery_app.conf.beat_schedule = {
    "update_daily_returns": {
        "task": "app.tasks.update_daily_returns",
        "schedule": 3600.0, 
    }
}
celery_app.conf.timezone = "UTC"
