db          | 2025-04-14 11:59:53.167 | 2025-04-14 14:59:53+00:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 8.4.0-1.el9 started.
redis       | 2025-04-14 11:59:53.247 | 1:C 14 Apr 2025 14:59:53.246 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
redis       | 2025-04-14 11:59:53.247 | 1:C 14 Apr 2025 14:59:53.246 * Redis version=7.4.2, bits=64, commit=00000000, modified=0, pid=1, just started
redis       | 2025-04-14 11:59:53.247 | 1:C 14 Apr 2025 14:59:53.246 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
redis       | 2025-04-14 11:59:53.247 | 1:M 14 Apr 2025 14:59:53.247 * monotonic clock: POSIX clock_gettime
redis       | 2025-04-14 11:59:53.247 | 1:M 14 Apr 2025 14:59:53.247 * Running mode=standalone, port=6379.
redis       | 2025-04-14 11:59:53.247 | 1:M 14 Apr 2025 14:59:53.247 * Server initialized
redis       | 2025-04-14 11:59:53.247 | 1:M 14 Apr 2025 14:59:53.247 * Ready to accept connections tcp
db          | 2025-04-14 11:59:53.505 | 2025-04-14 14:59:53+00:00 [Note] [Entrypoint]: Switching to dedicated user 'mysql'
db          | 2025-04-14 11:59:53.516 | 2025-04-14 14:59:53+00:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 8.4.0-1.el9 started.
db          | 2025-04-14 11:59:53.684 | '/var/lib/mysql/mysql.sock' -> '/var/run/mysqld/mysqld.sock'
db          | 2025-04-14 11:59:53.887 | 2025-04-14T14:59:53.693430Z 0 [System] [MY-015015] [Server] MySQL Server - start.
db          | 2025-04-14 11:59:53.887 | 2025-04-14T14:59:53.884001Z 0 [System] [MY-010116] [Server] /usr/sbin/mysqld (mysqld 8.4.0) starting as process 1
db          | 2025-04-14 11:59:53.887 | 2025-04-14T14:59:53.886282Z 0 [Warning] [MY-010159] [Server] Setting lower_case_table_names=2 because file system for /var/lib/mysql/ is case insensitive
db          | 2025-04-14 11:59:53.895 | 2025-04-14T14:59:53.895509Z 1 [System] [MY-013576] [InnoDB] InnoDB initialization has started.
db          | 2025-04-14 11:59:54.460 | 2025-04-14T14:59:54.460610Z 1 [System] [MY-013577] [InnoDB] InnoDB initialization has ended.
db          | 2025-04-14 11:59:54.858 | 2025-04-14T14:59:54.857913Z 0 [Warning] [MY-010068] [Server] CA certificate ca.pem is self signed.
db          | 2025-04-14 11:59:54.858 | 2025-04-14T14:59:54.858186Z 0 [System] [MY-013602] [Server] Channel mysql_main configured to support TLS. Encrypted connections are now supported for this channel.
db          | 2025-04-14 11:59:54.869 | 2025-04-14T14:59:54.869392Z 0 [Warning] [MY-011810] [Server] Insecure configuration for --pid-file: Location '/var/run/mysqld' in the path is accessible to all OS users. Consider choosing a different directory.
db          | 2025-04-14 11:59:54.899 | 2025-04-14T14:59:54.899776Z 0 [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections. Version: '8.4.0'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server - GPL.
db          | 2025-04-14 11:59:55.155 | 2025-04-14T14:59:55.155405Z 0 [System] [MY-011323] [Server] X Plugin ready for connections. Bind-address: '::' port: 33060, socket: /var/run/mysqld/mysqlx.sock
web         | 2025-04-14 11:59:58.730 | wait-for-it.sh: waiting 120 seconds for db:3306
web         | 2025-04-14 11:59:58.734 | wait-for-it.sh: db:3306 is available after 0 seconds
birt        | 2025-04-14 11:59:58.812 | NOTE: Picked up JDK_JAVA_OPTIONS:  --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.rmi/sun.rmi.transport=ALL-UNNAMED
backup      | 2025-04-14 11:59:58.834 | wait-for-it.sh: waiting 120 seconds for db:3306
backup      | 2025-04-14 11:59:58.839 | wait-for-it.sh: db:3306 is available after 0 seconds
backup      | 2025-04-14 11:59:58.844 | mysqldump: [Warning] Using a password on the command line interface can be insecure.
celery      | 2025-04-14 11:59:58.889 | wait-for-it.sh: waiting 120 seconds for db:3306
celery      | 2025-04-14 11:59:58.893 | wait-for-it.sh: db:3306 is available after 0 seconds
nginx       | 2025-04-14 11:59:59.058 | /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
nginx       | 2025-04-14 11:59:59.058 | /docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
nginx       | 2025-04-14 11:59:59.061 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
celery-beat | 2025-04-14 11:59:59.064 | wait-for-it.sh: waiting 120 seconds for db:3306
celery-beat | 2025-04-14 11:59:59.072 | wait-for-it.sh: db:3306 is available after 0 seconds
nginx       | 2025-04-14 11:59:59.082 | 10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
nginx       | 2025-04-14 11:59:59.125 | 10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
nginx       | 2025-04-14 11:59:59.125 | /docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
nginx       | 2025-04-14 11:59:59.126 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
nginx       | 2025-04-14 11:59:59.130 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
nginx       | 2025-04-14 11:59:59.132 | /docker-entrypoint.sh: Configuration complete; ready for start up
backup      | 2025-04-14 11:59:59.227 | Limpiando backups antiguos...
backup      | 2025-04-14 11:59:59.241 | Limpieza completada. Se mantienen los 10 backups más recientes.
birt        | 2025-04-14 11:59:59.444 | 14-Apr-2025 14:59:59.439 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Server version name:   Apache Tomcat/9.0.102
birt        | 2025-04-14 11:59:59.445 | 14-Apr-2025 14:59:59.445 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Server built:          Mar 3 2025 19:33:14 UTC
birt        | 2025-04-14 11:59:59.445 | 14-Apr-2025 14:59:59.445 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Server version number: 9.0.102.0
birt        | 2025-04-14 11:59:59.445 | 14-Apr-2025 14:59:59.445 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log OS Name:               Linux
birt        | 2025-04-14 11:59:59.446 | 14-Apr-2025 14:59:59.446 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log OS Version:            5.15.167.4-microsoft-standard-WSL2
birt        | 2025-04-14 11:59:59.446 | 14-Apr-2025 14:59:59.446 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Architecture:          amd64
birt        | 2025-04-14 11:59:59.446 | 14-Apr-2025 14:59:59.446 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Java Home:             /opt/java/openjdk
birt        | 2025-04-14 11:59:59.446 | 14-Apr-2025 14:59:59.446 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log JVM Version:           21.0.6+7-LTS
birt        | 2025-04-14 11:59:59.446 | 14-Apr-2025 14:59:59.446 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log JVM Vendor:            Eclipse Adoptium
birt        | 2025-04-14 11:59:59.447 | 14-Apr-2025 14:59:59.447 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log CATALINA_BASE:         /usr/local/tomcat
birt        | 2025-04-14 11:59:59.447 | 14-Apr-2025 14:59:59.447 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log CATALINA_HOME:         /usr/local/tomcat
birt        | 2025-04-14 11:59:59.487 | 14-Apr-2025 14:59:59.487 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.lang=ALL-UNNAMED
birt        | 2025-04-14 11:59:59.487 | 14-Apr-2025 14:59:59.487 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.lang.invoke=ALL-UNNAMED
birt        | 2025-04-14 11:59:59.487 | 14-Apr-2025 14:59:59.487 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.lang.reflect=ALL-UNNAMED
birt        | 2025-04-14 11:59:59.487 | 14-Apr-2025 14:59:59.487 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.io=ALL-UNNAMED
birt        | 2025-04-14 11:59:59.487 | 14-Apr-2025 14:59:59.487 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.util=ALL-UNNAMED
birt        | 2025-04-14 11:59:59.487 | 14-Apr-2025 14:59:59.487 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.util.concurrent=ALL-UNNAMED
birt        | 2025-04-14 11:59:59.487 | 14-Apr-2025 14:59:59.487 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.rmi/sun.rmi.transport=ALL-UNNAMED
birt        | 2025-04-14 11:59:59.487 | 14-Apr-2025 14:59:59.487 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.util.logging.config.file=/usr/local/tomcat/conf/logging.properties
birt        | 2025-04-14 11:59:59.487 | 14-Apr-2025 14:59:59.487 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager
birt        | 2025-04-14 11:59:59.487 | 14-Apr-2025 14:59:59.487 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.awt.headless=true
birt        | 2025-04-14 11:59:59.487 | 14-Apr-2025 14:59:59.487 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djdk.tls.ephemeralDHKeySize=2048
birt        | 2025-04-14 11:59:59.487 | 14-Apr-2025 14:59:59.487 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.protocol.handler.pkgs=org.apache.catalina.webresources
birt        | 2025-04-14 11:59:59.487 | 14-Apr-2025 14:59:59.487 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dsun.io.useCanonCaches=false
birt        | 2025-04-14 11:59:59.488 | 14-Apr-2025 14:59:59.487 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dorg.apache.catalina.security.SecurityListener.UMASK=0027
birt        | 2025-04-14 11:59:59.488 | 14-Apr-2025 14:59:59.487 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dignore.endorsed.dirs=
birt        | 2025-04-14 11:59:59.488 | 14-Apr-2025 14:59:59.488 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dcatalina.base=/usr/local/tomcat
birt        | 2025-04-14 11:59:59.488 | 14-Apr-2025 14:59:59.488 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dcatalina.home=/usr/local/tomcat
birt        | 2025-04-14 11:59:59.488 | 14-Apr-2025 14:59:59.488 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.io.tmpdir=/usr/local/tomcat/temp
birt        | 2025-04-14 11:59:59.498 | 14-Apr-2025 14:59:59.498 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent Loaded Apache Tomcat Native library [1.3.1] using APR version [1.7.2].
birt        | 2025-04-14 11:59:59.498 | 14-Apr-2025 14:59:59.498 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent APR capabilities: IPv6 [true], sendfile [true], accept filters [false], random [true], UDS [true].
birt        | 2025-04-14 11:59:59.498 | 14-Apr-2025 14:59:59.498 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent APR/OpenSSL configuration: useAprConnector [false], useOpenSSL [true]
birt        | 2025-04-14 11:59:59.505 | 14-Apr-2025 14:59:59.504 INFO [main] org.apache.catalina.core.AprLifecycleListener.initializeSSL OpenSSL successfully initialized [OpenSSL 3.0.13 30 Jan 2024]
birt        | 2025-04-14 11:59:59.990 | 14-Apr-2025 14:59:59.990 INFO [main] org.apache.coyote.AbstractProtocol.init Initializing ProtocolHandler ["http-nio-8080"]
birt        | 2025-04-14 12:00:00.010 | 14-Apr-2025 15:00:00.010 INFO [main] org.apache.catalina.startup.Catalina.load Server initialization in [828] milliseconds
birt        | 2025-04-14 12:00:00.067 | 14-Apr-2025 15:00:00.067 INFO [main] org.apache.catalina.core.StandardService.startInternal Starting service [Catalina]
birt        | 2025-04-14 12:00:00.068 | 14-Apr-2025 15:00:00.067 INFO [main] org.apache.catalina.core.StandardEngine.startInternal Starting Servlet engine: [Apache Tomcat/9.0.102]
birt        | 2025-04-14 12:00:00.089 | 14-Apr-2025 15:00:00.089 INFO [main] org.apache.catalina.startup.HostConfig.deployWAR Deploying web application archive [/usr/local/tomcat/webapps/birt.war]
web         | 2025-04-14 12:00:00.239 | Operations to perform:
web         | 2025-04-14 12:00:00.239 |   Apply all migrations: admin, admin_interface, auth, contenttypes, django_celery_beat, django_celery_results, reloj_fichador, sessions
web         | 2025-04-14 12:00:00.239 | Running migrations:
web         | 2025-04-14 12:00:00.239 |   No migrations to apply.
celery      | 2025-04-14 12:00:00.348 |  
celery      | 2025-04-14 12:00:00.348 |  -------------- celery@c0d08e9bd461 v5.4.0 (opalescent)
celery      | 2025-04-14 12:00:00.348 | --- ***** ----- 
celery      | 2025-04-14 12:00:00.348 | -- ******* ---- Linux-5.15.167.4-microsoft-standard-WSL2-x86_64-with-glibc2.36 2025-04-14 12:00:00
celery      | 2025-04-14 12:00:00.348 | - *** --- * --- 
celery      | 2025-04-14 12:00:00.348 | - ** ---------- [config]
celery      | 2025-04-14 12:00:00.348 | - ** ---------- .> app:         mantenedor:0x7f882e991310
celery      | 2025-04-14 12:00:00.348 | - ** ---------- .> transport:   redis://redis:6379/5
celery      | 2025-04-14 12:00:00.348 | - ** ---------- .> results:     disabled://
celery      | 2025-04-14 12:00:00.348 | - *** --- * --- .> concurrency: 6 (prefork)
celery      | 2025-04-14 12:00:00.348 | -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
celery      | 2025-04-14 12:00:00.348 | --- ***** ----- 
celery      | 2025-04-14 12:00:00.348 |  -------------- [queues]
celery      | 2025-04-14 12:00:00.348 |                 .> celery           exchange=celery(direct) key=celery
celery      | 2025-04-14 12:00:00.348 |                 
celery      | 2025-04-14 12:00:00.348 | 
celery      | 2025-04-14 12:00:00.348 | [tasks]
celery      | 2025-04-14 12:00:00.348 |   . apps.reloj_fichador.tasks.crear_asistencia_prueba
celery      | 2025-04-14 12:00:00.348 |   . apps.reloj_fichador.tasks.generar_registros_asistencia
celery      | 2025-04-14 12:00:00.348 |   . apps.reloj_fichador.tasks.prueba_tarea
celery      | 2025-04-14 12:00:00.348 |   . mantenedor.celery.debug_task
celery      | 2025-04-14 12:00:00.348 | 
celery-beat | 2025-04-14 12:00:00.549 | Operations to perform:
celery-beat | 2025-04-14 12:00:00.549 |   Apply all migrations: admin, admin_interface, auth, contenttypes, django_celery_beat, django_celery_results, reloj_fichador, sessions
celery-beat | 2025-04-14 12:00:00.549 | Running migrations:
celery-beat | 2025-04-14 12:00:00.549 |   No migrations to apply.
celery      | 2025-04-14 12:00:00.762 | [2025-04-14 12:00:00,761: INFO/MainProcess] Connected to redis://redis:6379/5
celery      | 2025-04-14 12:00:00.765 | [2025-04-14 12:00:00,765: INFO/MainProcess] mingle: searching for neighbors
birt        | 2025-04-14 12:00:00.772 | 14-Apr-2025 15:00:00.771 INFO [main] org.apache.jasper.servlet.TldScanner.scanJars At least one JAR was scanned for TLDs yet contained no TLDs. Enable debug logging for this logger for a complete list of JARs that were scanned but no TLDs were found in them. Skipping unneeded JARs during scanning can improve startup time and JSP compilation time.
birt        | 2025-04-14 12:00:00.807 | 14-Apr-2025 15:00:00.807 INFO [main] org.apache.catalina.startup.HostConfig.deployWAR Deployment of web application archive [/usr/local/tomcat/webapps/birt.war] has finished in [718] ms
birt        | 2025-04-14 12:00:00.810 | 14-Apr-2025 15:00:00.810 INFO [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["http-nio-8080"]
birt        | 2025-04-14 12:00:00.823 | 14-Apr-2025 15:00:00.822 INFO [main] org.apache.catalina.startup.Catalina.start Server startup in [810] milliseconds
web         | 2025-04-14 12:00:01.312 | Found another file with the destination path 'admin/js/cancel.js'. It will be ignored since only the first encountered file is collected. If this is not what you want, make sure every static file has a unique path.
web         | 2025-04-14 12:00:01.312 | Found another file with the destination path 'admin/js/popup_response.js'. It will be ignored since only the first encountered file is collected. If this is not what you want, make sure every static file has a unique path.
web         | 2025-04-14 12:00:01.312 | 
web         | 2025-04-14 12:00:01.312 | 0 static files copied to '/app/staticfiles', 225 unmodified.
web         | 2025-04-14 12:00:01.507 | [2025-04-14 15:00:01 +0000] [1] [INFO] Starting gunicorn 23.0.0
web         | 2025-04-14 12:00:01.507 | [2025-04-14 15:00:01 +0000] [1] [INFO] Listening at: http://0.0.0.0:58000 (1)
web         | 2025-04-14 12:00:01.507 | [2025-04-14 15:00:01 +0000] [1] [INFO] Using worker: sync
web         | 2025-04-14 12:00:01.509 | [2025-04-14 15:00:01 +0000] [75] [INFO] Booting worker with pid: 75
web         | 2025-04-14 12:00:01.528 | [2025-04-14 15:00:01 +0000] [76] [INFO] Booting worker with pid: 76
web         | 2025-04-14 12:00:01.598 | [2025-04-14 15:00:01 +0000] [77] [INFO] Booting worker with pid: 77
celery-beat | 2025-04-14 12:00:01.739 | [2025-04-14 12:00:01,739: INFO/MainProcess] beat: Starting...
celery      | 2025-04-14 12:00:01.770 | [2025-04-14 12:00:01,770: INFO/MainProcess] mingle: all alone
celery-beat | 2025-04-14 12:00:01.778 | [2025-04-14 12:00:01,778: INFO/MainProcess] DatabaseScheduler: Schedule changed.
celery      | 2025-04-14 12:00:01.778 | [2025-04-14 12:00:01,777: INFO/MainProcess] celery@c0d08e9bd461 ready.
db          | 2025-04-14 12:24:17.189 | 2025-04-14T15:24:17.189198Z 0 [System] [MY-013172] [Server] Received SHUTDOWN from user <via user signal>. Shutting down mysqld (Version: 8.4.0).
birt        | 2025-04-14 12:24:17.191 | 14-Apr-2025 15:24:17.191 INFO [Thread-1] org.apache.coyote.AbstractProtocol.pause Pausing ProtocolHandler ["http-nio-8080"]
birt        | 2025-04-14 12:24:17.193 | 14-Apr-2025 15:24:17.193 INFO [Thread-1] org.apache.catalina.core.StandardService.stopInternal Stopping service [Catalina]
celery      | 2025-04-14 12:24:17.199 | 
celery      | 2025-04-14 12:24:17.199 | worker: Warm shutdown (MainProcess)
birt        | 2025-04-14 12:24:17.200 | 14-Apr-2025 15:24:17.199 INFO [Thread-1] org.apache.coyote.AbstractProtocol.stop Stopping ProtocolHandler ["http-nio-8080"]
birt        | 2025-04-14 12:24:17.203 | 14-Apr-2025 15:24:17.203 INFO [Thread-1] org.apache.coyote.AbstractProtocol.destroy Destroying ProtocolHandler ["http-nio-8080"]
redis       | 2025-04-14 12:24:17.227 | 1:signal-handler (1744644257) Received SIGTERM scheduling shutdown...
web         | 2025-04-14 12:24:17.237 | [2025-04-14 15:24:17 +0000] [1] [INFO] Handling signal: term
web         | 2025-04-14 12:24:17.238 | [2025-04-14 12:24:17 -0300] [76] [INFO] Worker exiting (pid: 76)
web         | 2025-04-14 12:24:17.238 | [2025-04-14 12:24:17 -0300] [75] [INFO] Worker exiting (pid: 75)
web         | 2025-04-14 12:24:17.238 | [2025-04-14 12:24:17 -0300] [77] [INFO] Worker exiting (pid: 77)
redis       | 2025-04-14 12:24:17.277 | 1:M 14 Apr 2025 15:24:17.277 * User requested shutdown...
redis       | 2025-04-14 12:24:17.278 | 1:M 14 Apr 2025 15:24:17.277 * Saving the final RDB snapshot before exiting.
redis       | 2025-04-14 12:24:17.281 | 1:M 14 Apr 2025 15:24:17.280 * DB saved on disk
redis       | 2025-04-14 12:24:17.281 | 1:M 14 Apr 2025 15:24:17.280 # Redis is now ready to exit, bye bye...
celery-beat | 2025-04-14 12:24:17.412 | celery beat v5.4.0 (opalescent) is starting.
celery-beat | 2025-04-14 12:24:17.412 | __    -    ... __   -        _
celery-beat | 2025-04-14 12:24:17.412 | LocalTime -> 2025-04-14 12:00:01
celery-beat | 2025-04-14 12:24:17.412 | Configuration ->
celery-beat | 2025-04-14 12:24:17.412 |     . broker -> redis://redis:6379/5
celery-beat | 2025-04-14 12:24:17.412 |     . loader -> celery.loaders.app.AppLoader
celery-beat | 2025-04-14 12:24:17.412 |     . scheduler -> django_celery_beat.schedulers.DatabaseScheduler
celery-beat | 2025-04-14 12:24:17.412 | 
celery-beat | 2025-04-14 12:24:17.412 |     . logfile -> [stderr]@%INFO
celery-beat | 2025-04-14 12:24:17.412 |     . maxinterval -> 5.00 seconds (5s)
web         | 2025-04-14 12:24:17.546 | [2025-04-14 15:24:17 +0000] [1] [INFO] Shutting down: Master
celery-beat | 2025-04-14 12:24:18.961 | wait-for-it.sh: waiting 120 seconds for db:3306
nginx       | 2025-04-14 12:24:19.329 | /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
nginx       | 2025-04-14 12:24:19.329 | /docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
nginx       | 2025-04-14 12:24:19.330 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
nginx       | 2025-04-14 12:24:19.331 | 10-listen-on-ipv6-by-default.sh: info: IPv6 listen already enabled
nginx       | 2025-04-14 12:24:19.331 | /docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
nginx       | 2025-04-14 12:24:19.331 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
nginx       | 2025-04-14 12:24:19.334 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
nginx       | 2025-04-14 12:24:19.336 | /docker-entrypoint.sh: Configuration complete; ready for start up
birt        | 2025-04-14 12:24:19.394 | NOTE: Picked up JDK_JAVA_OPTIONS:  --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.rmi/sun.rmi.transport=ALL-UNNAMED
redis       | 2025-04-14 12:24:19.467 | 1:C 14 Apr 2025 15:24:19.466 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
redis       | 2025-04-14 12:24:19.467 | 1:C 14 Apr 2025 15:24:19.466 * Redis version=7.4.2, bits=64, commit=00000000, modified=0, pid=1, just started
redis       | 2025-04-14 12:24:19.467 | 1:C 14 Apr 2025 15:24:19.466 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
redis       | 2025-04-14 12:24:19.467 | 1:M 14 Apr 2025 15:24:19.466 * monotonic clock: POSIX clock_gettime
redis       | 2025-04-14 12:24:19.467 | 1:M 14 Apr 2025 15:24:19.467 * Running mode=standalone, port=6379.
redis       | 2025-04-14 12:24:19.467 | 1:M 14 Apr 2025 15:24:19.467 * Server initialized
redis       | 2025-04-14 12:24:19.467 | 1:M 14 Apr 2025 15:24:19.467 * Loading RDB produced by version 7.4.2
redis       | 2025-04-14 12:24:19.467 | 1:M 14 Apr 2025 15:24:19.467 * RDB age 2 seconds
redis       | 2025-04-14 12:24:19.467 | 1:M 14 Apr 2025 15:24:19.467 * RDB memory usage when created 1.37 Mb
redis       | 2025-04-14 12:24:19.467 | 1:M 14 Apr 2025 15:24:19.467 * Done loading RDB, keys loaded: 3, keys expired: 0.
redis       | 2025-04-14 12:24:19.467 | 1:M 14 Apr 2025 15:24:19.467 * DB loaded from disk: 0.000 seconds
redis       | 2025-04-14 12:24:19.467 | 1:M 14 Apr 2025 15:24:19.467 * Ready to accept connections tcp
web         | 2025-04-14 12:24:19.540 | wait-for-it.sh: waiting 120 seconds for db:3306
celery      | 2025-04-14 12:24:19.645 | wait-for-it.sh: waiting 120 seconds for db:3306
birt        | 2025-04-14 12:24:19.736 | 14-Apr-2025 15:24:19.733 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Server version name:   Apache Tomcat/9.0.102
birt        | 2025-04-14 12:24:19.736 | 14-Apr-2025 15:24:19.736 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Server built:          Mar 3 2025 19:33:14 UTC
birt        | 2025-04-14 12:24:19.736 | 14-Apr-2025 15:24:19.736 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Server version number: 9.0.102.0
birt        | 2025-04-14 12:24:19.736 | 14-Apr-2025 15:24:19.736 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log OS Name:               Linux
birt        | 2025-04-14 12:24:19.736 | 14-Apr-2025 15:24:19.736 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log OS Version:            5.15.167.4-microsoft-standard-WSL2
birt        | 2025-04-14 12:24:19.736 | 14-Apr-2025 15:24:19.736 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Architecture:          amd64
birt        | 2025-04-14 12:24:19.736 | 14-Apr-2025 15:24:19.736 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Java Home:             /opt/java/openjdk
birt        | 2025-04-14 12:24:19.736 | 14-Apr-2025 15:24:19.736 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log JVM Version:           21.0.6+7-LTS
birt        | 2025-04-14 12:24:19.736 | 14-Apr-2025 15:24:19.736 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log JVM Vendor:            Eclipse Adoptium
birt        | 2025-04-14 12:24:19.736 | 14-Apr-2025 15:24:19.736 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log CATALINA_BASE:         /usr/local/tomcat
birt        | 2025-04-14 12:24:19.736 | 14-Apr-2025 15:24:19.736 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log CATALINA_HOME:         /usr/local/tomcat
birt        | 2025-04-14 12:24:19.741 | 14-Apr-2025 15:24:19.741 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.lang=ALL-UNNAMED
birt        | 2025-04-14 12:24:19.741 | 14-Apr-2025 15:24:19.741 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.lang.invoke=ALL-UNNAMED
birt        | 2025-04-14 12:24:19.741 | 14-Apr-2025 15:24:19.741 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.lang.reflect=ALL-UNNAMED
birt        | 2025-04-14 12:24:19.741 | 14-Apr-2025 15:24:19.741 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.io=ALL-UNNAMED
birt        | 2025-04-14 12:24:19.741 | 14-Apr-2025 15:24:19.741 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.util=ALL-UNNAMED
birt        | 2025-04-14 12:24:19.741 | 14-Apr-2025 15:24:19.741 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.util.concurrent=ALL-UNNAMED
birt        | 2025-04-14 12:24:19.741 | 14-Apr-2025 15:24:19.741 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.rmi/sun.rmi.transport=ALL-UNNAMED
birt        | 2025-04-14 12:24:19.742 | 14-Apr-2025 15:24:19.741 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.util.logging.config.file=/usr/local/tomcat/conf/logging.properties
birt        | 2025-04-14 12:24:19.742 | 14-Apr-2025 15:24:19.741 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager
birt        | 2025-04-14 12:24:19.742 | 14-Apr-2025 15:24:19.742 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.awt.headless=true
birt        | 2025-04-14 12:24:19.742 | 14-Apr-2025 15:24:19.742 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djdk.tls.ephemeralDHKeySize=2048
birt        | 2025-04-14 12:24:19.742 | 14-Apr-2025 15:24:19.742 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.protocol.handler.pkgs=org.apache.catalina.webresources
birt        | 2025-04-14 12:24:19.742 | 14-Apr-2025 15:24:19.742 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dsun.io.useCanonCaches=false
birt        | 2025-04-14 12:24:19.742 | 14-Apr-2025 15:24:19.742 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dorg.apache.catalina.security.SecurityListener.UMASK=0027
birt        | 2025-04-14 12:24:19.742 | 14-Apr-2025 15:24:19.742 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dignore.endorsed.dirs=
birt        | 2025-04-14 12:24:19.742 | 14-Apr-2025 15:24:19.742 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dcatalina.base=/usr/local/tomcat
birt        | 2025-04-14 12:24:19.742 | 14-Apr-2025 15:24:19.742 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dcatalina.home=/usr/local/tomcat
birt        | 2025-04-14 12:24:19.742 | 14-Apr-2025 15:24:19.742 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.io.tmpdir=/usr/local/tomcat/temp
birt        | 2025-04-14 12:24:19.744 | 14-Apr-2025 15:24:19.744 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent Loaded Apache Tomcat Native library [1.3.1] using APR version [1.7.2].
birt        | 2025-04-14 12:24:19.745 | 14-Apr-2025 15:24:19.744 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent APR capabilities: IPv6 [true], sendfile [true], accept filters [false], random [true], UDS [true].
birt        | 2025-04-14 12:24:19.745 | 14-Apr-2025 15:24:19.744 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent APR/OpenSSL configuration: useAprConnector [false], useOpenSSL [true]
birt        | 2025-04-14 12:24:19.748 | 14-Apr-2025 15:24:19.748 INFO [main] org.apache.catalina.core.AprLifecycleListener.initializeSSL OpenSSL successfully initialized [OpenSSL 3.0.13 30 Jan 2024]
db          | 2025-04-14 12:24:19.958 | 2025-04-14T15:24:19.958010Z 0 [System] [MY-010910] [Server] /usr/sbin/mysqld: Shutdown complete (mysqld 8.4.0)  MySQL Community Server - GPL.
db          | 2025-04-14 12:24:19.958 | 2025-04-14T15:24:19.958038Z 0 [System] [MY-015016] [Server] MySQL Server - end.
birt        | 2025-04-14 12:24:20.003 | 14-Apr-2025 15:24:20.003 INFO [main] org.apache.coyote.AbstractProtocol.init Initializing ProtocolHandler ["http-nio-8080"]
birt        | 2025-04-14 12:24:20.015 | 14-Apr-2025 15:24:20.015 INFO [main] org.apache.catalina.startup.Catalina.load Server initialization in [436] milliseconds
birt        | 2025-04-14 12:24:20.042 | 14-Apr-2025 15:24:20.042 INFO [main] org.apache.catalina.core.StandardService.startInternal Starting service [Catalina]
birt        | 2025-04-14 12:24:20.042 | 14-Apr-2025 15:24:20.042 INFO [main] org.apache.catalina.core.StandardEngine.startInternal Starting Servlet engine: [Apache Tomcat/9.0.102]
birt        | 2025-04-14 12:24:20.060 | 14-Apr-2025 15:24:20.060 INFO [main] org.apache.catalina.startup.HostConfig.deployWAR Deploying web application archive [/usr/local/tomcat/webapps/birt.war]
birt        | 2025-04-14 12:24:20.622 | 14-Apr-2025 15:24:20.622 INFO [main] org.apache.jasper.servlet.TldScanner.scanJars At least one JAR was scanned for TLDs yet contained no TLDs. Enable debug logging for this logger for a complete list of JARs that were scanned but no TLDs were found in them. Skipping unneeded JARs during scanning can improve startup time and JSP compilation time.
birt        | 2025-04-14 12:24:20.718 | 14-Apr-2025 15:24:20.718 INFO [main] org.apache.catalina.startup.HostConfig.deployWAR Deployment of web application archive [/usr/local/tomcat/webapps/birt.war] has finished in [658] ms
birt        | 2025-04-14 12:24:20.721 | 14-Apr-2025 15:24:20.721 INFO [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["http-nio-8080"]
birt        | 2025-04-14 12:24:20.728 | 14-Apr-2025 15:24:20.728 INFO [main] org.apache.catalina.startup.Catalina.start Server startup in [711] milliseconds
db          | 2025-04-14 12:24:20.732 | 2025-04-14 15:24:20+00:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 8.4.0-1.el9 started.
db          | 2025-04-14 12:24:21.036 | 2025-04-14 15:24:21+00:00 [Note] [Entrypoint]: Switching to dedicated user 'mysql'
db          | 2025-04-14 12:24:21.040 | 2025-04-14 15:24:21+00:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 8.4.0-1.el9 started.
db          | 2025-04-14 12:24:21.197 | '/var/lib/mysql/mysql.sock' -> '/var/run/mysqld/mysqld.sock'
db          | 2025-04-14 12:24:21.390 | 2025-04-14T15:24:21.206854Z 0 [System] [MY-015015] [Server] MySQL Server - start.
db          | 2025-04-14 12:24:21.390 | 2025-04-14T15:24:21.387533Z 0 [System] [MY-010116] [Server] /usr/sbin/mysqld (mysqld 8.4.0) starting as process 1
db          | 2025-04-14 12:24:21.390 | 2025-04-14T15:24:21.389900Z 0 [Warning] [MY-010159] [Server] Setting lower_case_table_names=2 because file system for /var/lib/mysql/ is case insensitive
db          | 2025-04-14 12:24:21.398 | 2025-04-14T15:24:21.398499Z 1 [System] [MY-013576] [InnoDB] InnoDB initialization has started.
db          | 2025-04-14 12:24:21.948 | 2025-04-14T15:24:21.947880Z 1 [System] [MY-013577] [InnoDB] InnoDB initialization has ended.
db          | 2025-04-14 12:24:22.312 | 2025-04-14T15:24:22.311881Z 0 [Warning] [MY-010068] [Server] CA certificate ca.pem is self signed.
db          | 2025-04-14 12:24:22.312 | 2025-04-14T15:24:22.312265Z 0 [System] [MY-013602] [Server] Channel mysql_main configured to support TLS. Encrypted connections are now supported for this channel.
db          | 2025-04-14 12:24:22.323 | 2025-04-14T15:24:22.323110Z 0 [Warning] [MY-011810] [Server] Insecure configuration for --pid-file: Location '/var/run/mysqld' in the path is accessible to all OS users. Consider choosing a different directory.
db          | 2025-04-14 12:24:22.351 | 2025-04-14T15:24:22.350927Z 0 [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections. Version: '8.4.0'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server - GPL.
nginx       | 2025-04-14 12:24:22.372 | 2025/04/14 15:24:19 [emerg] 1#1: host not found in upstream "web" in /etc/nginx/nginx.conf:39
nginx       | 2025-04-14 12:24:22.372 | nginx: [emerg] host not found in upstream "web" in /etc/nginx/nginx.conf:39
db          | 2025-04-14 12:24:22.606 | 2025-04-14T15:24:22.606236Z 0 [System] [MY-011323] [Server] X Plugin ready for connections. Bind-address: '::' port: 33060, socket: /var/run/mysqld/mysqlx.sock
celery      | 2025-04-14 12:24:22.669 | wait-for-it.sh: db:3306 is available after 3 seconds
nginx       | 2025-04-14 12:24:22.954 | /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
nginx       | 2025-04-14 12:24:22.954 | /docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
nginx       | 2025-04-14 12:24:22.955 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
nginx       | 2025-04-14 12:24:22.957 | 10-listen-on-ipv6-by-default.sh: info: IPv6 listen already enabled
nginx       | 2025-04-14 12:24:22.957 | /docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
nginx       | 2025-04-14 12:24:22.957 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
nginx       | 2025-04-14 12:24:22.959 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
nginx       | 2025-04-14 12:24:22.961 | /docker-entrypoint.sh: Configuration complete; ready for start up
celery-beat | 2025-04-14 12:24:22.973 | wait-for-it.sh: db:3306 is available after 4 seconds
celery      | 2025-04-14 12:24:23.662 |  
celery      | 2025-04-14 12:24:23.662 |  -------------- celery@c0d08e9bd461 v5.4.0 (opalescent)
celery      | 2025-04-14 12:24:23.662 | --- ***** ----- 
celery      | 2025-04-14 12:24:23.662 | -- ******* ---- Linux-5.15.167.4-microsoft-standard-WSL2-x86_64-with-glibc2.36 2025-04-14 12:24:23
celery      | 2025-04-14 12:24:23.662 | - *** --- * --- 
celery      | 2025-04-14 12:24:23.662 | - ** ---------- [config]
celery      | 2025-04-14 12:24:23.662 | - ** ---------- .> app:         mantenedor:0x7f702b58f450
celery      | 2025-04-14 12:24:23.662 | - ** ---------- .> transport:   redis://redis:6379/5
celery      | 2025-04-14 12:24:23.662 | - ** ---------- .> results:     disabled://
celery      | 2025-04-14 12:24:23.662 | - *** --- * --- .> concurrency: 6 (prefork)
celery      | 2025-04-14 12:24:23.662 | -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
celery      | 2025-04-14 12:24:23.662 | --- ***** ----- 
celery      | 2025-04-14 12:24:23.662 |  -------------- [queues]
celery      | 2025-04-14 12:24:23.662 |                 .> celery           exchange=celery(direct) key=celery
celery      | 2025-04-14 12:24:23.662 |                 
celery      | 2025-04-14 12:24:23.662 | 
celery      | 2025-04-14 12:24:23.662 | [tasks]
celery      | 2025-04-14 12:24:23.662 |   . apps.reloj_fichador.tasks.crear_asistencia_prueba
celery      | 2025-04-14 12:24:23.662 |   . apps.reloj_fichador.tasks.generar_registros_asistencia
celery      | 2025-04-14 12:24:23.662 |   . apps.reloj_fichador.tasks.prueba_tarea
celery      | 2025-04-14 12:24:23.662 |   . mantenedor.celery.debug_task
celery      | 2025-04-14 12:24:23.662 | 
celery      | 2025-04-14 12:24:24.006 | [2025-04-14 12:24:24,005: INFO/MainProcess] Connected to redis://redis:6379/5
celery      | 2025-04-14 12:24:24.008 | [2025-04-14 12:24:24,008: INFO/MainProcess] mingle: searching for neighbors
celery-beat | 2025-04-14 12:24:24.174 | Operations to perform:
celery-beat | 2025-04-14 12:24:24.174 |   Apply all migrations: admin, admin_interface, auth, contenttypes, django_celery_beat, django_celery_results, reloj_fichador, sessions
celery-beat | 2025-04-14 12:24:24.174 | Running migrations:
celery-beat | 2025-04-14 12:24:24.174 |   No migrations to apply.
web         | 2025-04-14 12:24:24.547 | wait-for-it.sh: db:3306 is available after 5 seconds
celery      | 2025-04-14 12:24:25.014 | [2025-04-14 12:24:25,013: INFO/MainProcess] mingle: all alone
celery      | 2025-04-14 12:24:25.021 | [2025-04-14 12:24:25,020: INFO/MainProcess] celery@c0d08e9bd461 ready.
celery-beat | 2025-04-14 12:24:25.231 | [2025-04-14 12:24:25,231: INFO/MainProcess] beat: Starting...
celery-beat | 2025-04-14 12:24:25.276 | [2025-04-14 12:24:25,276: INFO/MainProcess] DatabaseScheduler: Schedule changed.
web         | 2025-04-14 12:24:25.679 | Operations to perform:
web         | 2025-04-14 12:24:25.679 |   Apply all migrations: admin, admin_interface, auth, contenttypes, django_celery_beat, django_celery_results, reloj_fichador, sessions
web         | 2025-04-14 12:24:25.679 | Running migrations:
web         | 2025-04-14 12:24:25.679 |   No migrations to apply.
web         | 2025-04-14 12:24:26.642 | Found another file with the destination path 'admin/js/cancel.js'. It will be ignored since only the first encountered file is collected. If this is not what you want, make sure every static file has a unique path.
web         | 2025-04-14 12:24:26.643 | Found another file with the destination path 'admin/js/popup_response.js'. It will be ignored since only the first encountered file is collected. If this is not what you want, make sure every static file has a unique path.
web         | 2025-04-14 12:24:26.643 | 
web         | 2025-04-14 12:24:26.643 | 0 static files copied to '/app/staticfiles', 225 unmodified.
web         | 2025-04-14 12:24:26.838 | [2025-04-14 15:24:26 +0000] [1] [INFO] Starting gunicorn 23.0.0
web         | 2025-04-14 12:24:26.838 | [2025-04-14 15:24:26 +0000] [1] [INFO] Listening at: http://0.0.0.0:58000 (1)
web         | 2025-04-14 12:24:26.838 | [2025-04-14 15:24:26 +0000] [1] [INFO] Using worker: sync
web         | 2025-04-14 12:24:26.840 | [2025-04-14 15:24:26 +0000] [79] [INFO] Booting worker with pid: 79
web         | 2025-04-14 12:24:26.919 | [2025-04-14 15:24:26 +0000] [80] [INFO] Booting worker with pid: 80
web         | 2025-04-14 12:24:26.996 | [2025-04-14 15:24:26 +0000] [81] [INFO] Booting worker with pid: 81
backup      | 2025-04-14 12:24:27.786 | wait-for-it.sh: waiting 120 seconds for db:3306
backup      | 2025-04-14 12:24:27.790 | wait-for-it.sh: db:3306 is available after 0 seconds
backup      | 2025-04-14 12:24:27.793 | mysqldump: [Warning] Using a password on the command line interface can be insecure.
backup      | 2025-04-14 12:24:28.052 | Limpiando backups antiguos...
backup      | 2025-04-14 12:24:28.063 | Limpieza completada. Se mantienen los 10 backups más recientes.
nginx       | 2025-04-14 12:39:09.887 | 172.18.0.1 - - [14/Apr/2025:15:39:09 +0000] "GET / HTTP/1.1" 200 17241 "-" "Mozilla/5.0 (compatible; InternetMeasurement/1.0; +https://internet-measurement.com/)"
backup      | 2025-04-14 12:57:48.197 | wait-for-it.sh: waiting 120 seconds for db:3306
backup      | 2025-04-14 12:57:48.200 | wait-for-it.sh: db:3306 is available after 0 seconds
backup      | 2025-04-14 12:57:48.204 | mysqldump: [Warning] Using a password on the command line interface can be insecure.
backup      | 2025-04-14 12:57:48.359 | Limpiando backups antiguos...
backup      | 2025-04-14 12:57:48.369 | Limpieza completada. Se mantienen los 10 backups más recientes.
redis       | 2025-04-14 13:24:20.078 | 1:M 14 Apr 2025 16:24:20.078 * 1 changes in 3600 seconds. Saving...
redis       | 2025-04-14 13:24:20.079 | 1:M 14 Apr 2025 16:24:20.079 * Background saving started by pid 3943
redis       | 2025-04-14 13:24:20.082 | 3943:C 14 Apr 2025 16:24:20.082 * DB saved on disk
redis       | 2025-04-14 13:24:20.082 | 3943:C 14 Apr 2025 16:24:20.082 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
redis       | 2025-04-14 13:24:20.179 | 1:M 14 Apr 2025 16:24:20.179 * Background saving terminated with success
backup      | 2025-04-14 13:30:01.733 | wait-for-it.sh: waiting 120 seconds for db:3306
backup      | 2025-04-14 13:30:01.735 | wait-for-it.sh: db:3306 is available after 0 seconds
backup      | 2025-04-14 13:30:01.738 | mysqldump: [Warning] Using a password on the command line interface can be insecure.
backup      | 2025-04-14 13:30:01.895 | Limpiando backups antiguos...
backup      | 2025-04-14 13:30:01.904 | Limpieza completada. Se mantienen los 10 backups más recientes.
backup      | 2025-04-14 14:00:05.252 | wait-for-it.sh: waiting 120 seconds for db:3306
backup      | 2025-04-14 14:00:05.255 | wait-for-it.sh: db:3306 is available after 0 seconds
backup      | 2025-04-14 14:00:05.258 | mysqldump: [Warning] Using a password on the command line interface can be insecure.
backup      | 2025-04-14 14:00:05.414 | Limpiando backups antiguos...
backup      | 2025-04-14 14:00:05.423 | Limpieza completada. Se mantienen los 10 backups más recientes.
nginx       | 2025-04-14 14:03:01.364 | 172.18.0.1 - - [14/Apr/2025:17:03:01 +0000] "\x16\x03\x01\x00\x8C\x01\x00\x00\x88\x03\x03$H\x1BE\xF4\xE7\xBB\xD0\xDA\xCD\xD4\xE8-\xC8\xA1F\xD2\xFB\xA1g\x8F\xB4\xFB\x84$\x9A\x08\xDBT\xA3\xFA\x00\x00\x00\x1A\xC0/\xC0+\xC0\x11\xC0\x07\xC0\x13\xC0\x09\xC0\x14\xC0" 400 157 "-" "-"
nginx       | 2025-04-14 14:23:53.580 | 172.18.0.1 - - [14/Apr/2025:17:23:53 +0000] "GET / HTTP/1.1" 200 17241 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
redis       | 2025-04-14 14:24:21.032 | 1:M 14 Apr 2025 17:24:21.031 * 1 changes in 3600 seconds. Saving...
redis       | 2025-04-14 14:24:21.032 | 1:M 14 Apr 2025 17:24:21.032 * Background saving started by pid 8245
redis       | 2025-04-14 14:24:21.036 | 8245:C 14 Apr 2025 17:24:21.035 * DB saved on disk
redis       | 2025-04-14 14:24:21.036 | 8245:C 14 Apr 2025 17:24:21.036 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
redis       | 2025-04-14 14:24:21.133 | 1:M 14 Apr 2025 17:24:21.132 * Background saving terminated with success
backup      | 2025-04-14 14:30:08.768 | wait-for-it.sh: waiting 120 seconds for db:3306
backup      | 2025-04-14 14:30:08.772 | wait-for-it.sh: db:3306 is available after 0 seconds
backup      | 2025-04-14 14:30:08.775 | mysqldump: [Warning] Using a password on the command line interface can be insecure.
backup      | 2025-04-14 14:30:08.933 | Limpiando backups antiguos...
backup      | 2025-04-14 14:30:08.943 | Limpieza completada. Se mantienen los 10 backups más recientes.
nginx       | 2025-04-14 14:39:14.827 | /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
nginx       | 2025-04-14 14:39:14.827 | /docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
nginx       | 2025-04-14 14:39:14.828 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
nginx       | 2025-04-14 14:39:14.829 | 10-listen-on-ipv6-by-default.sh: info: IPv6 listen already enabled
nginx       | 2025-04-14 14:39:14.830 | /docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
nginx       | 2025-04-14 14:39:14.830 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
nginx       | 2025-04-14 14:39:14.832 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
nginx       | 2025-04-14 14:39:14.833 | /docker-entrypoint.sh: Configuration complete; ready for start up
backup      | 2025-04-14 15:00:14.128 | wait-for-it.sh: waiting 120 seconds for db:3306
backup      | 2025-04-14 15:00:14.131 | wait-for-it.sh: db:3306 is available after 0 seconds
backup      | 2025-04-14 15:00:14.134 | mysqldump: [Warning] Using a password on the command line interface can be insecure.
backup      | 2025-04-14 15:00:14.433 | Limpiando backups antiguos...
backup      | 2025-04-14 15:00:14.445 | Limpieza completada. Se mantienen los 10 backups más recientes.
nginx       | 2025-04-14 15:02:32.966 | 172.18.0.1 - - [14/Apr/2025:18:02:32 +0000] "GET /admin/reloj_fichador/registrodiario/1015/change/ HTTP/1.1" 302 0 "-" "-"
nginx       | 2025-04-14 15:02:32.968 | 172.18.0.1 - - [14/Apr/2025:18:02:32 +0000] "GET /admin/ HTTP/1.1" 302 0 "-" "-"
nginx       | 2025-04-14 15:02:32.979 | 172.18.0.1 - - [14/Apr/2025:18:02:32 +0000] "GET /admin HTTP/1.1" 301 5 "-" "-"
nginx       | 2025-04-14 15:02:33.008 | 172.18.0.1 - - [14/Apr/2025:18:02:33 +0000] "GET /admin/login/?next=/admin/reloj_fichador/registrodiario/1015/change/ HTTP/1.1" 200 17387 "-" "-"
nginx       | 2025-04-14 15:02:33.010 | 172.18.0.1 - - [14/Apr/2025:18:02:33 +0000] "GET /admin/ HTTP/1.1" 302 0 "-" "-"
nginx       | 2025-04-14 15:02:33.028 | 172.18.0.1 - - [14/Apr/2025:18:02:33 +0000] "GET /admin/login/?next=/admin/ HTTP/1.1" 200 17303 "-" "-"
nginx       | 2025-04-14 15:02:33.083 | 172.18.0.1 - - [14/Apr/2025:18:02:33 +0000] "GET /admin/login/?next=/admin/ HTTP/1.1" 200 17303 "-" "-"
nginx       | 2025-04-14 15:02:33.091 | 172.18.0.1 - - [14/Apr/2025:18:02:33 +0000] "GET /admin/login/?next=/admin/ HTTP/1.1" 200 17303 "-" "-"
nginx       | 2025-04-14 15:02:33.941 | 172.18.0.1 - - [14/Apr/2025:18:02:33 +0000] "GET /admin/reloj_fichador/registrodiario/1015/change/ HTTP/1.1" 302 0 "-" "-"
nginx       | 2025-04-14 15:02:33.941 | 172.18.0.1 - - [14/Apr/2025:18:02:33 +0000] "GET /admin/ HTTP/1.1" 302 0 "-" "-"
nginx       | 2025-04-14 15:02:33.944 | 172.18.0.1 - - [14/Apr/2025:18:02:33 +0000] "GET /admin HTTP/1.1" 301 5 "-" "-"
nginx       | 2025-04-14 15:02:33.952 | 172.18.0.1 - - [14/Apr/2025:18:02:33 +0000] "GET /admin/login/?next=/admin/ HTTP/1.1" 200 17303 "-" "-"
nginx       | 2025-04-14 15:02:33.953 | 172.18.0.1 - - [14/Apr/2025:18:02:33 +0000] "GET /admin/ HTTP/1.1" 302 0 "-" "-"
nginx       | 2025-04-14 15:02:33.953 | 172.18.0.1 - - [14/Apr/2025:18:02:33 +0000] "GET /admin/login/?next=/admin/ HTTP/1.1" 200 17303 "-" "-"
nginx       | 2025-04-14 15:02:33.957 | 172.18.0.1 - - [14/Apr/2025:18:02:33 +0000] "GET /admin/login/?next=/admin/reloj_fichador/registrodiario/1015/change/ HTTP/1.1" 200 17387 "-" "-"
nginx       | 2025-04-14 15:02:33.964 | 172.18.0.1 - - [14/Apr/2025:18:02:33 +0000] "GET /admin/login/?next=/admin/ HTTP/1.1" 200 17303 "-" "-"
nginx       | 2025-04-14 15:11:16.980 | 172.18.0.1 - - [14/Apr/2025:18:11:16 +0000] "GET / HTTP/1.1" 200 17241 "-" "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0"
nginx       | 2025-04-14 15:11:17.105 | 172.18.0.1 - - [14/Apr/2025:18:11:17 +0000] "GET /?keep_alive=1744654218450 HTTP/1.1" 200 17241 "http://192.168.10.11:5080/" "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0"
nginx       | 2025-04-14 15:11:17.106 | 172.18.0.1 - - [14/Apr/2025:18:11:17 +0000] "GET /?keep_alive=1744654218452 HTTP/1.1" 200 17241 "http://192.168.10.11:5080/" "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0"
nginx       | 2025-04-14 15:11:18.536 | 172.18.0.1 - - [14/Apr/2025:18:11:18 +0000] "GET / HTTP/1.1" 200 17241 "-" "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0"
nginx       | 2025-04-14 15:11:18.568 | 172.18.0.1 - - [14/Apr/2025:18:11:18 +0000] "GET /static/css/styles.css HTTP/1.1" 200 7633 "http://192.168.10.11:5080/" "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0"
nginx       | 2025-04-14 15:11:18.699 | 172.18.0.1 - - [14/Apr/2025:18:11:18 +0000] "GET /static/images/login-background1.jpg HTTP/1.1" 200 6345054 "http://192.168.10.11:5080/static/css/styles.css" "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0"
nginx       | 2025-04-14 15:11:18.707 | 172.18.0.1 - - [14/Apr/2025:18:11:18 +0000] "GET /?keep_alive=1744654220082 HTTP/1.1" 200 17241 "http://192.168.10.11:5080/" "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0"
nginx       | 2025-04-14 15:11:18.709 | 172.18.0.1 - - [14/Apr/2025:18:11:18 +0000] "GET /?keep_alive=1744654220084 HTTP/1.1" 200 17241 "http://192.168.10.11:5080/" "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0"
web         | 2025-04-14 15:11:24.988 | Forbidden (CSRF cookie not set.): /registrar/entrada/
nginx       | 2025-04-14 15:11:24.989 | 172.18.0.1 - - [14/Apr/2025:18:11:24 +0000] "POST /registrar/entrada/ HTTP/1.1" 403 2970 "http://192.168.10.11:5080/" "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0"
web         | 2025-04-14 15:11:30.352 | Forbidden (CSRF cookie not set.): /registrar/salida_transitoria/
nginx       | 2025-04-14 15:11:30.352 | 172.18.0.1 - - [14/Apr/2025:18:11:30 +0000] "POST /registrar/salida_transitoria/ HTTP/1.1" 403 2970 "http://192.168.10.11:5080/" "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0"
web         | 2025-04-14 15:11:32.212 | Forbidden (CSRF cookie not set.): /registrar/entrada_transitoria/
nginx       | 2025-04-14 15:11:32.212 | 172.18.0.1 - - [14/Apr/2025:18:11:32 +0000] "POST /registrar/entrada_transitoria/ HTTP/1.1" 403 2970 "http://192.168.10.11:5080/" "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0"
web         | 2025-04-14 15:11:32.987 | Forbidden (CSRF cookie not set.): /registrar/entrada_transitoria/
nginx       | 2025-04-14 15:11:32.988 | 172.18.0.1 - - [14/Apr/2025:18:11:32 +0000] "POST /registrar/entrada_transitoria/ HTTP/1.1" 403 2970 "http://192.168.10.11:5080/" "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0"
web         | 2025-04-14 15:11:34.167 | Forbidden (CSRF cookie not set.): /registrar/salida/
nginx       | 2025-04-14 15:11:34.167 | 172.18.0.1 - - [14/Apr/2025:18:11:34 +0000] "POST /registrar/salida/ HTTP/1.1" 403 2970 "http://192.168.10.11:5080/" "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0"
web         | 2025-04-14 15:11:36.151 | Forbidden (CSRF cookie not set.): /registrar/salida/
nginx       | 2025-04-14 15:11:36.151 | 172.18.0.1 - - [14/Apr/2025:18:11:36 +0000] "POST /registrar/salida/ HTTP/1.1" 403 2970 "http://192.168.10.11:5080/" "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0"
web         | 2025-04-14 15:11:37.913 | Forbidden (CSRF cookie not set.): /registrar/entrada/
nginx       | 2025-04-14 15:11:37.913 | 172.18.0.1 - - [14/Apr/2025:18:11:37 +0000] "POST /registrar/entrada/ HTTP/1.1" 403 2970 "http://192.168.10.11:5080/" "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0"
web         | 2025-04-14 15:11:38.555 | Forbidden (CSRF cookie not set.): /registrar/entrada/
nginx       | 2025-04-14 15:11:38.555 | 172.18.0.1 - - [14/Apr/2025:18:11:38 +0000] "POST /registrar/entrada/ HTTP/1.1" 403 2970 "http://192.168.10.11:5080/" "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0"
nginx       | 2025-04-14 15:11:46.135 | 172.18.0.1 - - [14/Apr/2025:18:11:46 +0000] "GET / HTTP/1.1" 200 17241 "-" "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0"
nginx       | 2025-04-14 15:11:46.158 | 172.18.0.1 - - [14/Apr/2025:18:11:46 +0000] "GET /static/css/styles.css HTTP/1.1" 200 7633 "http://192.168.10.11:5080/" "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0"
nginx       | 2025-04-14 15:11:46.263 | 172.18.0.1 - - [14/Apr/2025:18:11:46 +0000] "GET /static/images/login-background1.jpg HTTP/1.1" 200 6345054 "http://192.168.10.11:5080/static/css/styles.css" "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0"
nginx       | 2025-04-14 15:11:46.295 | 172.18.0.1 - - [14/Apr/2025:18:11:46 +0000] "GET /?keep_alive=1744654247658 HTTP/1.1" 200 17241 "http://192.168.10.11:5080/" "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0"
nginx       | 2025-04-14 15:11:50.273 | 172.18.0.1 - - [14/Apr/2025:18:11:50 +0000] "GET /?keep_alive=1744654251692 HTTP/1.1" 200 17241 "http://192.168.10.11:5080/" "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0"
web         | 2025-04-14 15:11:53.002 | Forbidden (CSRF cookie not set.): /registrar/entrada/
nginx       | 2025-04-14 15:11:53.002 | 172.18.0.1 - - [14/Apr/2025:18:11:53 +0000] "POST /registrar/entrada/ HTTP/1.1" 403 2970 "http://192.168.10.11:5080/" "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0"
nginx       | 2025-04-14 15:12:05.784 | 172.18.0.1 - - [14/Apr/2025:18:12:05 +0000] "GET /?keep_alive=1744654267026 HTTP/1.1" 200 17241 "http://192.168.10.11:5080/" "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0"
nginx       | 2025-04-14 15:12:05.785 | 172.18.0.1 - - [14/Apr/2025:18:12:05 +0000] "GET /?keep_alive=1744654267050 HTTP/1.1" 200 17241 "http://192.168.10.11:5080/" "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0"
redis       | 2025-04-14 15:24:22.046 | 1:M 14 Apr 2025 18:24:22.046 * 1 changes in 3600 seconds. Saving...
redis       | 2025-04-14 15:24:22.046 | 1:M 14 Apr 2025 18:24:22.046 * Background saving started by pid 12547
redis       | 2025-04-14 15:24:22.049 | 12547:C 14 Apr 2025 18:24:22.049 * DB saved on disk
redis       | 2025-04-14 15:24:22.049 | 12547:C 14 Apr 2025 18:24:22.049 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
redis       | 2025-04-14 15:24:22.147 | 1:M 14 Apr 2025 18:24:22.146 * Background saving terminated with success