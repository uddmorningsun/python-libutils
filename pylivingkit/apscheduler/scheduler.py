import typing
import logging

from apscheduler import events
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.schedulers.gevent import GeventScheduler

from pylivingkit.apscheduler.config import gconfig


def create_scheduler(
    name: str, scheduler_class: typing.Optional[typing.Type[BaseScheduler]], key_prefix=None, **kwargs
):
    """With default configuration initialize Scheduler.

    If param `scheduler_class` is not None, higher priority than name.
    """
    if scheduler_class:
        if not issubclass(scheduler_class, BaseScheduler):
            raise ValueError("scheduler_class %r is not a %s subclass" % (scheduler_class, BaseScheduler.__name__))
        return scheduler_class(gconfig, prefix=kwargs.pop("prefix", key_prefix), **kwargs)
    scheduler = GeventScheduler(gconfig, prefix=kwargs.pop("prefix", key_prefix), **kwargs)
    scheduler.add_listener(attach_job_added_event, mask=events.EVENT_JOB_ADDED)
    return scheduler


def attach_job_added_event(event_obj: events.JobEvent):
    logging.info("add job: (%r:%r) stored in %s jobstore", event_obj.job_id, event_obj.alias, event_obj.jobstore)
