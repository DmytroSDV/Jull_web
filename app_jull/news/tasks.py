from celery import shared_task


@shared_task
def test_func():
    return "tests"
