redis       | 2025-04-10 08:52:40.132 | 1:C 10 Apr 2025 11:52:40.131 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
redis       | 2025-04-10 08:52:40.132 | 1:C 10 Apr 2025 11:52:40.132 * Redis version=7.4.2, bits=64, commit=00000000, modified=0, pid=1, just started
redis       | 2025-04-10 08:52:40.132 | 1:C 10 Apr 2025 11:52:40.132 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
redis       | 2025-04-10 08:52:40.132 | 1:M 10 Apr 2025 11:52:40.132 * monotonic clock: POSIX clock_gettime
redis       | 2025-04-10 08:52:40.133 | 1:M 10 Apr 2025 11:52:40.133 * Running mode=standalone, port=6379.
redis       | 2025-04-10 08:52:40.133 | 1:M 10 Apr 2025 11:52:40.133 * Server initialized
redis       | 2025-04-10 08:52:40.133 | 1:M 10 Apr 2025 11:52:40.133 * Ready to accept connections tcp
db          | 2025-04-10 08:52:40.157 | 2025-04-10 11:52:40+00:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 8.4.0-1.el9 started.
web         | 2025-04-10 08:52:40.353 | wait-for-it.sh: waiting 15 seconds for db:3306
celery      | 2025-04-10 08:52:40.408 | wait-for-it.sh: waiting 15 seconds for db:3306
birt        | 2025-04-10 08:52:40.513 | NOTE: Picked up JDK_JAVA_OPTIONS:  --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.rmi/sun.rmi.transport=ALL-UNNAMED
backup      | 2025-04-10 08:52:40.525 | wait-for-it.sh: waiting 15 seconds for db:3306
celery-beat | 2025-04-10 08:52:40.604 | wait-for-it.sh: waiting 15 seconds for db:3306
db          | 2025-04-10 08:52:40.610 | 2025-04-10 11:52:40+00:00 [Note] [Entrypoint]: Switching to dedicated user 'mysql'
db          | 2025-04-10 08:52:40.615 | 2025-04-10 11:52:40+00:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 8.4.0-1.el9 started.
nginx       | 2025-04-10 08:52:40.686 | /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
nginx       | 2025-04-10 08:52:40.686 | /docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
nginx       | 2025-04-10 08:52:40.686 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
nginx       | 2025-04-10 08:52:40.692 | 10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
nginx       | 2025-04-10 08:52:40.699 | 10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
nginx       | 2025-04-10 08:52:40.700 | /docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
nginx       | 2025-04-10 08:52:40.700 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
nginx       | 2025-04-10 08:52:40.704 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
nginx       | 2025-04-10 08:52:40.706 | /docker-entrypoint.sh: Configuration complete; ready for start up
db          | 2025-04-10 08:52:40.824 | '/var/lib/mysql/mysql.sock' -> '/var/run/mysqld/mysqld.sock'
birt        | 2025-04-10 08:52:40.857 | 10-Apr-2025 11:52:40.854 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Server version name:   Apache Tomcat/9.0.102
birt        | 2025-04-10 08:52:40.858 | 10-Apr-2025 11:52:40.857 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Server built:          Mar 3 2025 19:33:14 UTC
birt        | 2025-04-10 08:52:40.858 | 10-Apr-2025 11:52:40.858 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Server version number: 9.0.102.0
birt        | 2025-04-10 08:52:40.858 | 10-Apr-2025 11:52:40.858 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log OS Name:               Linux
birt        | 2025-04-10 08:52:40.858 | 10-Apr-2025 11:52:40.858 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log OS Version:            5.15.167.4-microsoft-standard-WSL2
birt        | 2025-04-10 08:52:40.858 | 10-Apr-2025 11:52:40.858 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Architecture:          amd64
birt        | 2025-04-10 08:52:40.858 | 10-Apr-2025 11:52:40.858 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Java Home:             /opt/java/openjdk
birt        | 2025-04-10 08:52:40.858 | 10-Apr-2025 11:52:40.858 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log JVM Version:           21.0.6+7-LTS
birt        | 2025-04-10 08:52:40.858 | 10-Apr-2025 11:52:40.858 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log JVM Vendor:            Eclipse Adoptium
birt        | 2025-04-10 08:52:40.858 | 10-Apr-2025 11:52:40.858 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log CATALINA_BASE:         /usr/local/tomcat
birt        | 2025-04-10 08:52:40.858 | 10-Apr-2025 11:52:40.858 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log CATALINA_HOME:         /usr/local/tomcat
birt        | 2025-04-10 08:52:40.865 | 10-Apr-2025 11:52:40.864 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.lang=ALL-UNNAMED
birt        | 2025-04-10 08:52:40.865 | 10-Apr-2025 11:52:40.865 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.lang.invoke=ALL-UNNAMED
birt        | 2025-04-10 08:52:40.865 | 10-Apr-2025 11:52:40.865 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.lang.reflect=ALL-UNNAMED
birt        | 2025-04-10 08:52:40.865 | 10-Apr-2025 11:52:40.865 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.io=ALL-UNNAMED
birt        | 2025-04-10 08:52:40.865 | 10-Apr-2025 11:52:40.865 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.util=ALL-UNNAMED
birt        | 2025-04-10 08:52:40.865 | 10-Apr-2025 11:52:40.865 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.util.concurrent=ALL-UNNAMED
birt        | 2025-04-10 08:52:40.865 | 10-Apr-2025 11:52:40.865 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.rmi/sun.rmi.transport=ALL-UNNAMED
birt        | 2025-04-10 08:52:40.866 | 10-Apr-2025 11:52:40.865 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.util.logging.config.file=/usr/local/tomcat/conf/logging.properties
birt        | 2025-04-10 08:52:40.866 | 10-Apr-2025 11:52:40.866 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager
birt        | 2025-04-10 08:52:40.866 | 10-Apr-2025 11:52:40.866 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.awt.headless=true
birt        | 2025-04-10 08:52:40.867 | 10-Apr-2025 11:52:40.866 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djdk.tls.ephemeralDHKeySize=2048
birt        | 2025-04-10 08:52:40.867 | 10-Apr-2025 11:52:40.867 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.protocol.handler.pkgs=org.apache.catalina.webresources
birt        | 2025-04-10 08:52:40.867 | 10-Apr-2025 11:52:40.867 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dsun.io.useCanonCaches=false
birt        | 2025-04-10 08:52:40.867 | 10-Apr-2025 11:52:40.867 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dorg.apache.catalina.security.SecurityListener.UMASK=0027
birt        | 2025-04-10 08:52:40.868 | 10-Apr-2025 11:52:40.867 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dignore.endorsed.dirs=
birt        | 2025-04-10 08:52:40.868 | 10-Apr-2025 11:52:40.868 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dcatalina.base=/usr/local/tomcat
birt        | 2025-04-10 08:52:40.868 | 10-Apr-2025 11:52:40.868 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dcatalina.home=/usr/local/tomcat
birt        | 2025-04-10 08:52:40.868 | 10-Apr-2025 11:52:40.868 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.io.tmpdir=/usr/local/tomcat/temp
birt        | 2025-04-10 08:52:40.872 | 10-Apr-2025 11:52:40.871 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent Loaded Apache Tomcat Native library [1.3.1] using APR version [1.7.2].
birt        | 2025-04-10 08:52:40.872 | 10-Apr-2025 11:52:40.872 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent APR capabilities: IPv6 [true], sendfile [true], accept filters [false], random [true], UDS [true].
birt        | 2025-04-10 08:52:40.872 | 10-Apr-2025 11:52:40.872 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent APR/OpenSSL configuration: useAprConnector [false], useOpenSSL [true]
birt        | 2025-04-10 08:52:40.875 | 10-Apr-2025 11:52:40.875 INFO [main] org.apache.catalina.core.AprLifecycleListener.initializeSSL OpenSSL successfully initialized [OpenSSL 3.0.13 30 Jan 2024]
db          | 2025-04-10 08:52:41.065 | 2025-04-10T11:52:40.835345Z 0 [System] [MY-015015] [Server] MySQL Server - start.
db          | 2025-04-10 08:52:41.065 | 2025-04-10T11:52:41.061869Z 0 [System] [MY-010116] [Server] /usr/sbin/mysqld (mysqld 8.4.0) starting as process 1
db          | 2025-04-10 08:52:41.065 | 2025-04-10T11:52:41.064684Z 0 [Warning] [MY-010159] [Server] Setting lower_case_table_names=2 because file system for /var/lib/mysql/ is case insensitive
db          | 2025-04-10 08:52:41.074 | 2025-04-10T11:52:41.074195Z 1 [System] [MY-013576] [InnoDB] InnoDB initialization has started.
birt        | 2025-04-10 08:52:41.114 | 10-Apr-2025 11:52:41.114 INFO [main] org.apache.coyote.AbstractProtocol.init Initializing ProtocolHandler ["http-nio-8080"]
birt        | 2025-04-10 08:52:41.131 | 10-Apr-2025 11:52:41.131 INFO [main] org.apache.catalina.startup.Catalina.load Server initialization in [419] milliseconds
birt        | 2025-04-10 08:52:41.157 | 10-Apr-2025 11:52:41.157 INFO [main] org.apache.catalina.core.StandardService.startInternal Starting service [Catalina]
birt        | 2025-04-10 08:52:41.157 | 10-Apr-2025 11:52:41.157 INFO [main] org.apache.catalina.core.StandardEngine.startInternal Starting Servlet engine: [Apache Tomcat/9.0.102]
birt        | 2025-04-10 08:52:41.171 | 10-Apr-2025 11:52:41.170 INFO [main] org.apache.catalina.startup.HostConfig.deployWAR Deploying web application archive [/usr/local/tomcat/webapps/birt.war]
birt        | 2025-04-10 08:52:41.750 | 10-Apr-2025 11:52:41.750 INFO [main] org.apache.jasper.servlet.TldScanner.scanJars At least one JAR was scanned for TLDs yet contained no TLDs. Enable debug logging for this logger for a complete list of JARs that were scanned but no TLDs were found in them. Skipping unneeded JARs during scanning can improve startup time and JSP compilation time.
birt        | 2025-04-10 08:52:41.777 | 10-Apr-2025 11:52:41.777 INFO [main] org.apache.catalina.startup.HostConfig.deployWAR Deployment of web application archive [/usr/local/tomcat/webapps/birt.war] has finished in [606] ms
birt        | 2025-04-10 08:52:41.781 | 10-Apr-2025 11:52:41.780 INFO [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["http-nio-8080"]
birt        | 2025-04-10 08:52:41.788 | 10-Apr-2025 11:52:41.788 INFO [main] org.apache.catalina.startup.Catalina.start Server startup in [656] milliseconds
db          | 2025-04-10 08:52:42.317 | 2025-04-10T11:52:42.317595Z 1 [System] [MY-013577] [InnoDB] InnoDB initialization has ended.
db          | 2025-04-10 08:52:42.589 | 2025-04-10T11:52:42.589079Z 0 [System] [MY-010229] [Server] Starting XA crash recovery...
db          | 2025-04-10 08:52:42.596 | 2025-04-10T11:52:42.595882Z 0 [System] [MY-010232] [Server] XA crash recovery finished.
db          | 2025-04-10 08:52:42.701 | 2025-04-10T11:52:42.700791Z 0 [Warning] [MY-010068] [Server] CA certificate ca.pem is self signed.
db          | 2025-04-10 08:52:42.701 | 2025-04-10T11:52:42.700975Z 0 [System] [MY-013602] [Server] Channel mysql_main configured to support TLS. Encrypted connections are now supported for this channel.
db          | 2025-04-10 08:52:42.709 | 2025-04-10T11:52:42.708971Z 0 [Warning] [MY-011810] [Server] Insecure configuration for --pid-file: Location '/var/run/mysqld' in the path is accessible to all OS users. Consider choosing a different directory.
db          | 2025-04-10 08:52:42.725 | 2025-04-10T11:52:42.725274Z 0 [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections. Version: '8.4.0'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server - GPL.
db          | 2025-04-10 08:52:42.980 | 2025-04-10T11:52:42.980805Z 0 [System] [MY-011323] [Server] X Plugin ready for connections. Bind-address: '::' port: 33060, socket: /var/run/mysqld/mysqlx.sock
web         | 2025-04-10 08:52:43.361 | wait-for-it.sh: db:3306 is available after 3 seconds
celery      | 2025-04-10 08:52:43.415 | wait-for-it.sh: db:3306 is available after 3 seconds
backup      | 2025-04-10 08:52:43.533 | wait-for-it.sh: db:3306 is available after 3 seconds
backup      | 2025-04-10 08:52:43.537 | mysqldump: [Warning] Using a password on the command line interface can be insecure.
celery-beat | 2025-04-10 08:52:43.611 | wait-for-it.sh: db:3306 is available after 3 seconds
celery      | 2025-04-10 08:52:44.539 |  
celery      | 2025-04-10 08:52:44.539 |  -------------- celery@336749e752ac v5.4.0 (opalescent)
celery      | 2025-04-10 08:52:44.539 | --- ***** ----- 
celery      | 2025-04-10 08:52:44.539 | -- ******* ---- Linux-5.15.167.4-microsoft-standard-WSL2-x86_64-with-glibc2.36 2025-04-10 08:52:44
celery      | 2025-04-10 08:52:44.539 | - *** --- * --- 
celery      | 2025-04-10 08:52:44.539 | - ** ---------- [config]
celery      | 2025-04-10 08:52:44.539 | - ** ---------- .> app:         mantenedor:0x7fac4f541790
celery      | 2025-04-10 08:52:44.539 | - ** ---------- .> transport:   redis://redis:6379/5
celery      | 2025-04-10 08:52:44.539 | - ** ---------- .> results:     disabled://
celery      | 2025-04-10 08:52:44.539 | - *** --- * --- .> concurrency: 6 (prefork)
celery      | 2025-04-10 08:52:44.539 | -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
celery      | 2025-04-10 08:52:44.539 | --- ***** ----- 
celery      | 2025-04-10 08:52:44.539 |  -------------- [queues]
celery      | 2025-04-10 08:52:44.539 |                 .> celery           exchange=celery(direct) key=celery
celery      | 2025-04-10 08:52:44.539 |                 
celery      | 2025-04-10 08:52:44.539 | 
celery      | 2025-04-10 08:52:44.539 | [tasks]
celery      | 2025-04-10 08:52:44.539 |   . apps.reloj_fichador.tasks.crear_asistencia_prueba
celery      | 2025-04-10 08:52:44.539 |   . apps.reloj_fichador.tasks.generar_registros_asistencia
celery      | 2025-04-10 08:52:44.539 |   . apps.reloj_fichador.tasks.prueba_tarea
celery      | 2025-04-10 08:52:44.539 |   . mantenedor.celery.debug_task
celery      | 2025-04-10 08:52:44.539 | 
web         | 2025-04-10 08:52:44.739 | Operations to perform:
web         | 2025-04-10 08:52:44.739 |   Apply all migrations: admin, admin_interface, auth, contenttypes, django_celery_beat, django_celery_results, reloj_fichador, sessions
web         | 2025-04-10 08:52:44.739 | Running migrations:
web         | 2025-04-10 08:52:44.739 |   No migrations to apply.
celery-beat | 2025-04-10 08:52:44.760 | Operations to perform:
celery-beat | 2025-04-10 08:52:44.760 |   Apply all migrations: admin, admin_interface, auth, contenttypes, django_celery_beat, django_celery_results, reloj_fichador, sessions
celery-beat | 2025-04-10 08:52:44.760 | Running migrations:
celery-beat | 2025-04-10 08:52:44.760 |   No migrations to apply.
celery      | 2025-04-10 08:52:44.920 | [2025-04-10 08:52:44,919: INFO/MainProcess] Connected to redis://redis:6379/5
celery      | 2025-04-10 08:52:44.922 | [2025-04-10 08:52:44,921: INFO/MainProcess] mingle: searching for neighbors
web         | 2025-04-10 08:52:45.836 | Found another file with the destination path 'admin/js/cancel.js'. It will be ignored since only the first encountered file is collected. If this is not what you want, make sure every static file has a unique path.
web         | 2025-04-10 08:52:45.836 | Found another file with the destination path 'admin/js/popup_response.js'. It will be ignored since only the first encountered file is collected. If this is not what you want, make sure every static file has a unique path.
web         | 2025-04-10 08:52:45.836 | 
web         | 2025-04-10 08:52:45.836 | 0 static files copied to '/app/staticfiles', 225 unmodified.
celery      | 2025-04-10 08:52:45.928 | [2025-04-10 08:52:45,928: INFO/MainProcess] mingle: all alone
celery      | 2025-04-10 08:52:45.938 | [2025-04-10 08:52:45,938: INFO/MainProcess] celery@336749e752ac ready.
celery-beat | 2025-04-10 08:52:45.969 | [2025-04-10 08:52:45,969: INFO/MainProcess] beat: Starting...
celery-beat | 2025-04-10 08:52:46.006 | [2025-04-10 08:52:46,006: INFO/MainProcess] DatabaseScheduler: Schedule changed.
web         | 2025-04-10 08:52:46.074 | [2025-04-10 11:52:46 +0000] [1] [INFO] Starting gunicorn 23.0.0
web         | 2025-04-10 08:52:46.074 | [2025-04-10 11:52:46 +0000] [1] [INFO] Listening at: http://0.0.0.0:58000 (1)
web         | 2025-04-10 08:52:46.074 | [2025-04-10 11:52:46 +0000] [1] [INFO] Using worker: sync
web         | 2025-04-10 08:52:46.075 | [2025-04-10 11:52:46 +0000] [86] [INFO] Booting worker with pid: 86
web         | 2025-04-10 08:52:46.163 | [2025-04-10 11:52:46 +0000] [87] [INFO] Booting worker with pid: 87
web         | 2025-04-10 08:52:46.259 | [2025-04-10 11:52:46 +0000] [88] [INFO] Booting worker with pid: 88