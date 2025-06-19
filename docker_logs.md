db          | 2025-06-19 10:13:34.997 | 2025-06-19 13:13:34+00:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 8.4.0-1.el9 started.
redis       | 2025-06-19 10:13:35.035 | Starting Redis Server
redis       | 2025-06-19 10:13:35.047 | 1:C 19 Jun 2025 13:13:35.047 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
redis       | 2025-06-19 10:13:35.047 | 1:C 19 Jun 2025 13:13:35.047 * Redis version=8.0.2, bits=64, commit=00000000, modified=1, pid=1, just started
redis       | 2025-06-19 10:13:35.047 | 1:C 19 Jun 2025 13:13:35.047 * Configuration loaded
redis       | 2025-06-19 10:13:35.047 | 1:M 19 Jun 2025 13:13:35.047 * monotonic clock: POSIX clock_gettime
redis       | 2025-06-19 10:13:35.047 | 1:M 19 Jun 2025 13:13:35.047 * Running mode=standalone, port=6379.
redis       | 2025-06-19 10:13:35.048 | 1:M 19 Jun 2025 13:13:35.048 * <bf> RedisBloom version 8.0.1 (Git=unknown)
redis       | 2025-06-19 10:13:35.048 | 1:M 19 Jun 2025 13:13:35.048 * <bf> Registering configuration options: [
redis       | 2025-06-19 10:13:35.048 | 1:M 19 Jun 2025 13:13:35.048 * <bf> 	{ bf-error-rate       :      0.01 }
redis       | 2025-06-19 10:13:35.048 | 1:M 19 Jun 2025 13:13:35.048 * <bf> 	{ bf-initial-size     :       100 }
redis       | 2025-06-19 10:13:35.048 | 1:M 19 Jun 2025 13:13:35.048 * <bf> 	{ bf-expansion-factor :         2 }
redis       | 2025-06-19 10:13:35.048 | 1:M 19 Jun 2025 13:13:35.048 * <bf> 	{ cf-bucket-size      :         2 }
redis       | 2025-06-19 10:13:35.048 | 1:M 19 Jun 2025 13:13:35.048 * <bf> 	{ cf-initial-size     :      1024 }
redis       | 2025-06-19 10:13:35.048 | 1:M 19 Jun 2025 13:13:35.048 * <bf> 	{ cf-max-iterations   :        20 }
redis       | 2025-06-19 10:13:35.048 | 1:M 19 Jun 2025 13:13:35.048 * <bf> 	{ cf-expansion-factor :         1 }
redis       | 2025-06-19 10:13:35.048 | 1:M 19 Jun 2025 13:13:35.048 * <bf> 	{ cf-max-expansions   :        32 }
redis       | 2025-06-19 10:13:35.048 | 1:M 19 Jun 2025 13:13:35.048 * <bf> ]
redis       | 2025-06-19 10:13:35.048 | 1:M 19 Jun 2025 13:13:35.048 * Module 'bf' loaded from /usr/local/lib/redis/modules//redisbloom.so
redis       | 2025-06-19 10:13:35.051 | 1:M 19 Jun 2025 13:13:35.050 * <search> Redis version found by RedisSearch : 8.0.2 - oss
redis       | 2025-06-19 10:13:35.051 | 1:M 19 Jun 2025 13:13:35.050 * <search> RediSearch version 8.0.1 (Git=5688fcc)
redis       | 2025-06-19 10:13:35.052 | 1:M 19 Jun 2025 13:13:35.050 * <search> Low level api version 1 initialized successfully
redis       | 2025-06-19 10:13:35.052 | 1:M 19 Jun 2025 13:13:35.050 * <search> gc: ON, prefix min length: 2, min word length to stem: 4, prefix max expansions: 200, query timeout (ms): 500, timeout policy: return, cursor read size: 1000, cursor max idle (ms): 300000, max doctable size: 1000000, max number of search results:  1000000, 
redis       | 2025-06-19 10:13:35.052 | 1:M 19 Jun 2025 13:13:35.050 * <search> Initialized thread pools!
redis       | 2025-06-19 10:13:35.052 | 1:M 19 Jun 2025 13:13:35.050 * <search> Disabled workers threadpool of size 0
redis       | 2025-06-19 10:13:35.052 | 1:M 19 Jun 2025 13:13:35.050 * <search> Subscribe to config changes
redis       | 2025-06-19 10:13:35.052 | 1:M 19 Jun 2025 13:13:35.050 * <search> Enabled role change notification
redis       | 2025-06-19 10:13:35.052 | 1:M 19 Jun 2025 13:13:35.050 * <search> Cluster configuration: AUTO partitions, type: 0, coordinator timeout: 0ms
redis       | 2025-06-19 10:13:35.052 | 1:M 19 Jun 2025 13:13:35.051 * <search> Register write commands
redis       | 2025-06-19 10:13:35.052 | 1:M 19 Jun 2025 13:13:35.051 * Module 'search' loaded from /usr/local/lib/redis/modules//redisearch.so
redis       | 2025-06-19 10:13:35.052 | 1:M 19 Jun 2025 13:13:35.051 * <timeseries> RedisTimeSeries version 80001, git_sha=577bfa8b5909e7ee572f0b651399be8303dc6641
redis       | 2025-06-19 10:13:35.052 | 1:M 19 Jun 2025 13:13:35.051 * <timeseries> Redis version found by RedisTimeSeries : 8.0.2 - oss
redis       | 2025-06-19 10:13:35.052 | 1:M 19 Jun 2025 13:13:35.051 * <timeseries> Registering configuration options: [
redis       | 2025-06-19 10:13:35.052 | 1:M 19 Jun 2025 13:13:35.051 * <timeseries> 	{ ts-compaction-policy   :              }
redis       | 2025-06-19 10:13:35.052 | 1:M 19 Jun 2025 13:13:35.051 * <timeseries> 	{ ts-num-threads         :            3 }
redis       | 2025-06-19 10:13:35.052 | 1:M 19 Jun 2025 13:13:35.051 * <timeseries> 	{ ts-retention-policy    :            0 }
redis       | 2025-06-19 10:13:35.052 | 1:M 19 Jun 2025 13:13:35.051 * <timeseries> 	{ ts-duplicate-policy    :        block }
redis       | 2025-06-19 10:13:35.052 | 1:M 19 Jun 2025 13:13:35.051 * <timeseries> 	{ ts-chunk-size-bytes    :         4096 }
redis       | 2025-06-19 10:13:35.052 | 1:M 19 Jun 2025 13:13:35.051 * <timeseries> 	{ ts-encoding            :   compressed }
redis       | 2025-06-19 10:13:35.052 | 1:M 19 Jun 2025 13:13:35.051 * <timeseries> 	{ ts-ignore-max-time-diff:            0 }
redis       | 2025-06-19 10:13:35.052 | 1:M 19 Jun 2025 13:13:35.051 * <timeseries> 	{ ts-ignore-max-val-diff :     0.000000 }
redis       | 2025-06-19 10:13:35.052 | 1:M 19 Jun 2025 13:13:35.051 * <timeseries> ]
redis       | 2025-06-19 10:13:35.052 | 1:M 19 Jun 2025 13:13:35.051 * <timeseries> Detected redis oss
redis       | 2025-06-19 10:13:35.052 | 1:M 19 Jun 2025 13:13:35.051 * Module 'timeseries' loaded from /usr/local/lib/redis/modules//redistimeseries.so
redis       | 2025-06-19 10:13:35.052 | 1:M 19 Jun 2025 13:13:35.052 * <ReJSON> Created new data type 'ReJSON-RL'
redis       | 2025-06-19 10:13:35.053 | 1:M 19 Jun 2025 13:13:35.053 * <ReJSON> version: 80001 git sha: unknown branch: unknown
redis       | 2025-06-19 10:13:35.053 | 1:M 19 Jun 2025 13:13:35.053 * <ReJSON> Exported RedisJSON_V1 API
redis       | 2025-06-19 10:13:35.053 | 1:M 19 Jun 2025 13:13:35.053 * <ReJSON> Exported RedisJSON_V2 API
redis       | 2025-06-19 10:13:35.053 | 1:M 19 Jun 2025 13:13:35.053 * <ReJSON> Exported RedisJSON_V3 API
redis       | 2025-06-19 10:13:35.053 | 1:M 19 Jun 2025 13:13:35.053 * <ReJSON> Exported RedisJSON_V4 API
redis       | 2025-06-19 10:13:35.053 | 1:M 19 Jun 2025 13:13:35.053 * <ReJSON> Exported RedisJSON_V5 API
redis       | 2025-06-19 10:13:35.053 | 1:M 19 Jun 2025 13:13:35.053 * <ReJSON> Enabled diskless replication
redis       | 2025-06-19 10:13:35.053 | 1:M 19 Jun 2025 13:13:35.053 * <ReJSON> Initialized shared string cache, thread safe: false.
redis       | 2025-06-19 10:13:35.053 | 1:M 19 Jun 2025 13:13:35.053 * Module 'ReJSON' loaded from /usr/local/lib/redis/modules//rejson.so
redis       | 2025-06-19 10:13:35.053 | 1:M 19 Jun 2025 13:13:35.053 * <search> Acquired RedisJSON_V5 API
redis       | 2025-06-19 10:13:35.059 | 1:M 19 Jun 2025 13:13:35.057 * Server initialized
redis       | 2025-06-19 10:13:35.059 | 1:M 19 Jun 2025 13:13:35.057 * <search> Loading event starts
redis       | 2025-06-19 10:13:35.059 | 1:M 19 Jun 2025 13:13:35.057 * <search> Enabled workers threadpool of size 4
redis       | 2025-06-19 10:13:35.059 | 1:M 19 Jun 2025 13:13:35.057 * Loading RDB produced by version 8.0.2
redis       | 2025-06-19 10:13:35.059 | 1:M 19 Jun 2025 13:13:35.057 * RDB age 11 seconds
redis       | 2025-06-19 10:13:35.059 | 1:M 19 Jun 2025 13:13:35.057 * RDB memory usage when created 1.37 Mb
redis       | 2025-06-19 10:13:35.059 | 1:M 19 Jun 2025 13:13:35.057 * Done loading RDB, keys loaded: 2, keys expired: 0.
redis       | 2025-06-19 10:13:35.059 | 1:M 19 Jun 2025 13:13:35.057 * <search> Disabled workers threadpool of size 4
redis       | 2025-06-19 10:13:35.059 | 1:M 19 Jun 2025 13:13:35.057 * <search> Loading event ends
redis       | 2025-06-19 10:13:35.059 | 1:M 19 Jun 2025 13:13:35.057 * DB loaded from disk: 0.000 seconds
redis       | 2025-06-19 10:13:35.059 | 1:M 19 Jun 2025 13:13:35.057 * Ready to accept connections tcp
db          | 2025-06-19 10:13:35.188 | 2025-06-19 13:13:35+00:00 [Note] [Entrypoint]: Switching to dedicated user 'mysql'
db          | 2025-06-19 10:13:35.193 | 2025-06-19 13:13:35+00:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 8.4.0-1.el9 started.
db          | 2025-06-19 10:13:35.376 | '/var/lib/mysql/mysql.sock' -> '/var/run/mysqld/mysqld.sock'
db          | 2025-06-19 10:13:35.564 | 2025-06-19T13:13:35.387205Z 0 [System] [MY-015015] [Server] MySQL Server - start.
db          | 2025-06-19 10:13:35.564 | 2025-06-19T13:13:35.562314Z 0 [System] [MY-010116] [Server] /usr/sbin/mysqld (mysqld 8.4.0) starting as process 1
db          | 2025-06-19 10:13:35.567 | 2025-06-19T13:13:35.567554Z 1 [System] [MY-013576] [InnoDB] InnoDB initialization has started.
db          | 2025-06-19 10:13:35.722 | 2025-06-19T13:13:35.722018Z 1 [System] [MY-013577] [InnoDB] InnoDB initialization has ended.
db          | 2025-06-19 10:13:35.893 | 2025-06-19T13:13:35.893554Z 0 [Warning] [MY-010068] [Server] CA certificate ca.pem is self signed.
db          | 2025-06-19 10:13:35.893 | 2025-06-19T13:13:35.893575Z 0 [System] [MY-013602] [Server] Channel mysql_main configured to support TLS. Encrypted connections are now supported for this channel.
db          | 2025-06-19 10:13:35.898 | 2025-06-19T13:13:35.898788Z 0 [Warning] [MY-011810] [Server] Insecure configuration for --pid-file: Location '/var/run/mysqld' in the path is accessible to all OS users. Consider choosing a different directory.
db          | 2025-06-19 10:13:35.912 | 2025-06-19T13:13:35.912616Z 0 [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections. Version: '8.4.0'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server - GPL.
db          | 2025-06-19 10:13:36.166 | 2025-06-19T13:13:36.166567Z 0 [System] [MY-011323] [Server] X Plugin ready for connections. Bind-address: '::' port: 33060, socket: /var/run/mysqld/mysqlx.sock
celery-beat | 2025-06-19 10:13:40.182 | wait-for-it.sh: waiting 120 seconds for db:3306
celery-beat | 2025-06-19 10:13:40.186 | wait-for-it.sh: db:3306 is available after 0 seconds
celery      | 2025-06-19 10:13:40.199 | wait-for-it.sh: waiting 120 seconds for db:3306
celery      | 2025-06-19 10:13:40.205 | wait-for-it.sh: db:3306 is available after 0 seconds
celery-beat | 2025-06-19 10:13:40.522 | Traceback (most recent call last):
celery-beat | 2025-06-19 10:13:40.522 |   File "/app/manage.py", line 18, in <module>
celery-beat | 2025-06-19 10:13:40.525 |     main()
celery-beat | 2025-06-19 10:13:40.525 |   File "/app/manage.py", line 15, in main
celery-beat | 2025-06-19 10:13:40.525 |     execute_from_command_line(sys.argv)
celery-beat | 2025-06-19 10:13:40.525 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
celery-beat | 2025-06-19 10:13:40.526 |     utility.execute()
celery-beat | 2025-06-19 10:13:40.526 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 416, in execute
celery-beat | 2025-06-19 10:13:40.526 |     django.setup()
celery-beat | 2025-06-19 10:13:40.526 |   File "/usr/local/lib/python3.11/site-packages/django/__init__.py", line 24, in setup
celery-beat | 2025-06-19 10:13:40.526 |     apps.populate(settings.INSTALLED_APPS)
celery-beat | 2025-06-19 10:13:40.526 |   File "/usr/local/lib/python3.11/site-packages/django/apps/registry.py", line 91, in populate
celery-beat | 2025-06-19 10:13:40.528 |     app_config = AppConfig.create(entry)
celery-beat | 2025-06-19 10:13:40.528 |                  ^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-06-19 10:13:40.528 |   File "/usr/local/lib/python3.11/site-packages/django/apps/config.py", line 193, in create
celery-beat | 2025-06-19 10:13:40.528 |     import_module(entry)
celery-beat | 2025-06-19 10:13:40.528 |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
celery-beat | 2025-06-19 10:13:40.528 |     return _bootstrap._gcd_import(name[level:], package, level)
celery-beat | 2025-06-19 10:13:40.528 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-06-19 10:13:40.528 |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
celery-beat | 2025-06-19 10:13:40.528 |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
celery-beat | 2025-06-19 10:13:40.528 |   File "<frozen importlib._bootstrap>", line 1140, in _find_and_load_unlocked
celery-beat | 2025-06-19 10:13:40.528 | ModuleNotFoundError: No module named 'admin_interface'
celery      | 2025-06-19 10:13:40.614 | Traceback (most recent call last):
celery      | 2025-06-19 10:13:40.614 |   File "/usr/local/bin/celery", line 8, in <module>
celery      | 2025-06-19 10:13:40.614 |     sys.exit(main())
celery      | 2025-06-19 10:13:40.614 |              ^^^^^^
celery      | 2025-06-19 10:13:40.614 |   File "/usr/local/lib/python3.11/site-packages/celery/__main__.py", line 15, in main
celery      | 2025-06-19 10:13:40.616 |     sys.exit(_main())
celery      | 2025-06-19 10:13:40.616 |              ^^^^^^^
celery      | 2025-06-19 10:13:40.616 |   File "/usr/local/lib/python3.11/site-packages/celery/bin/celery.py", line 236, in main
celery      | 2025-06-19 10:13:40.617 |     return celery(auto_envvar_prefix="CELERY")
celery      | 2025-06-19 10:13:40.617 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:40.617 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1157, in __call__
celery      | 2025-06-19 10:13:40.619 |     return self.main(*args, **kwargs)
celery      | 2025-06-19 10:13:40.619 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:40.619 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1078, in main
celery      | 2025-06-19 10:13:40.619 |     rv = self.invoke(ctx)
celery      | 2025-06-19 10:13:40.619 |          ^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:40.619 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1688, in invoke
celery      | 2025-06-19 10:13:40.620 |     return _process_result(sub_ctx.command.invoke(sub_ctx))
celery      | 2025-06-19 10:13:40.620 |                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:40.620 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1434, in invoke
celery      | 2025-06-19 10:13:40.620 |     return ctx.invoke(self.callback, **ctx.params)
celery      | 2025-06-19 10:13:40.620 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:40.620 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 783, in invoke
celery      | 2025-06-19 10:13:40.620 |     return __callback(*args, **kwargs)
celery      | 2025-06-19 10:13:40.620 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:40.620 |   File "/usr/local/lib/python3.11/site-packages/click/decorators.py", line 33, in new_func
celery      | 2025-06-19 10:13:40.621 |     return f(get_current_context(), *args, **kwargs)
celery      | 2025-06-19 10:13:40.621 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:40.621 |   File "/usr/local/lib/python3.11/site-packages/celery/bin/base.py", line 135, in caller
celery      | 2025-06-19 10:13:40.621 |     return f(ctx, *args, **kwargs)
celery      | 2025-06-19 10:13:40.621 |            ^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:40.621 |   File "/usr/local/lib/python3.11/site-packages/celery/bin/worker.py", line 348, in worker
celery      | 2025-06-19 10:13:40.622 |     worker = app.Worker(
celery      | 2025-06-19 10:13:40.622 |              ^^^^^^^^^^^
celery      | 2025-06-19 10:13:40.622 |   File "/usr/local/lib/python3.11/site-packages/celery/worker/worker.py", line 93, in __init__
celery      | 2025-06-19 10:13:40.624 |     self.app.loader.init_worker()
celery      | 2025-06-19 10:13:40.624 |   File "/usr/local/lib/python3.11/site-packages/celery/loaders/base.py", line 110, in init_worker
celery      | 2025-06-19 10:13:40.624 |     self.import_default_modules()
celery      | 2025-06-19 10:13:40.624 |   File "/usr/local/lib/python3.11/site-packages/celery/loaders/base.py", line 104, in import_default_modules
celery      | 2025-06-19 10:13:40.624 |     raise response
celery      | 2025-06-19 10:13:40.625 |   File "/usr/local/lib/python3.11/site-packages/celery/utils/dispatch/signal.py", line 276, in send
celery      | 2025-06-19 10:13:40.626 |     response = receiver(signal=self, sender=sender, **named)
celery      | 2025-06-19 10:13:40.626 |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:40.626 |   File "/usr/local/lib/python3.11/site-packages/celery/fixups/django.py", line 100, in on_import_modules
celery      | 2025-06-19 10:13:40.627 |     self.worker_fixup.validate_models()
celery      | 2025-06-19 10:13:40.627 |   File "/usr/local/lib/python3.11/site-packages/celery/fixups/django.py", line 138, in validate_models
celery      | 2025-06-19 10:13:40.627 |     self.django_setup()
celery      | 2025-06-19 10:13:40.627 |   File "/usr/local/lib/python3.11/site-packages/celery/fixups/django.py", line 134, in django_setup
celery      | 2025-06-19 10:13:40.627 |     django.setup()
celery      | 2025-06-19 10:13:40.633 |   File "/usr/local/lib/python3.11/site-packages/django/__init__.py", line 24, in setup
celery      | 2025-06-19 10:13:40.633 |     apps.populate(settings.INSTALLED_APPS)
celery      | 2025-06-19 10:13:40.633 |   File "/usr/local/lib/python3.11/site-packages/django/apps/registry.py", line 91, in populate
celery      | 2025-06-19 10:13:40.633 |     app_config = AppConfig.create(entry)
celery      | 2025-06-19 10:13:40.633 |                  ^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:40.633 |   File "/usr/local/lib/python3.11/site-packages/django/apps/config.py", line 193, in create
celery      | 2025-06-19 10:13:40.633 |     import_module(entry)
celery      | 2025-06-19 10:13:40.633 |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
celery      | 2025-06-19 10:13:40.633 |     return _bootstrap._gcd_import(name[level:], package, level)
celery      | 2025-06-19 10:13:40.633 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:40.633 |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
celery      | 2025-06-19 10:13:40.633 |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
celery      | 2025-06-19 10:13:40.633 |   File "<frozen importlib._bootstrap>", line 1140, in _find_and_load_unlocked
celery      | 2025-06-19 10:13:40.633 | ModuleNotFoundError: No module named 'admin_interface'
backup      | 2025-06-19 10:13:40.662 | wait-for-it.sh: waiting 120 seconds for db:3306
backup      | 2025-06-19 10:13:40.665 | wait-for-it.sh: db:3306 is available after 0 seconds
backup      | 2025-06-19 10:13:40.669 | mysqldump: [Warning] Using a password on the command line interface can be insecure.
web         | 2025-06-19 10:13:40.689 | wait-for-it.sh: waiting 120 seconds for db:3306
web         | 2025-06-19 10:13:40.693 | wait-for-it.sh: db:3306 is available after 0 seconds
celery-beat | 2025-06-19 10:13:40.924 | wait-for-it.sh: waiting 120 seconds for db:3306
celery-beat | 2025-06-19 10:13:40.929 | wait-for-it.sh: db:3306 is available after 0 seconds
nginx       | 2025-06-19 10:13:40.972 | /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
nginx       | 2025-06-19 10:13:40.972 | /docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
nginx       | 2025-06-19 10:13:40.974 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
nginx       | 2025-06-19 10:13:41.001 | 10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
nginx       | 2025-06-19 10:13:41.011 | 10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
nginx       | 2025-06-19 10:13:41.013 | /docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
nginx       | 2025-06-19 10:13:41.013 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
nginx       | 2025-06-19 10:13:41.021 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
nginx       | 2025-06-19 10:13:41.023 | /docker-entrypoint.sh: Configuration complete; ready for start up
celery      | 2025-06-19 10:13:41.103 | wait-for-it.sh: waiting 120 seconds for db:3306
celery      | 2025-06-19 10:13:41.111 | wait-for-it.sh: db:3306 is available after 0 seconds
web         | 2025-06-19 10:13:41.267 | Traceback (most recent call last):
web         | 2025-06-19 10:13:41.267 |   File "/app/manage.py", line 18, in <module>
web         | 2025-06-19 10:13:41.268 |     main()
web         | 2025-06-19 10:13:41.268 |   File "/app/manage.py", line 15, in main
web         | 2025-06-19 10:13:41.268 |     execute_from_command_line(sys.argv)
web         | 2025-06-19 10:13:41.268 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
web         | 2025-06-19 10:13:41.268 |     utility.execute()
web         | 2025-06-19 10:13:41.269 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 416, in execute
web         | 2025-06-19 10:13:41.269 |     django.setup()
web         | 2025-06-19 10:13:41.269 |   File "/usr/local/lib/python3.11/site-packages/django/__init__.py", line 24, in setup
web         | 2025-06-19 10:13:41.269 |     apps.populate(settings.INSTALLED_APPS)
web         | 2025-06-19 10:13:41.269 |   File "/usr/local/lib/python3.11/site-packages/django/apps/registry.py", line 91, in populate
web         | 2025-06-19 10:13:41.269 |     app_config = AppConfig.create(entry)
web         | 2025-06-19 10:13:41.269 |                  ^^^^^^^^^^^^^^^^^^^^^^^
web         | 2025-06-19 10:13:41.269 |   File "/usr/local/lib/python3.11/site-packages/django/apps/config.py", line 193, in create
web         | 2025-06-19 10:13:41.269 |     import_module(entry)
web         | 2025-06-19 10:13:41.270 |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
web         | 2025-06-19 10:13:41.270 |     return _bootstrap._gcd_import(name[level:], package, level)
web         | 2025-06-19 10:13:41.270 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
web         | 2025-06-19 10:13:41.270 |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
web         | 2025-06-19 10:13:41.270 |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
web         | 2025-06-19 10:13:41.270 |   File "<frozen importlib._bootstrap>", line 1140, in _find_and_load_unlocked
web         | 2025-06-19 10:13:41.270 | ModuleNotFoundError: No module named 'admin_interface'
backup      | 2025-06-19 10:13:41.392 | Limpiando backups antiguos...
backup      | 2025-06-19 10:13:41.438 | Limpieza completada. Se mantienen los 480 backups más recientes.
celery-beat | 2025-06-19 10:13:41.440 | Traceback (most recent call last):
celery-beat | 2025-06-19 10:13:41.440 |   File "/app/manage.py", line 18, in <module>
celery-beat | 2025-06-19 10:13:41.440 |     main()
celery-beat | 2025-06-19 10:13:41.440 |   File "/app/manage.py", line 15, in main
celery-beat | 2025-06-19 10:13:41.440 |     execute_from_command_line(sys.argv)
celery-beat | 2025-06-19 10:13:41.440 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
celery-beat | 2025-06-19 10:13:41.440 |     utility.execute()
celery-beat | 2025-06-19 10:13:41.440 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 416, in execute
celery-beat | 2025-06-19 10:13:41.440 |     django.setup()
celery-beat | 2025-06-19 10:13:41.440 |   File "/usr/local/lib/python3.11/site-packages/django/__init__.py", line 24, in setup
celery-beat | 2025-06-19 10:13:41.440 |     apps.populate(settings.INSTALLED_APPS)
celery-beat | 2025-06-19 10:13:41.440 |   File "/usr/local/lib/python3.11/site-packages/django/apps/registry.py", line 91, in populate
celery-beat | 2025-06-19 10:13:41.440 |     app_config = AppConfig.create(entry)
celery-beat | 2025-06-19 10:13:41.440 |                  ^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-06-19 10:13:41.440 |   File "/usr/local/lib/python3.11/site-packages/django/apps/config.py", line 193, in create
celery-beat | 2025-06-19 10:13:41.440 |     import_module(entry)
celery-beat | 2025-06-19 10:13:41.440 |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
celery-beat | 2025-06-19 10:13:41.440 |     return _bootstrap._gcd_import(name[level:], package, level)
celery-beat | 2025-06-19 10:13:41.440 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-06-19 10:13:41.440 |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
celery-beat | 2025-06-19 10:13:41.440 |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
celery-beat | 2025-06-19 10:13:41.441 |   File "<frozen importlib._bootstrap>", line 1140, in _find_and_load_unlocked
celery-beat | 2025-06-19 10:13:41.441 | ModuleNotFoundError: No module named 'admin_interface'
celery      | 2025-06-19 10:13:41.581 | Traceback (most recent call last):
celery      | 2025-06-19 10:13:41.581 |   File "/usr/local/bin/celery", line 8, in <module>
celery      | 2025-06-19 10:13:41.582 |     sys.exit(main())
celery      | 2025-06-19 10:13:41.582 |              ^^^^^^
celery      | 2025-06-19 10:13:41.582 |   File "/usr/local/lib/python3.11/site-packages/celery/__main__.py", line 15, in main
celery      | 2025-06-19 10:13:41.582 |     sys.exit(_main())
celery      | 2025-06-19 10:13:41.582 |              ^^^^^^^
celery      | 2025-06-19 10:13:41.582 |   File "/usr/local/lib/python3.11/site-packages/celery/bin/celery.py", line 236, in main
celery      | 2025-06-19 10:13:41.582 |     return celery(auto_envvar_prefix="CELERY")
celery      | 2025-06-19 10:13:41.582 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:41.582 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1157, in __call__
celery      | 2025-06-19 10:13:41.582 |     return self.main(*args, **kwargs)
celery      | 2025-06-19 10:13:41.582 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:41.582 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1078, in main
celery      | 2025-06-19 10:13:41.582 |     rv = self.invoke(ctx)
celery      | 2025-06-19 10:13:41.582 |          ^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:41.582 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1688, in invoke
celery      | 2025-06-19 10:13:41.582 |     return _process_result(sub_ctx.command.invoke(sub_ctx))
celery      | 2025-06-19 10:13:41.582 |                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:41.582 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1434, in invoke
celery      | 2025-06-19 10:13:41.582 |     return ctx.invoke(self.callback, **ctx.params)
celery      | 2025-06-19 10:13:41.582 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:41.582 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 783, in invoke
celery      | 2025-06-19 10:13:41.582 |     return __callback(*args, **kwargs)
celery      | 2025-06-19 10:13:41.582 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:41.582 |   File "/usr/local/lib/python3.11/site-packages/click/decorators.py", line 33, in new_func
celery      | 2025-06-19 10:13:41.582 |     return f(get_current_context(), *args, **kwargs)
celery      | 2025-06-19 10:13:41.583 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:41.583 |   File "/usr/local/lib/python3.11/site-packages/celery/bin/base.py", line 135, in caller
celery      | 2025-06-19 10:13:41.583 |     return f(ctx, *args, **kwargs)
celery      | 2025-06-19 10:13:41.583 |            ^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:41.583 |   File "/usr/local/lib/python3.11/site-packages/celery/bin/worker.py", line 348, in worker
celery      | 2025-06-19 10:13:41.583 |     worker = app.Worker(
celery      | 2025-06-19 10:13:41.583 |              ^^^^^^^^^^^
celery      | 2025-06-19 10:13:41.583 |   File "/usr/local/lib/python3.11/site-packages/celery/worker/worker.py", line 93, in __init__
celery      | 2025-06-19 10:13:41.583 |     self.app.loader.init_worker()
celery      | 2025-06-19 10:13:41.583 |   File "/usr/local/lib/python3.11/site-packages/celery/loaders/base.py", line 110, in init_worker
celery      | 2025-06-19 10:13:41.583 |     self.import_default_modules()
celery      | 2025-06-19 10:13:41.583 |   File "/usr/local/lib/python3.11/site-packages/celery/loaders/base.py", line 104, in import_default_modules
celery      | 2025-06-19 10:13:41.583 |     raise response
celery      | 2025-06-19 10:13:41.583 |   File "/usr/local/lib/python3.11/site-packages/celery/utils/dispatch/signal.py", line 276, in send
celery      | 2025-06-19 10:13:41.583 |     response = receiver(signal=self, sender=sender, **named)
celery      | 2025-06-19 10:13:41.583 |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:41.583 |   File "/usr/local/lib/python3.11/site-packages/celery/fixups/django.py", line 100, in on_import_modules
celery      | 2025-06-19 10:13:41.583 |     self.worker_fixup.validate_models()
celery      | 2025-06-19 10:13:41.583 |   File "/usr/local/lib/python3.11/site-packages/celery/fixups/django.py", line 138, in validate_models
celery      | 2025-06-19 10:13:41.583 |     self.django_setup()
celery      | 2025-06-19 10:13:41.583 |   File "/usr/local/lib/python3.11/site-packages/celery/fixups/django.py", line 134, in django_setup
celery      | 2025-06-19 10:13:41.583 |     django.setup()
celery      | 2025-06-19 10:13:41.583 |   File "/usr/local/lib/python3.11/site-packages/django/__init__.py", line 24, in setup
celery      | 2025-06-19 10:13:41.583 |     apps.populate(settings.INSTALLED_APPS)
celery      | 2025-06-19 10:13:41.583 |   File "/usr/local/lib/python3.11/site-packages/django/apps/registry.py", line 91, in populate
celery      | 2025-06-19 10:13:41.583 |     app_config = AppConfig.create(entry)
celery      | 2025-06-19 10:13:41.583 |                  ^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:41.583 |   File "/usr/local/lib/python3.11/site-packages/django/apps/config.py", line 193, in create
celery      | 2025-06-19 10:13:41.583 |     import_module(entry)
celery      | 2025-06-19 10:13:41.583 |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
celery      | 2025-06-19 10:13:41.583 |     return _bootstrap._gcd_import(name[level:], package, level)
celery      | 2025-06-19 10:13:41.583 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:41.583 |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
celery      | 2025-06-19 10:13:41.584 |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
celery      | 2025-06-19 10:13:41.584 |   File "<frozen importlib._bootstrap>", line 1140, in _find_and_load_unlocked
celery      | 2025-06-19 10:13:41.584 | ModuleNotFoundError: No module named 'admin_interface'
web         | 2025-06-19 10:13:41.671 | wait-for-it.sh: waiting 120 seconds for db:3306
web         | 2025-06-19 10:13:41.676 | wait-for-it.sh: db:3306 is available after 0 seconds
celery-beat | 2025-06-19 10:13:41.884 | wait-for-it.sh: waiting 120 seconds for db:3306
celery-beat | 2025-06-19 10:13:41.888 | wait-for-it.sh: db:3306 is available after 0 seconds
web         | 2025-06-19 10:13:41.958 | Traceback (most recent call last):
web         | 2025-06-19 10:13:41.958 |   File "/app/manage.py", line 18, in <module>
web         | 2025-06-19 10:13:41.958 |     main()
web         | 2025-06-19 10:13:41.958 |   File "/app/manage.py", line 15, in main
web         | 2025-06-19 10:13:41.958 |     execute_from_command_line(sys.argv)
web         | 2025-06-19 10:13:41.958 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
web         | 2025-06-19 10:13:41.959 |     utility.execute()
web         | 2025-06-19 10:13:41.959 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 416, in execute
web         | 2025-06-19 10:13:41.959 |     django.setup()
web         | 2025-06-19 10:13:41.959 |   File "/usr/local/lib/python3.11/site-packages/django/__init__.py", line 24, in setup
web         | 2025-06-19 10:13:41.959 |     apps.populate(settings.INSTALLED_APPS)
web         | 2025-06-19 10:13:41.959 |   File "/usr/local/lib/python3.11/site-packages/django/apps/registry.py", line 91, in populate
web         | 2025-06-19 10:13:41.959 |     app_config = AppConfig.create(entry)
web         | 2025-06-19 10:13:41.959 |                  ^^^^^^^^^^^^^^^^^^^^^^^
web         | 2025-06-19 10:13:41.959 |   File "/usr/local/lib/python3.11/site-packages/django/apps/config.py", line 193, in create
web         | 2025-06-19 10:13:41.959 |     import_module(entry)
web         | 2025-06-19 10:13:41.959 |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
web         | 2025-06-19 10:13:41.959 |     return _bootstrap._gcd_import(name[level:], package, level)
web         | 2025-06-19 10:13:41.959 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
web         | 2025-06-19 10:13:41.959 |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
web         | 2025-06-19 10:13:41.959 |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
web         | 2025-06-19 10:13:41.959 |   File "<frozen importlib._bootstrap>", line 1140, in _find_and_load_unlocked
web         | 2025-06-19 10:13:41.959 | ModuleNotFoundError: No module named 'admin_interface'
celery      | 2025-06-19 10:13:42.088 | wait-for-it.sh: waiting 120 seconds for db:3306
celery      | 2025-06-19 10:13:42.094 | wait-for-it.sh: db:3306 is available after 0 seconds
celery-beat | 2025-06-19 10:13:42.202 | Traceback (most recent call last):
celery-beat | 2025-06-19 10:13:42.202 |   File "/app/manage.py", line 18, in <module>
celery-beat | 2025-06-19 10:13:42.202 |     main()
celery-beat | 2025-06-19 10:13:42.202 |   File "/app/manage.py", line 15, in main
celery-beat | 2025-06-19 10:13:42.202 |     execute_from_command_line(sys.argv)
celery-beat | 2025-06-19 10:13:42.203 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
celery-beat | 2025-06-19 10:13:42.203 |     utility.execute()
celery-beat | 2025-06-19 10:13:42.203 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 416, in execute
celery-beat | 2025-06-19 10:13:42.203 |     django.setup()
celery-beat | 2025-06-19 10:13:42.203 |   File "/usr/local/lib/python3.11/site-packages/django/__init__.py", line 24, in setup
celery-beat | 2025-06-19 10:13:42.203 |     apps.populate(settings.INSTALLED_APPS)
celery-beat | 2025-06-19 10:13:42.203 |   File "/usr/local/lib/python3.11/site-packages/django/apps/registry.py", line 91, in populate
celery-beat | 2025-06-19 10:13:42.203 |     app_config = AppConfig.create(entry)
celery-beat | 2025-06-19 10:13:42.203 |                  ^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-06-19 10:13:42.203 |   File "/usr/local/lib/python3.11/site-packages/django/apps/config.py", line 193, in create
celery-beat | 2025-06-19 10:13:42.203 |     import_module(entry)
celery-beat | 2025-06-19 10:13:42.203 |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
celery-beat | 2025-06-19 10:13:42.203 |     return _bootstrap._gcd_import(name[level:], package, level)
celery-beat | 2025-06-19 10:13:42.203 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-06-19 10:13:42.203 |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
celery-beat | 2025-06-19 10:13:42.203 |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
celery-beat | 2025-06-19 10:13:42.203 |   File "<frozen importlib._bootstrap>", line 1140, in _find_and_load_unlocked
celery-beat | 2025-06-19 10:13:42.203 | ModuleNotFoundError: No module named 'admin_interface'
web         | 2025-06-19 10:13:42.439 | wait-for-it.sh: waiting 120 seconds for db:3306
web         | 2025-06-19 10:13:42.443 | wait-for-it.sh: db:3306 is available after 0 seconds
celery      | 2025-06-19 10:13:42.499 | Traceback (most recent call last):
celery      | 2025-06-19 10:13:42.499 |   File "/usr/local/bin/celery", line 8, in <module>
celery      | 2025-06-19 10:13:42.499 |     sys.exit(main())
celery      | 2025-06-19 10:13:42.499 |              ^^^^^^
celery      | 2025-06-19 10:13:42.499 |   File "/usr/local/lib/python3.11/site-packages/celery/__main__.py", line 15, in main
celery      | 2025-06-19 10:13:42.499 |     sys.exit(_main())
celery      | 2025-06-19 10:13:42.499 |              ^^^^^^^
celery      | 2025-06-19 10:13:42.499 |   File "/usr/local/lib/python3.11/site-packages/celery/bin/celery.py", line 236, in main
celery      | 2025-06-19 10:13:42.499 |     return celery(auto_envvar_prefix="CELERY")
celery      | 2025-06-19 10:13:42.499 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:42.499 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1157, in __call__
celery      | 2025-06-19 10:13:42.499 |     return self.main(*args, **kwargs)
celery      | 2025-06-19 10:13:42.499 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:42.499 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1078, in main
celery      | 2025-06-19 10:13:42.499 |     rv = self.invoke(ctx)
celery      | 2025-06-19 10:13:42.499 |          ^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:42.499 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1688, in invoke
celery      | 2025-06-19 10:13:42.499 |     return _process_result(sub_ctx.command.invoke(sub_ctx))
celery      | 2025-06-19 10:13:42.499 |                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:42.499 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1434, in invoke
celery      | 2025-06-19 10:13:42.499 |     return ctx.invoke(self.callback, **ctx.params)
celery      | 2025-06-19 10:13:42.499 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:42.499 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 783, in invoke
celery      | 2025-06-19 10:13:42.499 |     return __callback(*args, **kwargs)
celery      | 2025-06-19 10:13:42.499 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:42.499 |   File "/usr/local/lib/python3.11/site-packages/click/decorators.py", line 33, in new_func
celery      | 2025-06-19 10:13:42.499 |     return f(get_current_context(), *args, **kwargs)
celery      | 2025-06-19 10:13:42.499 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:42.499 |   File "/usr/local/lib/python3.11/site-packages/celery/bin/base.py", line 135, in caller
celery      | 2025-06-19 10:13:42.499 |     return f(ctx, *args, **kwargs)
celery      | 2025-06-19 10:13:42.499 |            ^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:42.499 |   File "/usr/local/lib/python3.11/site-packages/celery/bin/worker.py", line 348, in worker
celery      | 2025-06-19 10:13:42.499 |     worker = app.Worker(
celery      | 2025-06-19 10:13:42.499 |              ^^^^^^^^^^^
celery      | 2025-06-19 10:13:42.499 |   File "/usr/local/lib/python3.11/site-packages/celery/worker/worker.py", line 93, in __init__
celery      | 2025-06-19 10:13:42.499 |     self.app.loader.init_worker()
celery      | 2025-06-19 10:13:42.499 |   File "/usr/local/lib/python3.11/site-packages/celery/loaders/base.py", line 110, in init_worker
celery      | 2025-06-19 10:13:42.499 |     self.import_default_modules()
celery      | 2025-06-19 10:13:42.499 |   File "/usr/local/lib/python3.11/site-packages/celery/loaders/base.py", line 104, in import_default_modules
celery      | 2025-06-19 10:13:42.499 |     raise response
celery      | 2025-06-19 10:13:42.499 |   File "/usr/local/lib/python3.11/site-packages/celery/utils/dispatch/signal.py", line 276, in send
celery      | 2025-06-19 10:13:42.499 |     response = receiver(signal=self, sender=sender, **named)
celery      | 2025-06-19 10:13:42.499 |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:42.499 |   File "/usr/local/lib/python3.11/site-packages/celery/fixups/django.py", line 100, in on_import_modules
celery      | 2025-06-19 10:13:42.499 |     self.worker_fixup.validate_models()
celery      | 2025-06-19 10:13:42.499 |   File "/usr/local/lib/python3.11/site-packages/celery/fixups/django.py", line 138, in validate_models
celery      | 2025-06-19 10:13:42.499 |     self.django_setup()
celery      | 2025-06-19 10:13:42.499 |   File "/usr/local/lib/python3.11/site-packages/celery/fixups/django.py", line 134, in django_setup
celery      | 2025-06-19 10:13:42.499 |     django.setup()
celery      | 2025-06-19 10:13:42.499 |   File "/usr/local/lib/python3.11/site-packages/django/__init__.py", line 24, in setup
celery      | 2025-06-19 10:13:42.499 |     apps.populate(settings.INSTALLED_APPS)
celery      | 2025-06-19 10:13:42.499 |   File "/usr/local/lib/python3.11/site-packages/django/apps/registry.py", line 91, in populate
celery      | 2025-06-19 10:13:42.499 |     app_config = AppConfig.create(entry)
celery      | 2025-06-19 10:13:42.499 |                  ^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:42.499 |   File "/usr/local/lib/python3.11/site-packages/django/apps/config.py", line 193, in create
celery      | 2025-06-19 10:13:42.500 |     import_module(entry)
celery      | 2025-06-19 10:13:42.500 |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
celery      | 2025-06-19 10:13:42.500 |     return _bootstrap._gcd_import(name[level:], package, level)
celery      | 2025-06-19 10:13:42.500 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:42.500 |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
celery      | 2025-06-19 10:13:42.500 |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
celery      | 2025-06-19 10:13:42.500 |   File "<frozen importlib._bootstrap>", line 1140, in _find_and_load_unlocked
celery      | 2025-06-19 10:13:42.500 | ModuleNotFoundError: No module named 'admin_interface'
web         | 2025-06-19 10:13:42.733 | Traceback (most recent call last):
web         | 2025-06-19 10:13:42.733 |   File "/app/manage.py", line 18, in <module>
web         | 2025-06-19 10:13:42.734 |     main()
web         | 2025-06-19 10:13:42.734 |   File "/app/manage.py", line 15, in main
web         | 2025-06-19 10:13:42.734 |     execute_from_command_line(sys.argv)
web         | 2025-06-19 10:13:42.734 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
web         | 2025-06-19 10:13:42.734 |     utility.execute()
web         | 2025-06-19 10:13:42.734 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 416, in execute
web         | 2025-06-19 10:13:42.735 |     django.setup()
web         | 2025-06-19 10:13:42.735 |   File "/usr/local/lib/python3.11/site-packages/django/__init__.py", line 24, in setup
web         | 2025-06-19 10:13:42.735 |     apps.populate(settings.INSTALLED_APPS)
web         | 2025-06-19 10:13:42.735 |   File "/usr/local/lib/python3.11/site-packages/django/apps/registry.py", line 91, in populate
web         | 2025-06-19 10:13:42.735 |     app_config = AppConfig.create(entry)
web         | 2025-06-19 10:13:42.735 |                  ^^^^^^^^^^^^^^^^^^^^^^^
web         | 2025-06-19 10:13:42.735 |   File "/usr/local/lib/python3.11/site-packages/django/apps/config.py", line 193, in create
web         | 2025-06-19 10:13:42.735 |     import_module(entry)
web         | 2025-06-19 10:13:42.735 |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
web         | 2025-06-19 10:13:42.735 |     return _bootstrap._gcd_import(name[level:], package, level)
web         | 2025-06-19 10:13:42.735 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
web         | 2025-06-19 10:13:42.735 |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
web         | 2025-06-19 10:13:42.735 |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
web         | 2025-06-19 10:13:42.735 |   File "<frozen importlib._bootstrap>", line 1140, in _find_and_load_unlocked
web         | 2025-06-19 10:13:42.735 | ModuleNotFoundError: No module named 'admin_interface'
celery-beat | 2025-06-19 10:13:42.825 | wait-for-it.sh: waiting 120 seconds for db:3306
celery-beat | 2025-06-19 10:13:42.828 | wait-for-it.sh: db:3306 is available after 0 seconds
celery-beat | 2025-06-19 10:13:43.094 | Traceback (most recent call last):
celery-beat | 2025-06-19 10:13:43.094 |   File "/app/manage.py", line 18, in <module>
celery-beat | 2025-06-19 10:13:43.094 |     main()
celery-beat | 2025-06-19 10:13:43.094 |   File "/app/manage.py", line 15, in main
celery-beat | 2025-06-19 10:13:43.094 |     execute_from_command_line(sys.argv)
celery-beat | 2025-06-19 10:13:43.094 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
celery-beat | 2025-06-19 10:13:43.094 |     utility.execute()
celery-beat | 2025-06-19 10:13:43.094 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 416, in execute
celery-beat | 2025-06-19 10:13:43.094 |     django.setup()
celery-beat | 2025-06-19 10:13:43.094 |   File "/usr/local/lib/python3.11/site-packages/django/__init__.py", line 24, in setup
celery-beat | 2025-06-19 10:13:43.094 |     apps.populate(settings.INSTALLED_APPS)
celery-beat | 2025-06-19 10:13:43.094 |   File "/usr/local/lib/python3.11/site-packages/django/apps/registry.py", line 91, in populate
celery-beat | 2025-06-19 10:13:43.094 |     app_config = AppConfig.create(entry)
celery-beat | 2025-06-19 10:13:43.094 |                  ^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-06-19 10:13:43.095 |   File "/usr/local/lib/python3.11/site-packages/django/apps/config.py", line 193, in create
celery-beat | 2025-06-19 10:13:43.095 |     import_module(entry)
celery-beat | 2025-06-19 10:13:43.095 |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
celery-beat | 2025-06-19 10:13:43.095 |     return _bootstrap._gcd_import(name[level:], package, level)
celery-beat | 2025-06-19 10:13:43.095 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-06-19 10:13:43.095 |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
celery-beat | 2025-06-19 10:13:43.095 |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
celery-beat | 2025-06-19 10:13:43.095 |   File "<frozen importlib._bootstrap>", line 1140, in _find_and_load_unlocked
celery-beat | 2025-06-19 10:13:43.095 | ModuleNotFoundError: No module named 'admin_interface'
celery      | 2025-06-19 10:13:43.165 | wait-for-it.sh: waiting 120 seconds for db:3306
celery      | 2025-06-19 10:13:43.167 | wait-for-it.sh: db:3306 is available after 0 seconds
web         | 2025-06-19 10:13:43.401 | wait-for-it.sh: waiting 120 seconds for db:3306
web         | 2025-06-19 10:13:43.406 | wait-for-it.sh: db:3306 is available after 0 seconds
celery      | 2025-06-19 10:13:43.481 | Traceback (most recent call last):
celery      | 2025-06-19 10:13:43.481 |   File "/usr/local/bin/celery", line 8, in <module>
celery      | 2025-06-19 10:13:43.481 |     sys.exit(main())
celery      | 2025-06-19 10:13:43.481 |              ^^^^^^
celery      | 2025-06-19 10:13:43.481 |   File "/usr/local/lib/python3.11/site-packages/celery/__main__.py", line 15, in main
celery      | 2025-06-19 10:13:43.481 |     sys.exit(_main())
celery      | 2025-06-19 10:13:43.481 |              ^^^^^^^
celery      | 2025-06-19 10:13:43.481 |   File "/usr/local/lib/python3.11/site-packages/celery/bin/celery.py", line 236, in main
celery      | 2025-06-19 10:13:43.481 |     return celery(auto_envvar_prefix="CELERY")
celery      | 2025-06-19 10:13:43.481 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:43.481 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1157, in __call__
celery      | 2025-06-19 10:13:43.481 |     return self.main(*args, **kwargs)
celery      | 2025-06-19 10:13:43.481 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:43.481 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1078, in main
celery      | 2025-06-19 10:13:43.481 |     rv = self.invoke(ctx)
celery      | 2025-06-19 10:13:43.481 |          ^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:43.481 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1688, in invoke
celery      | 2025-06-19 10:13:43.482 |     return _process_result(sub_ctx.command.invoke(sub_ctx))
celery      | 2025-06-19 10:13:43.482 |                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:43.482 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1434, in invoke
celery      | 2025-06-19 10:13:43.482 |     return ctx.invoke(self.callback, **ctx.params)
celery      | 2025-06-19 10:13:43.482 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:43.482 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 783, in invoke
celery      | 2025-06-19 10:13:43.482 |     return __callback(*args, **kwargs)
celery      | 2025-06-19 10:13:43.482 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:43.482 |   File "/usr/local/lib/python3.11/site-packages/click/decorators.py", line 33, in new_func
celery      | 2025-06-19 10:13:43.482 |     return f(get_current_context(), *args, **kwargs)
celery      | 2025-06-19 10:13:43.482 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:43.482 |   File "/usr/local/lib/python3.11/site-packages/celery/bin/base.py", line 135, in caller
celery      | 2025-06-19 10:13:43.482 |     return f(ctx, *args, **kwargs)
celery      | 2025-06-19 10:13:43.482 |            ^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:43.482 |   File "/usr/local/lib/python3.11/site-packages/celery/bin/worker.py", line 348, in worker
celery      | 2025-06-19 10:13:43.482 |     worker = app.Worker(
celery      | 2025-06-19 10:13:43.482 |              ^^^^^^^^^^^
celery      | 2025-06-19 10:13:43.482 |   File "/usr/local/lib/python3.11/site-packages/celery/worker/worker.py", line 93, in __init__
celery      | 2025-06-19 10:13:43.482 |     self.app.loader.init_worker()
celery      | 2025-06-19 10:13:43.482 |   File "/usr/local/lib/python3.11/site-packages/celery/loaders/base.py", line 110, in init_worker
celery      | 2025-06-19 10:13:43.482 |     self.import_default_modules()
celery      | 2025-06-19 10:13:43.482 |   File "/usr/local/lib/python3.11/site-packages/celery/loaders/base.py", line 104, in import_default_modules
celery      | 2025-06-19 10:13:43.482 |     raise response
celery      | 2025-06-19 10:13:43.483 |   File "/usr/local/lib/python3.11/site-packages/celery/utils/dispatch/signal.py", line 276, in send
celery      | 2025-06-19 10:13:43.483 |     response = receiver(signal=self, sender=sender, **named)
celery      | 2025-06-19 10:13:43.483 |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:43.483 |   File "/usr/local/lib/python3.11/site-packages/celery/fixups/django.py", line 100, in on_import_modules
celery      | 2025-06-19 10:13:43.483 |     self.worker_fixup.validate_models()
celery      | 2025-06-19 10:13:43.483 |   File "/usr/local/lib/python3.11/site-packages/celery/fixups/django.py", line 138, in validate_models
celery      | 2025-06-19 10:13:43.483 |     self.django_setup()
celery      | 2025-06-19 10:13:43.483 |   File "/usr/local/lib/python3.11/site-packages/celery/fixups/django.py", line 134, in django_setup
celery      | 2025-06-19 10:13:43.483 |     django.setup()
celery      | 2025-06-19 10:13:43.483 |   File "/usr/local/lib/python3.11/site-packages/django/__init__.py", line 24, in setup
celery      | 2025-06-19 10:13:43.483 |     apps.populate(settings.INSTALLED_APPS)
celery      | 2025-06-19 10:13:43.483 |   File "/usr/local/lib/python3.11/site-packages/django/apps/registry.py", line 91, in populate
celery      | 2025-06-19 10:13:43.483 |     app_config = AppConfig.create(entry)
celery      | 2025-06-19 10:13:43.483 |                  ^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:43.483 |   File "/usr/local/lib/python3.11/site-packages/django/apps/config.py", line 193, in create
celery      | 2025-06-19 10:13:43.483 |     import_module(entry)
celery      | 2025-06-19 10:13:43.483 |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
celery      | 2025-06-19 10:13:43.483 |     return _bootstrap._gcd_import(name[level:], package, level)
celery      | 2025-06-19 10:13:43.483 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:43.483 |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
celery      | 2025-06-19 10:13:43.483 |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
celery      | 2025-06-19 10:13:43.483 |   File "<frozen importlib._bootstrap>", line 1140, in _find_and_load_unlocked
celery      | 2025-06-19 10:13:43.483 | ModuleNotFoundError: No module named 'admin_interface'
web         | 2025-06-19 10:13:43.637 | Traceback (most recent call last):
web         | 2025-06-19 10:13:43.637 |   File "/app/manage.py", line 18, in <module>
web         | 2025-06-19 10:13:43.637 |     main()
web         | 2025-06-19 10:13:43.638 |   File "/app/manage.py", line 15, in main
web         | 2025-06-19 10:13:43.638 |     execute_from_command_line(sys.argv)
web         | 2025-06-19 10:13:43.638 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
web         | 2025-06-19 10:13:43.638 |     utility.execute()
web         | 2025-06-19 10:13:43.638 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 416, in execute
web         | 2025-06-19 10:13:43.638 |     django.setup()
web         | 2025-06-19 10:13:43.638 |   File "/usr/local/lib/python3.11/site-packages/django/__init__.py", line 24, in setup
web         | 2025-06-19 10:13:43.638 |     apps.populate(settings.INSTALLED_APPS)
web         | 2025-06-19 10:13:43.638 |   File "/usr/local/lib/python3.11/site-packages/django/apps/registry.py", line 91, in populate
web         | 2025-06-19 10:13:43.638 |     app_config = AppConfig.create(entry)
web         | 2025-06-19 10:13:43.638 |                  ^^^^^^^^^^^^^^^^^^^^^^^
web         | 2025-06-19 10:13:43.638 |   File "/usr/local/lib/python3.11/site-packages/django/apps/config.py", line 193, in create
web         | 2025-06-19 10:13:43.638 |     import_module(entry)
web         | 2025-06-19 10:13:43.638 |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
web         | 2025-06-19 10:13:43.638 |     return _bootstrap._gcd_import(name[level:], package, level)
web         | 2025-06-19 10:13:43.638 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
web         | 2025-06-19 10:13:43.638 |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
web         | 2025-06-19 10:13:43.638 |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
web         | 2025-06-19 10:13:43.638 |   File "<frozen importlib._bootstrap>", line 1140, in _find_and_load_unlocked
web         | 2025-06-19 10:13:43.638 | ModuleNotFoundError: No module named 'admin_interface'
celery-beat | 2025-06-19 10:13:44.070 | wait-for-it.sh: waiting 120 seconds for db:3306
celery-beat | 2025-06-19 10:13:44.072 | wait-for-it.sh: db:3306 is available after 0 seconds
celery-beat | 2025-06-19 10:13:44.270 | Traceback (most recent call last):
celery-beat | 2025-06-19 10:13:44.270 |   File "/app/manage.py", line 18, in <module>
celery-beat | 2025-06-19 10:13:44.270 |     main()
celery-beat | 2025-06-19 10:13:44.270 |   File "/app/manage.py", line 15, in main
celery-beat | 2025-06-19 10:13:44.270 |     execute_from_command_line(sys.argv)
celery-beat | 2025-06-19 10:13:44.270 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
celery-beat | 2025-06-19 10:13:44.270 |     utility.execute()
celery-beat | 2025-06-19 10:13:44.270 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 416, in execute
celery-beat | 2025-06-19 10:13:44.270 |     django.setup()
celery-beat | 2025-06-19 10:13:44.270 |   File "/usr/local/lib/python3.11/site-packages/django/__init__.py", line 24, in setup
celery-beat | 2025-06-19 10:13:44.270 |     apps.populate(settings.INSTALLED_APPS)
celery-beat | 2025-06-19 10:13:44.270 |   File "/usr/local/lib/python3.11/site-packages/django/apps/registry.py", line 91, in populate
celery-beat | 2025-06-19 10:13:44.270 |     app_config = AppConfig.create(entry)
celery-beat | 2025-06-19 10:13:44.270 |                  ^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-06-19 10:13:44.270 |   File "/usr/local/lib/python3.11/site-packages/django/apps/config.py", line 193, in create
celery-beat | 2025-06-19 10:13:44.270 |     import_module(entry)
celery-beat | 2025-06-19 10:13:44.270 |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
celery-beat | 2025-06-19 10:13:44.270 |     return _bootstrap._gcd_import(name[level:], package, level)
celery-beat | 2025-06-19 10:13:44.270 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-06-19 10:13:44.270 |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
celery-beat | 2025-06-19 10:13:44.270 |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
celery-beat | 2025-06-19 10:13:44.270 |   File "<frozen importlib._bootstrap>", line 1140, in _find_and_load_unlocked
celery-beat | 2025-06-19 10:13:44.270 | ModuleNotFoundError: No module named 'admin_interface'
celery      | 2025-06-19 10:13:44.502 | wait-for-it.sh: waiting 120 seconds for db:3306
celery      | 2025-06-19 10:13:44.504 | wait-for-it.sh: db:3306 is available after 0 seconds
web         | 2025-06-19 10:13:44.652 | wait-for-it.sh: waiting 120 seconds for db:3306
web         | 2025-06-19 10:13:44.655 | wait-for-it.sh: db:3306 is available after 0 seconds
celery      | 2025-06-19 10:13:44.821 | Traceback (most recent call last):
celery      | 2025-06-19 10:13:44.821 |   File "/usr/local/bin/celery", line 8, in <module>
celery      | 2025-06-19 10:13:44.821 |     sys.exit(main())
celery      | 2025-06-19 10:13:44.821 |              ^^^^^^
celery      | 2025-06-19 10:13:44.821 |   File "/usr/local/lib/python3.11/site-packages/celery/__main__.py", line 15, in main
celery      | 2025-06-19 10:13:44.821 |     sys.exit(_main())
celery      | 2025-06-19 10:13:44.822 |              ^^^^^^^
celery      | 2025-06-19 10:13:44.822 |   File "/usr/local/lib/python3.11/site-packages/celery/bin/celery.py", line 236, in main
celery      | 2025-06-19 10:13:44.822 |     return celery(auto_envvar_prefix="CELERY")
celery      | 2025-06-19 10:13:44.822 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:44.822 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1157, in __call__
celery      | 2025-06-19 10:13:44.822 |     return self.main(*args, **kwargs)
celery      | 2025-06-19 10:13:44.822 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:44.822 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1078, in main
celery      | 2025-06-19 10:13:44.822 |     rv = self.invoke(ctx)
celery      | 2025-06-19 10:13:44.822 |          ^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:44.822 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1688, in invoke
celery      | 2025-06-19 10:13:44.822 |     return _process_result(sub_ctx.command.invoke(sub_ctx))
celery      | 2025-06-19 10:13:44.822 |                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:44.822 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1434, in invoke
celery      | 2025-06-19 10:13:44.822 |     return ctx.invoke(self.callback, **ctx.params)
celery      | 2025-06-19 10:13:44.822 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:44.822 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 783, in invoke
celery      | 2025-06-19 10:13:44.822 |     return __callback(*args, **kwargs)
celery      | 2025-06-19 10:13:44.822 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:44.822 |   File "/usr/local/lib/python3.11/site-packages/click/decorators.py", line 33, in new_func
celery      | 2025-06-19 10:13:44.822 |     return f(get_current_context(), *args, **kwargs)
celery      | 2025-06-19 10:13:44.822 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:44.822 |   File "/usr/local/lib/python3.11/site-packages/celery/bin/base.py", line 135, in caller
celery      | 2025-06-19 10:13:44.822 |     return f(ctx, *args, **kwargs)
celery      | 2025-06-19 10:13:44.822 |            ^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:44.822 |   File "/usr/local/lib/python3.11/site-packages/celery/bin/worker.py", line 348, in worker
celery      | 2025-06-19 10:13:44.822 |     worker = app.Worker(
celery      | 2025-06-19 10:13:44.822 |              ^^^^^^^^^^^
celery      | 2025-06-19 10:13:44.822 |   File "/usr/local/lib/python3.11/site-packages/celery/worker/worker.py", line 93, in __init__
celery      | 2025-06-19 10:13:44.822 |     self.app.loader.init_worker()
celery      | 2025-06-19 10:13:44.822 |   File "/usr/local/lib/python3.11/site-packages/celery/loaders/base.py", line 110, in init_worker
celery      | 2025-06-19 10:13:44.822 |     self.import_default_modules()
celery      | 2025-06-19 10:13:44.822 |   File "/usr/local/lib/python3.11/site-packages/celery/loaders/base.py", line 104, in import_default_modules
celery      | 2025-06-19 10:13:44.822 |     raise response
celery      | 2025-06-19 10:13:44.822 |   File "/usr/local/lib/python3.11/site-packages/celery/utils/dispatch/signal.py", line 276, in send
celery      | 2025-06-19 10:13:44.822 |     response = receiver(signal=self, sender=sender, **named)
celery      | 2025-06-19 10:13:44.822 |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:44.822 |   File "/usr/local/lib/python3.11/site-packages/celery/fixups/django.py", line 100, in on_import_modules
celery      | 2025-06-19 10:13:44.823 |     self.worker_fixup.validate_models()
celery      | 2025-06-19 10:13:44.823 |   File "/usr/local/lib/python3.11/site-packages/celery/fixups/django.py", line 138, in validate_models
celery      | 2025-06-19 10:13:44.823 |     self.django_setup()
celery      | 2025-06-19 10:13:44.823 |   File "/usr/local/lib/python3.11/site-packages/celery/fixups/django.py", line 134, in django_setup
celery      | 2025-06-19 10:13:44.823 |     django.setup()
celery      | 2025-06-19 10:13:44.823 |   File "/usr/local/lib/python3.11/site-packages/django/__init__.py", line 24, in setup
celery      | 2025-06-19 10:13:44.823 |     apps.populate(settings.INSTALLED_APPS)
celery      | 2025-06-19 10:13:44.823 |   File "/usr/local/lib/python3.11/site-packages/django/apps/registry.py", line 91, in populate
celery      | 2025-06-19 10:13:44.823 |     app_config = AppConfig.create(entry)
celery      | 2025-06-19 10:13:44.823 |                  ^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:44.823 |   File "/usr/local/lib/python3.11/site-packages/django/apps/config.py", line 193, in create
celery      | 2025-06-19 10:13:44.823 |     import_module(entry)
celery      | 2025-06-19 10:13:44.823 |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
celery      | 2025-06-19 10:13:44.823 |     return _bootstrap._gcd_import(name[level:], package, level)
celery      | 2025-06-19 10:13:44.823 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:44.823 |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
celery      | 2025-06-19 10:13:44.823 |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
celery      | 2025-06-19 10:13:44.823 |   File "<frozen importlib._bootstrap>", line 1140, in _find_and_load_unlocked
celery      | 2025-06-19 10:13:44.823 | ModuleNotFoundError: No module named 'admin_interface'
web         | 2025-06-19 10:13:44.902 | Traceback (most recent call last):
web         | 2025-06-19 10:13:44.902 |   File "/app/manage.py", line 18, in <module>
web         | 2025-06-19 10:13:44.902 |     main()
web         | 2025-06-19 10:13:44.902 |   File "/app/manage.py", line 15, in main
web         | 2025-06-19 10:13:44.902 |     execute_from_command_line(sys.argv)
web         | 2025-06-19 10:13:44.902 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
web         | 2025-06-19 10:13:44.902 |     utility.execute()
web         | 2025-06-19 10:13:44.902 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 416, in execute
web         | 2025-06-19 10:13:44.903 |     django.setup()
web         | 2025-06-19 10:13:44.903 |   File "/usr/local/lib/python3.11/site-packages/django/__init__.py", line 24, in setup
web         | 2025-06-19 10:13:44.903 |     apps.populate(settings.INSTALLED_APPS)
web         | 2025-06-19 10:13:44.903 |   File "/usr/local/lib/python3.11/site-packages/django/apps/registry.py", line 91, in populate
web         | 2025-06-19 10:13:44.903 |     app_config = AppConfig.create(entry)
web         | 2025-06-19 10:13:44.903 |                  ^^^^^^^^^^^^^^^^^^^^^^^
web         | 2025-06-19 10:13:44.903 |   File "/usr/local/lib/python3.11/site-packages/django/apps/config.py", line 193, in create
web         | 2025-06-19 10:13:44.903 |     import_module(entry)
web         | 2025-06-19 10:13:44.903 |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
web         | 2025-06-19 10:13:44.903 |     return _bootstrap._gcd_import(name[level:], package, level)
web         | 2025-06-19 10:13:44.903 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
web         | 2025-06-19 10:13:44.903 |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
web         | 2025-06-19 10:13:44.903 |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
web         | 2025-06-19 10:13:44.903 |   File "<frozen importlib._bootstrap>", line 1140, in _find_and_load_unlocked
web         | 2025-06-19 10:13:44.903 | ModuleNotFoundError: No module named 'admin_interface'
celery-beat | 2025-06-19 10:13:46.030 | wait-for-it.sh: waiting 120 seconds for db:3306
celery-beat | 2025-06-19 10:13:46.032 | wait-for-it.sh: db:3306 is available after 0 seconds
celery-beat | 2025-06-19 10:13:46.240 | Traceback (most recent call last):
celery-beat | 2025-06-19 10:13:46.240 |   File "/app/manage.py", line 18, in <module>
celery-beat | 2025-06-19 10:13:46.241 |     main()
celery-beat | 2025-06-19 10:13:46.241 |   File "/app/manage.py", line 15, in main
celery-beat | 2025-06-19 10:13:46.241 |     execute_from_command_line(sys.argv)
celery-beat | 2025-06-19 10:13:46.241 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
celery-beat | 2025-06-19 10:13:46.241 |     utility.execute()
celery-beat | 2025-06-19 10:13:46.241 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 416, in execute
celery-beat | 2025-06-19 10:13:46.241 |     django.setup()
celery-beat | 2025-06-19 10:13:46.241 |   File "/usr/local/lib/python3.11/site-packages/django/__init__.py", line 24, in setup
celery-beat | 2025-06-19 10:13:46.241 |     apps.populate(settings.INSTALLED_APPS)
celery-beat | 2025-06-19 10:13:46.241 |   File "/usr/local/lib/python3.11/site-packages/django/apps/registry.py", line 91, in populate
celery-beat | 2025-06-19 10:13:46.241 |     app_config = AppConfig.create(entry)
celery-beat | 2025-06-19 10:13:46.241 |                  ^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-06-19 10:13:46.241 |   File "/usr/local/lib/python3.11/site-packages/django/apps/config.py", line 193, in create
celery-beat | 2025-06-19 10:13:46.241 |     import_module(entry)
celery-beat | 2025-06-19 10:13:46.241 |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
celery-beat | 2025-06-19 10:13:46.241 |     return _bootstrap._gcd_import(name[level:], package, level)
celery-beat | 2025-06-19 10:13:46.241 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-06-19 10:13:46.241 |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
celery-beat | 2025-06-19 10:13:46.241 |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
celery-beat | 2025-06-19 10:13:46.241 |   File "<frozen importlib._bootstrap>", line 1140, in _find_and_load_unlocked
celery-beat | 2025-06-19 10:13:46.241 | ModuleNotFoundError: No module named 'admin_interface'
celery      | 2025-06-19 10:13:46.642 | wait-for-it.sh: waiting 120 seconds for db:3306
celery      | 2025-06-19 10:13:46.644 | wait-for-it.sh: db:3306 is available after 0 seconds
nginx       | 2025-06-19 10:13:46.672 | 172.19.0.1 - - [19/Jun/2025:13:13:46 +0000] "GET /admin/reloj_fichador/registrodiario/?hora_fichada__range__gte=39610329&hora_fichada__range__lte= HTTP/1.1" 502 559 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
nginx       | 2025-06-19 10:13:46.672 | 2025/06/19 13:13:46 [error] 28#28: *2 connect() failed (111: Connection refused) while connecting to upstream, client: 172.19.0.1, server: localhost, request: "GET /admin/reloj_fichador/registrodiario/?hora_fichada__range__gte=39610329&hora_fichada__range__lte= HTTP/1.1", upstream: "http://172.19.0.7:58000/admin/reloj_fichador/registrodiario/?hora_fichada__range__gte=39610329&hora_fichada__range__lte=", host: "localhost:5080", referrer: "http://localhost:5080/admin/reloj_fichador/registrodiario/"
web         | 2025-06-19 10:13:46.720 | wait-for-it.sh: waiting 120 seconds for db:3306
web         | 2025-06-19 10:13:46.722 | wait-for-it.sh: db:3306 is available after 0 seconds
nginx       | 2025-06-19 10:13:46.799 | 2025/06/19 13:13:46 [error] 28#28: *2 connect() failed (111: Connection refused) while connecting to upstream, client: 172.19.0.1, server: localhost, request: "GET /favicon.ico HTTP/1.1", upstream: "http://172.19.0.7:58000/favicon.ico", host: "localhost:5080", referrer: "http://localhost:5080/admin/reloj_fichador/registrodiario/?hora_fichada__range__gte=39610329&hora_fichada__range__lte="
nginx       | 2025-06-19 10:13:46.801 | 172.19.0.1 - - [19/Jun/2025:13:13:46 +0000] "GET /favicon.ico HTTP/1.1" 502 559 "http://localhost:5080/admin/reloj_fichador/registrodiario/?hora_fichada__range__gte=39610329&hora_fichada__range__lte=" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
web         | 2025-06-19 10:13:47.031 | Traceback (most recent call last):
web         | 2025-06-19 10:13:47.031 |   File "/app/manage.py", line 18, in <module>
web         | 2025-06-19 10:13:47.031 |     main()
web         | 2025-06-19 10:13:47.031 |   File "/app/manage.py", line 15, in main
web         | 2025-06-19 10:13:47.031 |     execute_from_command_line(sys.argv)
web         | 2025-06-19 10:13:47.031 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
web         | 2025-06-19 10:13:47.031 |     utility.execute()
web         | 2025-06-19 10:13:47.031 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 416, in execute
web         | 2025-06-19 10:13:47.031 |     django.setup()
web         | 2025-06-19 10:13:47.031 |   File "/usr/local/lib/python3.11/site-packages/django/__init__.py", line 24, in setup
web         | 2025-06-19 10:13:47.031 |     apps.populate(settings.INSTALLED_APPS)
web         | 2025-06-19 10:13:47.031 |   File "/usr/local/lib/python3.11/site-packages/django/apps/registry.py", line 91, in populate
web         | 2025-06-19 10:13:47.031 |     app_config = AppConfig.create(entry)
web         | 2025-06-19 10:13:47.031 |                  ^^^^^^^^^^^^^^^^^^^^^^^
web         | 2025-06-19 10:13:47.031 |   File "/usr/local/lib/python3.11/site-packages/django/apps/config.py", line 193, in create
web         | 2025-06-19 10:13:47.031 |     import_module(entry)
web         | 2025-06-19 10:13:47.031 |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
web         | 2025-06-19 10:13:47.031 |     return _bootstrap._gcd_import(name[level:], package, level)
web         | 2025-06-19 10:13:47.031 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
web         | 2025-06-19 10:13:47.031 |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
web         | 2025-06-19 10:13:47.031 |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
web         | 2025-06-19 10:13:47.031 |   File "<frozen importlib._bootstrap>", line 1140, in _find_and_load_unlocked
web         | 2025-06-19 10:13:47.031 | ModuleNotFoundError: No module named 'admin_interface'
celery      | 2025-06-19 10:13:47.037 | Traceback (most recent call last):
celery      | 2025-06-19 10:13:47.037 |   File "/usr/local/bin/celery", line 8, in <module>
celery      | 2025-06-19 10:13:47.037 |     sys.exit(main())
celery      | 2025-06-19 10:13:47.037 |              ^^^^^^
celery      | 2025-06-19 10:13:47.037 |   File "/usr/local/lib/python3.11/site-packages/celery/__main__.py", line 15, in main
celery      | 2025-06-19 10:13:47.037 |     sys.exit(_main())
celery      | 2025-06-19 10:13:47.037 |              ^^^^^^^
celery      | 2025-06-19 10:13:47.037 |   File "/usr/local/lib/python3.11/site-packages/celery/bin/celery.py", line 236, in main
celery      | 2025-06-19 10:13:47.037 |     return celery(auto_envvar_prefix="CELERY")
celery      | 2025-06-19 10:13:47.037 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:47.037 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1157, in __call__
celery      | 2025-06-19 10:13:47.037 |     return self.main(*args, **kwargs)
celery      | 2025-06-19 10:13:47.037 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:47.037 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1078, in main
celery      | 2025-06-19 10:13:47.037 |     rv = self.invoke(ctx)
celery      | 2025-06-19 10:13:47.038 |          ^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:47.038 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1688, in invoke
celery      | 2025-06-19 10:13:47.038 |     return _process_result(sub_ctx.command.invoke(sub_ctx))
celery      | 2025-06-19 10:13:47.038 |                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:47.038 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1434, in invoke
celery      | 2025-06-19 10:13:47.038 |     return ctx.invoke(self.callback, **ctx.params)
celery      | 2025-06-19 10:13:47.038 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:47.038 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 783, in invoke
celery      | 2025-06-19 10:13:47.038 |     return __callback(*args, **kwargs)
celery      | 2025-06-19 10:13:47.038 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:47.038 |   File "/usr/local/lib/python3.11/site-packages/click/decorators.py", line 33, in new_func
celery      | 2025-06-19 10:13:47.038 |     return f(get_current_context(), *args, **kwargs)
celery      | 2025-06-19 10:13:47.038 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:47.038 |   File "/usr/local/lib/python3.11/site-packages/celery/bin/base.py", line 135, in caller
celery      | 2025-06-19 10:13:47.038 |     return f(ctx, *args, **kwargs)
celery      | 2025-06-19 10:13:47.038 |            ^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:47.038 |   File "/usr/local/lib/python3.11/site-packages/celery/bin/worker.py", line 348, in worker
celery      | 2025-06-19 10:13:47.038 |     worker = app.Worker(
celery      | 2025-06-19 10:13:47.038 |              ^^^^^^^^^^^
celery      | 2025-06-19 10:13:47.038 |   File "/usr/local/lib/python3.11/site-packages/celery/worker/worker.py", line 93, in __init__
celery      | 2025-06-19 10:13:47.038 |     self.app.loader.init_worker()
celery      | 2025-06-19 10:13:47.038 |   File "/usr/local/lib/python3.11/site-packages/celery/loaders/base.py", line 110, in init_worker
celery      | 2025-06-19 10:13:47.038 |     self.import_default_modules()
celery      | 2025-06-19 10:13:47.038 |   File "/usr/local/lib/python3.11/site-packages/celery/loaders/base.py", line 104, in import_default_modules
celery      | 2025-06-19 10:13:47.038 |     raise response
celery      | 2025-06-19 10:13:47.038 |   File "/usr/local/lib/python3.11/site-packages/celery/utils/dispatch/signal.py", line 276, in send
celery      | 2025-06-19 10:13:47.038 |     response = receiver(signal=self, sender=sender, **named)
celery      | 2025-06-19 10:13:47.038 |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:47.038 |   File "/usr/local/lib/python3.11/site-packages/celery/fixups/django.py", line 100, in on_import_modules
celery      | 2025-06-19 10:13:47.038 |     self.worker_fixup.validate_models()
celery      | 2025-06-19 10:13:47.038 |   File "/usr/local/lib/python3.11/site-packages/celery/fixups/django.py", line 138, in validate_models
celery      | 2025-06-19 10:13:47.038 |     self.django_setup()
celery      | 2025-06-19 10:13:47.038 |   File "/usr/local/lib/python3.11/site-packages/celery/fixups/django.py", line 134, in django_setup
celery      | 2025-06-19 10:13:47.038 |     django.setup()
celery      | 2025-06-19 10:13:47.038 |   File "/usr/local/lib/python3.11/site-packages/django/__init__.py", line 24, in setup
celery      | 2025-06-19 10:13:47.038 |     apps.populate(settings.INSTALLED_APPS)
celery      | 2025-06-19 10:13:47.038 |   File "/usr/local/lib/python3.11/site-packages/django/apps/registry.py", line 91, in populate
celery      | 2025-06-19 10:13:47.038 |     app_config = AppConfig.create(entry)
celery      | 2025-06-19 10:13:47.038 |                  ^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:47.038 |   File "/usr/local/lib/python3.11/site-packages/django/apps/config.py", line 193, in create
celery      | 2025-06-19 10:13:47.039 |     import_module(entry)
celery      | 2025-06-19 10:13:47.039 |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
celery      | 2025-06-19 10:13:47.039 |     return _bootstrap._gcd_import(name[level:], package, level)
celery      | 2025-06-19 10:13:47.039 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:47.039 |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
celery      | 2025-06-19 10:13:47.039 |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
celery      | 2025-06-19 10:13:47.039 |   File "<frozen importlib._bootstrap>", line 1140, in _find_and_load_unlocked
celery      | 2025-06-19 10:13:47.039 | ModuleNotFoundError: No module named 'admin_interface'
celery-beat | 2025-06-19 10:13:49.639 | wait-for-it.sh: waiting 120 seconds for db:3306
celery-beat | 2025-06-19 10:13:49.642 | wait-for-it.sh: db:3306 is available after 0 seconds
celery-beat | 2025-06-19 10:13:49.872 | Traceback (most recent call last):
celery-beat | 2025-06-19 10:13:49.872 |   File "/app/manage.py", line 18, in <module>
celery-beat | 2025-06-19 10:13:49.873 |     main()
celery-beat | 2025-06-19 10:13:49.873 |   File "/app/manage.py", line 15, in main
celery-beat | 2025-06-19 10:13:49.873 |     execute_from_command_line(sys.argv)
celery-beat | 2025-06-19 10:13:49.873 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
celery-beat | 2025-06-19 10:13:49.873 |     utility.execute()
celery-beat | 2025-06-19 10:13:49.873 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 416, in execute
celery-beat | 2025-06-19 10:13:49.873 |     django.setup()
celery-beat | 2025-06-19 10:13:49.873 |   File "/usr/local/lib/python3.11/site-packages/django/__init__.py", line 24, in setup
celery-beat | 2025-06-19 10:13:49.873 |     apps.populate(settings.INSTALLED_APPS)
celery-beat | 2025-06-19 10:13:49.873 |   File "/usr/local/lib/python3.11/site-packages/django/apps/registry.py", line 91, in populate
celery-beat | 2025-06-19 10:13:49.874 |     app_config = AppConfig.create(entry)
celery-beat | 2025-06-19 10:13:49.874 |                  ^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-06-19 10:13:49.874 |   File "/usr/local/lib/python3.11/site-packages/django/apps/config.py", line 193, in create
celery-beat | 2025-06-19 10:13:49.874 |     import_module(entry)
celery-beat | 2025-06-19 10:13:49.874 |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
celery-beat | 2025-06-19 10:13:49.874 |     return _bootstrap._gcd_import(name[level:], package, level)
celery-beat | 2025-06-19 10:13:49.874 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-06-19 10:13:49.874 |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
celery-beat | 2025-06-19 10:13:49.874 |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
celery-beat | 2025-06-19 10:13:49.874 |   File "<frozen importlib._bootstrap>", line 1140, in _find_and_load_unlocked
celery-beat | 2025-06-19 10:13:49.874 | ModuleNotFoundError: No module named 'admin_interface'
web         | 2025-06-19 10:13:50.439 | wait-for-it.sh: waiting 120 seconds for db:3306
web         | 2025-06-19 10:13:50.442 | wait-for-it.sh: db:3306 is available after 0 seconds
celery      | 2025-06-19 10:13:50.498 | wait-for-it.sh: waiting 120 seconds for db:3306
celery      | 2025-06-19 10:13:50.502 | wait-for-it.sh: db:3306 is available after 0 seconds
web         | 2025-06-19 10:13:50.732 | Traceback (most recent call last):
web         | 2025-06-19 10:13:50.732 |   File "/app/manage.py", line 18, in <module>
web         | 2025-06-19 10:13:50.732 |     main()
web         | 2025-06-19 10:13:50.732 |   File "/app/manage.py", line 15, in main
web         | 2025-06-19 10:13:50.732 |     execute_from_command_line(sys.argv)
web         | 2025-06-19 10:13:50.732 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
web         | 2025-06-19 10:13:50.732 |     utility.execute()
web         | 2025-06-19 10:13:50.732 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 416, in execute
web         | 2025-06-19 10:13:50.732 |     django.setup()
web         | 2025-06-19 10:13:50.732 |   File "/usr/local/lib/python3.11/site-packages/django/__init__.py", line 24, in setup
web         | 2025-06-19 10:13:50.732 |     apps.populate(settings.INSTALLED_APPS)
web         | 2025-06-19 10:13:50.732 |   File "/usr/local/lib/python3.11/site-packages/django/apps/registry.py", line 91, in populate
web         | 2025-06-19 10:13:50.732 |     app_config = AppConfig.create(entry)
web         | 2025-06-19 10:13:50.732 |                  ^^^^^^^^^^^^^^^^^^^^^^^
web         | 2025-06-19 10:13:50.732 |   File "/usr/local/lib/python3.11/site-packages/django/apps/config.py", line 193, in create
web         | 2025-06-19 10:13:50.732 |     import_module(entry)
web         | 2025-06-19 10:13:50.732 |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
web         | 2025-06-19 10:13:50.732 |     return _bootstrap._gcd_import(name[level:], package, level)
web         | 2025-06-19 10:13:50.733 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
web         | 2025-06-19 10:13:50.733 |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
web         | 2025-06-19 10:13:50.733 |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
web         | 2025-06-19 10:13:50.733 |   File "<frozen importlib._bootstrap>", line 1140, in _find_and_load_unlocked
web         | 2025-06-19 10:13:50.733 | ModuleNotFoundError: No module named 'admin_interface'
celery      | 2025-06-19 10:13:50.816 | Traceback (most recent call last):
celery      | 2025-06-19 10:13:50.816 |   File "/usr/local/bin/celery", line 8, in <module>
celery      | 2025-06-19 10:13:50.816 |     sys.exit(main())
celery      | 2025-06-19 10:13:50.816 |              ^^^^^^
celery      | 2025-06-19 10:13:50.816 |   File "/usr/local/lib/python3.11/site-packages/celery/__main__.py", line 15, in main
celery      | 2025-06-19 10:13:50.816 |     sys.exit(_main())
celery      | 2025-06-19 10:13:50.816 |              ^^^^^^^
celery      | 2025-06-19 10:13:50.816 |   File "/usr/local/lib/python3.11/site-packages/celery/bin/celery.py", line 236, in main
celery      | 2025-06-19 10:13:50.816 |     return celery(auto_envvar_prefix="CELERY")
celery      | 2025-06-19 10:13:50.816 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:50.816 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1157, in __call__
celery      | 2025-06-19 10:13:50.816 |     return self.main(*args, **kwargs)
celery      | 2025-06-19 10:13:50.816 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:50.816 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1078, in main
celery      | 2025-06-19 10:13:50.816 |     rv = self.invoke(ctx)
celery      | 2025-06-19 10:13:50.816 |          ^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:50.816 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1688, in invoke
celery      | 2025-06-19 10:13:50.816 |     return _process_result(sub_ctx.command.invoke(sub_ctx))
celery      | 2025-06-19 10:13:50.816 |                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:50.816 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1434, in invoke
celery      | 2025-06-19 10:13:50.816 |     return ctx.invoke(self.callback, **ctx.params)
celery      | 2025-06-19 10:13:50.816 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:50.816 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 783, in invoke
celery      | 2025-06-19 10:13:50.816 |     return __callback(*args, **kwargs)
celery      | 2025-06-19 10:13:50.816 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:50.816 |   File "/usr/local/lib/python3.11/site-packages/click/decorators.py", line 33, in new_func
celery      | 2025-06-19 10:13:50.816 |     return f(get_current_context(), *args, **kwargs)
celery      | 2025-06-19 10:13:50.816 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:50.816 |   File "/usr/local/lib/python3.11/site-packages/celery/bin/base.py", line 135, in caller
celery      | 2025-06-19 10:13:50.816 |     return f(ctx, *args, **kwargs)
celery      | 2025-06-19 10:13:50.816 |            ^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:50.816 |   File "/usr/local/lib/python3.11/site-packages/celery/bin/worker.py", line 348, in worker
celery      | 2025-06-19 10:13:50.816 |     worker = app.Worker(
celery      | 2025-06-19 10:13:50.816 |              ^^^^^^^^^^^
celery      | 2025-06-19 10:13:50.816 |   File "/usr/local/lib/python3.11/site-packages/celery/worker/worker.py", line 93, in __init__
celery      | 2025-06-19 10:13:50.816 |     self.app.loader.init_worker()
celery      | 2025-06-19 10:13:50.816 |   File "/usr/local/lib/python3.11/site-packages/celery/loaders/base.py", line 110, in init_worker
celery      | 2025-06-19 10:13:50.816 |     self.import_default_modules()
celery      | 2025-06-19 10:13:50.817 |   File "/usr/local/lib/python3.11/site-packages/celery/loaders/base.py", line 104, in import_default_modules
celery      | 2025-06-19 10:13:50.817 |     raise response
celery      | 2025-06-19 10:13:50.817 |   File "/usr/local/lib/python3.11/site-packages/celery/utils/dispatch/signal.py", line 276, in send
celery      | 2025-06-19 10:13:50.817 |     response = receiver(signal=self, sender=sender, **named)
celery      | 2025-06-19 10:13:50.817 |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:50.817 |   File "/usr/local/lib/python3.11/site-packages/celery/fixups/django.py", line 100, in on_import_modules
celery      | 2025-06-19 10:13:50.817 |     self.worker_fixup.validate_models()
celery      | 2025-06-19 10:13:50.817 |   File "/usr/local/lib/python3.11/site-packages/celery/fixups/django.py", line 138, in validate_models
celery      | 2025-06-19 10:13:50.817 |     self.django_setup()
celery      | 2025-06-19 10:13:50.817 |   File "/usr/local/lib/python3.11/site-packages/celery/fixups/django.py", line 134, in django_setup
celery      | 2025-06-19 10:13:50.817 |     django.setup()
celery      | 2025-06-19 10:13:50.817 |   File "/usr/local/lib/python3.11/site-packages/django/__init__.py", line 24, in setup
celery      | 2025-06-19 10:13:50.817 |     apps.populate(settings.INSTALLED_APPS)
celery      | 2025-06-19 10:13:50.817 |   File "/usr/local/lib/python3.11/site-packages/django/apps/registry.py", line 91, in populate
celery      | 2025-06-19 10:13:50.817 |     app_config = AppConfig.create(entry)
celery      | 2025-06-19 10:13:50.817 |                  ^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:50.817 |   File "/usr/local/lib/python3.11/site-packages/django/apps/config.py", line 193, in create
celery      | 2025-06-19 10:13:50.817 |     import_module(entry)
celery      | 2025-06-19 10:13:50.817 |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
celery      | 2025-06-19 10:13:50.817 |     return _bootstrap._gcd_import(name[level:], package, level)
celery      | 2025-06-19 10:13:50.817 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:50.817 |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
celery      | 2025-06-19 10:13:50.817 |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
celery      | 2025-06-19 10:13:50.817 |   File "<frozen importlib._bootstrap>", line 1140, in _find_and_load_unlocked
celery      | 2025-06-19 10:13:50.817 | ModuleNotFoundError: No module named 'admin_interface'
celery-beat | 2025-06-19 10:13:56.441 | wait-for-it.sh: waiting 120 seconds for db:3306
celery-beat | 2025-06-19 10:13:56.443 | wait-for-it.sh: db:3306 is available after 0 seconds
celery-beat | 2025-06-19 10:13:56.664 | Traceback (most recent call last):
celery-beat | 2025-06-19 10:13:56.664 |   File "/app/manage.py", line 18, in <module>
celery-beat | 2025-06-19 10:13:56.664 |     main()
celery-beat | 2025-06-19 10:13:56.664 |   File "/app/manage.py", line 15, in main
celery-beat | 2025-06-19 10:13:56.664 |     execute_from_command_line(sys.argv)
celery-beat | 2025-06-19 10:13:56.664 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
celery-beat | 2025-06-19 10:13:56.665 |     utility.execute()
celery-beat | 2025-06-19 10:13:56.665 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 416, in execute
celery-beat | 2025-06-19 10:13:56.665 |     django.setup()
celery-beat | 2025-06-19 10:13:56.665 |   File "/usr/local/lib/python3.11/site-packages/django/__init__.py", line 24, in setup
celery-beat | 2025-06-19 10:13:56.665 |     apps.populate(settings.INSTALLED_APPS)
celery-beat | 2025-06-19 10:13:56.665 |   File "/usr/local/lib/python3.11/site-packages/django/apps/registry.py", line 91, in populate
celery-beat | 2025-06-19 10:13:56.665 |     app_config = AppConfig.create(entry)
celery-beat | 2025-06-19 10:13:56.665 |                  ^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-06-19 10:13:56.665 |   File "/usr/local/lib/python3.11/site-packages/django/apps/config.py", line 193, in create
celery-beat | 2025-06-19 10:13:56.665 |     import_module(entry)
celery-beat | 2025-06-19 10:13:56.665 |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
celery-beat | 2025-06-19 10:13:56.665 |     return _bootstrap._gcd_import(name[level:], package, level)
celery-beat | 2025-06-19 10:13:56.665 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-06-19 10:13:56.665 |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
celery-beat | 2025-06-19 10:13:56.665 |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
celery-beat | 2025-06-19 10:13:56.665 |   File "<frozen importlib._bootstrap>", line 1140, in _find_and_load_unlocked
celery-beat | 2025-06-19 10:13:56.665 | ModuleNotFoundError: No module named 'admin_interface'
web         | 2025-06-19 10:13:57.311 | wait-for-it.sh: waiting 120 seconds for db:3306
web         | 2025-06-19 10:13:57.313 | wait-for-it.sh: db:3306 is available after 0 seconds
celery      | 2025-06-19 10:13:57.432 | wait-for-it.sh: waiting 120 seconds for db:3306
celery      | 2025-06-19 10:13:57.435 | wait-for-it.sh: db:3306 is available after 0 seconds
nginx       | 2025-06-19 10:13:57.501 | 172.19.0.1 - - [19/Jun/2025:13:13:57 +0000] "GET /admin/reloj_fichador/registrodiario/?hora_fichada__range__gte=39610329&hora_fichada__range__lte= HTTP/1.1" 502 559 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
nginx       | 2025-06-19 10:13:57.501 | 2025/06/19 13:13:57 [error] 28#28: *2 connect() failed (111: Connection refused) while connecting to upstream, client: 172.19.0.1, server: localhost, request: "GET /admin/reloj_fichador/registrodiario/?hora_fichada__range__gte=39610329&hora_fichada__range__lte= HTTP/1.1", upstream: "http://172.19.0.7:58000/admin/reloj_fichador/registrodiario/?hora_fichada__range__gte=39610329&hora_fichada__range__lte=", host: "localhost:5080", referrer: "http://localhost:5080/admin/reloj_fichador/registrodiario/"
nginx       | 2025-06-19 10:13:57.576 | 172.19.0.1 - - [19/Jun/2025:13:13:57 +0000] "GET /favicon.ico HTTP/1.1" 502 559 "http://localhost:5080/admin/reloj_fichador/registrodiario/?hora_fichada__range__gte=39610329&hora_fichada__range__lte=" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
nginx       | 2025-06-19 10:13:57.576 | 2025/06/19 13:13:57 [error] 28#28: *2 connect() failed (111: Connection refused) while connecting to upstream, client: 172.19.0.1, server: localhost, request: "GET /favicon.ico HTTP/1.1", upstream: "http://172.19.0.7:58000/favicon.ico", host: "localhost:5080", referrer: "http://localhost:5080/admin/reloj_fichador/registrodiario/?hora_fichada__range__gte=39610329&hora_fichada__range__lte="
web         | 2025-06-19 10:13:57.623 | Traceback (most recent call last):
web         | 2025-06-19 10:13:57.623 |   File "/app/manage.py", line 18, in <module>
web         | 2025-06-19 10:13:57.624 |     main()
web         | 2025-06-19 10:13:57.624 |   File "/app/manage.py", line 15, in main
web         | 2025-06-19 10:13:57.624 |     execute_from_command_line(sys.argv)
web         | 2025-06-19 10:13:57.624 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
web         | 2025-06-19 10:13:57.624 |     utility.execute()
web         | 2025-06-19 10:13:57.624 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 416, in execute
web         | 2025-06-19 10:13:57.624 |     django.setup()
web         | 2025-06-19 10:13:57.624 |   File "/usr/local/lib/python3.11/site-packages/django/__init__.py", line 24, in setup
web         | 2025-06-19 10:13:57.624 |     apps.populate(settings.INSTALLED_APPS)
web         | 2025-06-19 10:13:57.624 |   File "/usr/local/lib/python3.11/site-packages/django/apps/registry.py", line 91, in populate
web         | 2025-06-19 10:13:57.624 |     app_config = AppConfig.create(entry)
web         | 2025-06-19 10:13:57.624 |                  ^^^^^^^^^^^^^^^^^^^^^^^
web         | 2025-06-19 10:13:57.624 |   File "/usr/local/lib/python3.11/site-packages/django/apps/config.py", line 193, in create
web         | 2025-06-19 10:13:57.625 |     import_module(entry)
web         | 2025-06-19 10:13:57.625 |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
web         | 2025-06-19 10:13:57.625 |     return _bootstrap._gcd_import(name[level:], package, level)
web         | 2025-06-19 10:13:57.625 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
web         | 2025-06-19 10:13:57.625 |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
web         | 2025-06-19 10:13:57.625 |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
web         | 2025-06-19 10:13:57.625 |   File "<frozen importlib._bootstrap>", line 1140, in _find_and_load_unlocked
web         | 2025-06-19 10:13:57.625 | ModuleNotFoundError: No module named 'admin_interface'
celery      | 2025-06-19 10:13:57.775 | Traceback (most recent call last):
celery      | 2025-06-19 10:13:57.775 |   File "/usr/local/bin/celery", line 8, in <module>
celery      | 2025-06-19 10:13:57.775 |     sys.exit(main())
celery      | 2025-06-19 10:13:57.775 |              ^^^^^^
celery      | 2025-06-19 10:13:57.775 |   File "/usr/local/lib/python3.11/site-packages/celery/__main__.py", line 15, in main
celery      | 2025-06-19 10:13:57.775 |     sys.exit(_main())
celery      | 2025-06-19 10:13:57.775 |              ^^^^^^^
celery      | 2025-06-19 10:13:57.775 |   File "/usr/local/lib/python3.11/site-packages/celery/bin/celery.py", line 236, in main
celery      | 2025-06-19 10:13:57.775 |     return celery(auto_envvar_prefix="CELERY")
celery      | 2025-06-19 10:13:57.775 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:57.775 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1157, in __call__
celery      | 2025-06-19 10:13:57.775 |     return self.main(*args, **kwargs)
celery      | 2025-06-19 10:13:57.775 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:57.775 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1078, in main
celery      | 2025-06-19 10:13:57.775 |     rv = self.invoke(ctx)
celery      | 2025-06-19 10:13:57.775 |          ^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:57.775 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1688, in invoke
celery      | 2025-06-19 10:13:57.776 |     return _process_result(sub_ctx.command.invoke(sub_ctx))
celery      | 2025-06-19 10:13:57.776 |                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:57.776 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1434, in invoke
celery      | 2025-06-19 10:13:57.776 |     return ctx.invoke(self.callback, **ctx.params)
celery      | 2025-06-19 10:13:57.776 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:57.776 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 783, in invoke
celery      | 2025-06-19 10:13:57.776 |     return __callback(*args, **kwargs)
celery      | 2025-06-19 10:13:57.776 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:57.776 |   File "/usr/local/lib/python3.11/site-packages/click/decorators.py", line 33, in new_func
celery      | 2025-06-19 10:13:57.776 |     return f(get_current_context(), *args, **kwargs)
celery      | 2025-06-19 10:13:57.776 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:57.776 |   File "/usr/local/lib/python3.11/site-packages/celery/bin/base.py", line 135, in caller
celery      | 2025-06-19 10:13:57.776 |     return f(ctx, *args, **kwargs)
celery      | 2025-06-19 10:13:57.776 |            ^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:57.776 |   File "/usr/local/lib/python3.11/site-packages/celery/bin/worker.py", line 348, in worker
celery      | 2025-06-19 10:13:57.776 |     worker = app.Worker(
celery      | 2025-06-19 10:13:57.776 |              ^^^^^^^^^^^
celery      | 2025-06-19 10:13:57.776 |   File "/usr/local/lib/python3.11/site-packages/celery/worker/worker.py", line 93, in __init__
celery      | 2025-06-19 10:13:57.776 |     self.app.loader.init_worker()
celery      | 2025-06-19 10:13:57.776 |   File "/usr/local/lib/python3.11/site-packages/celery/loaders/base.py", line 110, in init_worker
celery      | 2025-06-19 10:13:57.776 |     self.import_default_modules()
celery      | 2025-06-19 10:13:57.776 |   File "/usr/local/lib/python3.11/site-packages/celery/loaders/base.py", line 104, in import_default_modules
celery      | 2025-06-19 10:13:57.776 |     raise response
celery      | 2025-06-19 10:13:57.776 |   File "/usr/local/lib/python3.11/site-packages/celery/utils/dispatch/signal.py", line 276, in send
celery      | 2025-06-19 10:13:57.776 |     response = receiver(signal=self, sender=sender, **named)
celery      | 2025-06-19 10:13:57.776 |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:57.776 |   File "/usr/local/lib/python3.11/site-packages/celery/fixups/django.py", line 100, in on_import_modules
celery      | 2025-06-19 10:13:57.776 |     self.worker_fixup.validate_models()
celery      | 2025-06-19 10:13:57.776 |   File "/usr/local/lib/python3.11/site-packages/celery/fixups/django.py", line 138, in validate_models
celery      | 2025-06-19 10:13:57.776 |     self.django_setup()
celery      | 2025-06-19 10:13:57.776 |   File "/usr/local/lib/python3.11/site-packages/celery/fixups/django.py", line 134, in django_setup
celery      | 2025-06-19 10:13:57.776 |     django.setup()
celery      | 2025-06-19 10:13:57.776 |   File "/usr/local/lib/python3.11/site-packages/django/__init__.py", line 24, in setup
celery      | 2025-06-19 10:13:57.776 |     apps.populate(settings.INSTALLED_APPS)
celery      | 2025-06-19 10:13:57.776 |   File "/usr/local/lib/python3.11/site-packages/django/apps/registry.py", line 91, in populate
celery      | 2025-06-19 10:13:57.776 |     app_config = AppConfig.create(entry)
celery      | 2025-06-19 10:13:57.776 |                  ^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:57.776 |   File "/usr/local/lib/python3.11/site-packages/django/apps/config.py", line 193, in create
celery      | 2025-06-19 10:13:57.776 |     import_module(entry)
celery      | 2025-06-19 10:13:57.776 |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
celery      | 2025-06-19 10:13:57.776 |     return _bootstrap._gcd_import(name[level:], package, level)
celery      | 2025-06-19 10:13:57.776 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:13:57.776 |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
celery      | 2025-06-19 10:13:57.776 |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
celery      | 2025-06-19 10:13:57.776 |   File "<frozen importlib._bootstrap>", line 1140, in _find_and_load_unlocked
celery      | 2025-06-19 10:13:57.776 | ModuleNotFoundError: No module named 'admin_interface'
celery-beat | 2025-06-19 10:14:09.631 | wait-for-it.sh: waiting 120 seconds for db:3306
celery-beat | 2025-06-19 10:14:09.633 | wait-for-it.sh: db:3306 is available after 0 seconds
celery-beat | 2025-06-19 10:14:09.846 | Traceback (most recent call last):
celery-beat | 2025-06-19 10:14:09.846 |   File "/app/manage.py", line 18, in <module>
celery-beat | 2025-06-19 10:14:09.846 |     main()
celery-beat | 2025-06-19 10:14:09.846 |   File "/app/manage.py", line 15, in main
celery-beat | 2025-06-19 10:14:09.846 |     execute_from_command_line(sys.argv)
celery-beat | 2025-06-19 10:14:09.846 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
celery-beat | 2025-06-19 10:14:09.847 |     utility.execute()
celery-beat | 2025-06-19 10:14:09.847 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 416, in execute
celery-beat | 2025-06-19 10:14:09.847 |     django.setup()
celery-beat | 2025-06-19 10:14:09.847 |   File "/usr/local/lib/python3.11/site-packages/django/__init__.py", line 24, in setup
celery-beat | 2025-06-19 10:14:09.847 |     apps.populate(settings.INSTALLED_APPS)
celery-beat | 2025-06-19 10:14:09.847 |   File "/usr/local/lib/python3.11/site-packages/django/apps/registry.py", line 91, in populate
celery-beat | 2025-06-19 10:14:09.847 |     app_config = AppConfig.create(entry)
celery-beat | 2025-06-19 10:14:09.847 |                  ^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-06-19 10:14:09.847 |   File "/usr/local/lib/python3.11/site-packages/django/apps/config.py", line 193, in create
celery-beat | 2025-06-19 10:14:09.847 |     import_module(entry)
celery-beat | 2025-06-19 10:14:09.847 |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
celery-beat | 2025-06-19 10:14:09.847 |     return _bootstrap._gcd_import(name[level:], package, level)
celery-beat | 2025-06-19 10:14:09.847 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-06-19 10:14:09.847 |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
celery-beat | 2025-06-19 10:14:09.847 |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
celery-beat | 2025-06-19 10:14:09.847 |   File "<frozen importlib._bootstrap>", line 1140, in _find_and_load_unlocked
celery-beat | 2025-06-19 10:14:09.847 | ModuleNotFoundError: No module named 'admin_interface'
web         | 2025-06-19 10:14:10.644 | wait-for-it.sh: waiting 120 seconds for db:3306
web         | 2025-06-19 10:14:10.645 | wait-for-it.sh: db:3306 is available after 0 seconds
celery      | 2025-06-19 10:14:10.780 | wait-for-it.sh: waiting 120 seconds for db:3306
celery      | 2025-06-19 10:14:10.783 | wait-for-it.sh: db:3306 is available after 0 seconds
web         | 2025-06-19 10:14:10.884 | Traceback (most recent call last):
web         | 2025-06-19 10:14:10.885 |   File "/app/manage.py", line 18, in <module>
web         | 2025-06-19 10:14:10.885 |     main()
web         | 2025-06-19 10:14:10.885 |   File "/app/manage.py", line 15, in main
web         | 2025-06-19 10:14:10.885 |     execute_from_command_line(sys.argv)
web         | 2025-06-19 10:14:10.885 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
web         | 2025-06-19 10:14:10.885 |     utility.execute()
web         | 2025-06-19 10:14:10.885 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 416, in execute
web         | 2025-06-19 10:14:10.885 |     django.setup()
web         | 2025-06-19 10:14:10.885 |   File "/usr/local/lib/python3.11/site-packages/django/__init__.py", line 24, in setup
web         | 2025-06-19 10:14:10.885 |     apps.populate(settings.INSTALLED_APPS)
web         | 2025-06-19 10:14:10.885 |   File "/usr/local/lib/python3.11/site-packages/django/apps/registry.py", line 91, in populate
web         | 2025-06-19 10:14:10.885 |     app_config = AppConfig.create(entry)
web         | 2025-06-19 10:14:10.885 |                  ^^^^^^^^^^^^^^^^^^^^^^^
web         | 2025-06-19 10:14:10.885 |   File "/usr/local/lib/python3.11/site-packages/django/apps/config.py", line 193, in create
web         | 2025-06-19 10:14:10.885 |     import_module(entry)
web         | 2025-06-19 10:14:10.885 |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
web         | 2025-06-19 10:14:10.885 |     return _bootstrap._gcd_import(name[level:], package, level)
web         | 2025-06-19 10:14:10.885 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
web         | 2025-06-19 10:14:10.885 |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
web         | 2025-06-19 10:14:10.885 |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
web         | 2025-06-19 10:14:10.885 |   File "<frozen importlib._bootstrap>", line 1140, in _find_and_load_unlocked
web         | 2025-06-19 10:14:10.885 | ModuleNotFoundError: No module named 'admin_interface'
celery      | 2025-06-19 10:14:11.081 | Traceback (most recent call last):
celery      | 2025-06-19 10:14:11.081 |   File "/usr/local/bin/celery", line 8, in <module>
celery      | 2025-06-19 10:14:11.081 |     sys.exit(main())
celery      | 2025-06-19 10:14:11.081 |              ^^^^^^
celery      | 2025-06-19 10:14:11.081 |   File "/usr/local/lib/python3.11/site-packages/celery/__main__.py", line 15, in main
celery      | 2025-06-19 10:14:11.081 |     sys.exit(_main())
celery      | 2025-06-19 10:14:11.081 |              ^^^^^^^
celery      | 2025-06-19 10:14:11.081 |   File "/usr/local/lib/python3.11/site-packages/celery/bin/celery.py", line 236, in main
celery      | 2025-06-19 10:14:11.081 |     return celery(auto_envvar_prefix="CELERY")
celery      | 2025-06-19 10:14:11.081 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:14:11.081 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1157, in __call__
celery      | 2025-06-19 10:14:11.081 |     return self.main(*args, **kwargs)
celery      | 2025-06-19 10:14:11.081 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:14:11.081 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1078, in main
celery      | 2025-06-19 10:14:11.081 |     rv = self.invoke(ctx)
celery      | 2025-06-19 10:14:11.081 |          ^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:14:11.081 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1688, in invoke
celery      | 2025-06-19 10:14:11.081 |     return _process_result(sub_ctx.command.invoke(sub_ctx))
celery      | 2025-06-19 10:14:11.081 |                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:14:11.081 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1434, in invoke
celery      | 2025-06-19 10:14:11.082 |     return ctx.invoke(self.callback, **ctx.params)
celery      | 2025-06-19 10:14:11.082 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:14:11.082 |   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 783, in invoke
celery      | 2025-06-19 10:14:11.082 |     return __callback(*args, **kwargs)
celery      | 2025-06-19 10:14:11.082 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:14:11.082 |   File "/usr/local/lib/python3.11/site-packages/click/decorators.py", line 33, in new_func
celery      | 2025-06-19 10:14:11.082 |     return f(get_current_context(), *args, **kwargs)
celery      | 2025-06-19 10:14:11.082 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:14:11.082 |   File "/usr/local/lib/python3.11/site-packages/celery/bin/base.py", line 135, in caller
celery      | 2025-06-19 10:14:11.082 |     return f(ctx, *args, **kwargs)
celery      | 2025-06-19 10:14:11.082 |            ^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:14:11.082 |   File "/usr/local/lib/python3.11/site-packages/celery/bin/worker.py", line 348, in worker
celery      | 2025-06-19 10:14:11.082 |     worker = app.Worker(
celery      | 2025-06-19 10:14:11.082 |              ^^^^^^^^^^^
celery      | 2025-06-19 10:14:11.082 |   File "/usr/local/lib/python3.11/site-packages/celery/worker/worker.py", line 93, in __init__
celery      | 2025-06-19 10:14:11.082 |     self.app.loader.init_worker()
celery      | 2025-06-19 10:14:11.082 |   File "/usr/local/lib/python3.11/site-packages/celery/loaders/base.py", line 110, in init_worker
celery      | 2025-06-19 10:14:11.082 |     self.import_default_modules()
celery      | 2025-06-19 10:14:11.082 |   File "/usr/local/lib/python3.11/site-packages/celery/loaders/base.py", line 104, in import_default_modules
celery      | 2025-06-19 10:14:11.082 |     raise response
celery      | 2025-06-19 10:14:11.082 |   File "/usr/local/lib/python3.11/site-packages/celery/utils/dispatch/signal.py", line 276, in send
celery      | 2025-06-19 10:14:11.082 |     response = receiver(signal=self, sender=sender, **named)
celery      | 2025-06-19 10:14:11.082 |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:14:11.082 |   File "/usr/local/lib/python3.11/site-packages/celery/fixups/django.py", line 100, in on_import_modules
celery      | 2025-06-19 10:14:11.082 |     self.worker_fixup.validate_models()
celery      | 2025-06-19 10:14:11.082 |   File "/usr/local/lib/python3.11/site-packages/celery/fixups/django.py", line 138, in validate_models
celery      | 2025-06-19 10:14:11.082 |     self.django_setup()
celery      | 2025-06-19 10:14:11.082 |   File "/usr/local/lib/python3.11/site-packages/celery/fixups/django.py", line 134, in django_setup
celery      | 2025-06-19 10:14:11.082 |     django.setup()
celery      | 2025-06-19 10:14:11.082 |   File "/usr/local/lib/python3.11/site-packages/django/__init__.py", line 24, in setup
celery      | 2025-06-19 10:14:11.082 |     apps.populate(settings.INSTALLED_APPS)
celery      | 2025-06-19 10:14:11.082 |   File "/usr/local/lib/python3.11/site-packages/django/apps/registry.py", line 91, in populate
celery      | 2025-06-19 10:14:11.082 |     app_config = AppConfig.create(entry)
celery      | 2025-06-19 10:14:11.083 |                  ^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:14:11.083 |   File "/usr/local/lib/python3.11/site-packages/django/apps/config.py", line 193, in create
celery      | 2025-06-19 10:14:11.083 |     import_module(entry)
celery      | 2025-06-19 10:14:11.083 |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
celery      | 2025-06-19 10:14:11.083 |     return _bootstrap._gcd_import(name[level:], package, level)
celery      | 2025-06-19 10:14:11.083 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-06-19 10:14:11.083 |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
celery      | 2025-06-19 10:14:11.083 |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
celery      | 2025-06-19 10:14:11.083 |   File "<frozen importlib._bootstrap>", line 1140, in _find_and_load_unlocked
celery      | 2025-06-19 10:14:11.083 | ModuleNotFoundError: No module named 'admin_interface'