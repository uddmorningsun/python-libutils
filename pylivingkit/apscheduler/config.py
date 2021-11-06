import os

SQLALCHEMY_ENGINE_URL = "SQLALCHEMY_ENGINE_URL"


# `apscheduler.schedulers.base.BaseScheduler._real_add_job` will fill missed job params.
job_defaults = {
    "misfire_grace_time": 1,
    "max_instances": 1,
    # bool or ('true', 'yes', 'on', 'y', 't', '1') or ('false', 'no', 'off', 'n', 'f', '0')
    "coalesce": True,
}

executors = {
    # If not setting fixed default, apscheduler will initialize default with ThreadPoolExecutor.
    "default": {
        # Priority: type > class
        # param type: `entry_points.txt` file records mapping
        "type": "gevent",
        "class": "apscheduler.executors.gevent:GeventExecutor",
        # Options for class or type
    },
    # Priority: instance object with {"nickname": executor_obj} > mapping
    # "alias_name_executor": isinstance(value, BaseExecutor)
    "nickname_debug_executor": {
        "type": "",
        "class": "apscheduler.executors.debug:DebugExecutor",
    },
    "nickname_threadpool_executor": {
        "type": "threadpool",
        "class": "apscheduler.executors.pool:ThreadPoolExecutor",
    },
    "nickname_processpool_executor": {
        "type": "processpool",
        "class": "apscheduler.executors.pool:ProcessPoolExecutor",
    },
    "nickname_tornado_executor": {
        "type": "",
        "class": "apscheduler.executors.tornado:TornadoExecutor",
    },
}

jobstores = {
    # "alias_name_jobstore": isinstance(value, BaseJobStore)
    # default MemoryJobStore
    "default": {
        "type": "memory",
        "class": "",
    },
    "nickname_sqlalchemy_jobstore": {
        "type": "",
        "class": "apscheduler.jobstores.sqlalchemy:SQLAlchemyJobStore",
        # rfc1738 URL format
        "url": os.getenv(SQLALCHEMY_ENGINE_URL, "sqlite+pysqlite:///db.sqlite3"),
        "engine_options": {},
    },
    "nickname_redis_jobstore": {
        "type": "",
        "class": "apscheduler.jobstores.redis:RedisJobStore",
    },
}

gconfig = {
    "job_defaults": job_defaults,
    "executors": executors,
    "jobstores": jobstores,
}
