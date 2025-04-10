db          | 2025-04-10 11:31:10.275 | 2025-04-10 14:31:10+00:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 8.4.0-1.el9 started.
redis       | 2025-04-10 11:31:10.360 | 1:C 10 Apr 2025 14:31:10.360 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
redis       | 2025-04-10 11:31:10.360 | 1:C 10 Apr 2025 14:31:10.360 * Redis version=7.4.2, bits=64, commit=00000000, modified=0, pid=1, just started
redis       | 2025-04-10 11:31:10.360 | 1:C 10 Apr 2025 14:31:10.360 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
redis       | 2025-04-10 11:31:10.360 | 1:M 10 Apr 2025 14:31:10.360 * monotonic clock: POSIX clock_gettime
redis       | 2025-04-10 11:31:10.361 | 1:M 10 Apr 2025 14:31:10.361 * Running mode=standalone, port=6379.
redis       | 2025-04-10 11:31:10.361 | 1:M 10 Apr 2025 14:31:10.361 * Server initialized
redis       | 2025-04-10 11:31:10.361 | 1:M 10 Apr 2025 14:31:10.361 * Ready to accept connections tcp
db          | 2025-04-10 11:31:10.530 | 2025-04-10 14:31:10+00:00 [Note] [Entrypoint]: Switching to dedicated user 'mysql'
db          | 2025-04-10 11:31:10.541 | 2025-04-10 14:31:10+00:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 8.4.0-1.el9 started.
db          | 2025-04-10 11:31:10.696 | 2025-04-10 14:31:10+00:00 [Note] [Entrypoint]: Initializing database files
db          | 2025-04-10 11:31:10.721 | 2025-04-10T14:31:10.707159Z 0 [System] [MY-015017] [Server] MySQL Server Initialization - start.
db          | 2025-04-10 11:31:10.721 | 2025-04-10T14:31:10.708693Z 0 [System] [MY-013169] [Server] /usr/sbin/mysqld (mysqld 8.4.0) initializing of server in progress as process 81
db          | 2025-04-10 11:31:10.721 | 2025-04-10T14:31:10.720769Z 0 [Warning] [MY-010159] [Server] Setting lower_case_table_names=2 because file system for /var/lib/mysql/ is case insensitive
db          | 2025-04-10 11:31:10.742 | 2025-04-10T14:31:10.742442Z 1 [System] [MY-013576] [InnoDB] InnoDB initialization has started.
celery-beat | 2025-04-10 11:31:10.756 | wait-for-it.sh: waiting 15 seconds for db:3306
celery      | 2025-04-10 11:31:10.759 | wait-for-it.sh: waiting 15 seconds for db:3306
web         | 2025-04-10 11:31:10.761 | wait-for-it.sh: waiting 15 seconds for db:3306
birt        | 2025-04-10 11:31:10.774 | NOTE: Picked up JDK_JAVA_OPTIONS:  --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.rmi/sun.rmi.transport=ALL-UNNAMED
nginx       | 2025-04-10 11:31:10.886 | /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
nginx       | 2025-04-10 11:31:10.886 | /docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
nginx       | 2025-04-10 11:31:10.892 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
nginx       | 2025-04-10 11:31:10.916 | 10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
nginx       | 2025-04-10 11:31:10.938 | 10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
nginx       | 2025-04-10 11:31:10.938 | /docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
nginx       | 2025-04-10 11:31:10.939 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
nginx       | 2025-04-10 11:31:10.946 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
nginx       | 2025-04-10 11:31:10.948 | /docker-entrypoint.sh: Configuration complete; ready for start up
birt        | 2025-04-10 11:31:11.301 | 10-Apr-2025 14:31:11.294 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Server version name:   Apache Tomcat/9.0.102
birt        | 2025-04-10 11:31:11.301 | 10-Apr-2025 14:31:11.301 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Server built:          Mar 3 2025 19:33:14 UTC
birt        | 2025-04-10 11:31:11.301 | 10-Apr-2025 14:31:11.301 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Server version number: 9.0.102.0
birt        | 2025-04-10 11:31:11.301 | 10-Apr-2025 14:31:11.301 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log OS Name:               Linux
birt        | 2025-04-10 11:31:11.301 | 10-Apr-2025 14:31:11.301 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log OS Version:            5.15.167.4-microsoft-standard-WSL2
birt        | 2025-04-10 11:31:11.301 | 10-Apr-2025 14:31:11.301 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Architecture:          amd64
birt        | 2025-04-10 11:31:11.301 | 10-Apr-2025 14:31:11.301 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Java Home:             /opt/java/openjdk
birt        | 2025-04-10 11:31:11.302 | 10-Apr-2025 14:31:11.301 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log JVM Version:           21.0.6+7-LTS
birt        | 2025-04-10 11:31:11.302 | 10-Apr-2025 14:31:11.302 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log JVM Vendor:            Eclipse Adoptium
birt        | 2025-04-10 11:31:11.302 | 10-Apr-2025 14:31:11.302 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log CATALINA_BASE:         /usr/local/tomcat
birt        | 2025-04-10 11:31:11.302 | 10-Apr-2025 14:31:11.302 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log CATALINA_HOME:         /usr/local/tomcat
birt        | 2025-04-10 11:31:11.312 | 10-Apr-2025 14:31:11.312 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.lang=ALL-UNNAMED
birt        | 2025-04-10 11:31:11.312 | 10-Apr-2025 14:31:11.312 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.lang.invoke=ALL-UNNAMED
birt        | 2025-04-10 11:31:11.312 | 10-Apr-2025 14:31:11.312 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.lang.reflect=ALL-UNNAMED
birt        | 2025-04-10 11:31:11.312 | 10-Apr-2025 14:31:11.312 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.io=ALL-UNNAMED
birt        | 2025-04-10 11:31:11.312 | 10-Apr-2025 14:31:11.312 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.util=ALL-UNNAMED
birt        | 2025-04-10 11:31:11.312 | 10-Apr-2025 14:31:11.312 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.util.concurrent=ALL-UNNAMED
birt        | 2025-04-10 11:31:11.312 | 10-Apr-2025 14:31:11.312 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.rmi/sun.rmi.transport=ALL-UNNAMED
birt        | 2025-04-10 11:31:11.312 | 10-Apr-2025 14:31:11.312 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.util.logging.config.file=/usr/local/tomcat/conf/logging.properties
birt        | 2025-04-10 11:31:11.312 | 10-Apr-2025 14:31:11.312 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager
birt        | 2025-04-10 11:31:11.312 | 10-Apr-2025 14:31:11.312 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.awt.headless=true
birt        | 2025-04-10 11:31:11.313 | 10-Apr-2025 14:31:11.312 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djdk.tls.ephemeralDHKeySize=2048
birt        | 2025-04-10 11:31:11.313 | 10-Apr-2025 14:31:11.313 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.protocol.handler.pkgs=org.apache.catalina.webresources
birt        | 2025-04-10 11:31:11.313 | 10-Apr-2025 14:31:11.313 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dsun.io.useCanonCaches=false
birt        | 2025-04-10 11:31:11.313 | 10-Apr-2025 14:31:11.313 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dorg.apache.catalina.security.SecurityListener.UMASK=0027
birt        | 2025-04-10 11:31:11.313 | 10-Apr-2025 14:31:11.313 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dignore.endorsed.dirs=
birt        | 2025-04-10 11:31:11.313 | 10-Apr-2025 14:31:11.313 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dcatalina.base=/usr/local/tomcat
birt        | 2025-04-10 11:31:11.313 | 10-Apr-2025 14:31:11.313 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dcatalina.home=/usr/local/tomcat
birt        | 2025-04-10 11:31:11.313 | 10-Apr-2025 14:31:11.313 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.io.tmpdir=/usr/local/tomcat/temp
birt        | 2025-04-10 11:31:11.319 | 10-Apr-2025 14:31:11.318 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent Loaded Apache Tomcat Native library [1.3.1] using APR version [1.7.2].
birt        | 2025-04-10 11:31:11.319 | 10-Apr-2025 14:31:11.319 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent APR capabilities: IPv6 [true], sendfile [true], accept filters [false], random [true], UDS [true].
birt        | 2025-04-10 11:31:11.319 | 10-Apr-2025 14:31:11.319 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent APR/OpenSSL configuration: useAprConnector [false], useOpenSSL [true]
birt        | 2025-04-10 11:31:11.323 | 10-Apr-2025 14:31:11.322 INFO [main] org.apache.catalina.core.AprLifecycleListener.initializeSSL OpenSSL successfully initialized [OpenSSL 3.0.13 30 Jan 2024]
db          | 2025-04-10 11:31:11.495 | 2025-04-10T14:31:11.495043Z 1 [System] [MY-013577] [InnoDB] InnoDB initialization has ended.
birt        | 2025-04-10 11:31:11.629 | 10-Apr-2025 14:31:11.629 INFO [main] org.apache.coyote.AbstractProtocol.init Initializing ProtocolHandler ["http-nio-8080"]
birt        | 2025-04-10 11:31:11.663 | 10-Apr-2025 14:31:11.662 INFO [main] org.apache.catalina.startup.Catalina.load Server initialization in [603] milliseconds
birt        | 2025-04-10 11:31:11.698 | 10-Apr-2025 14:31:11.698 INFO [main] org.apache.catalina.core.StandardService.startInternal Starting service [Catalina]
birt        | 2025-04-10 11:31:11.698 | 10-Apr-2025 14:31:11.698 INFO [main] org.apache.catalina.core.StandardEngine.startInternal Starting Servlet engine: [Apache Tomcat/9.0.102]
birt        | 2025-04-10 11:31:11.712 | 10-Apr-2025 14:31:11.712 INFO [main] org.apache.catalina.startup.HostConfig.deployWAR Deploying web application archive [/usr/local/tomcat/webapps/birt.war]
birt        | 2025-04-10 11:31:12.308 | 10-Apr-2025 14:31:12.308 INFO [main] org.apache.jasper.servlet.TldScanner.scanJars At least one JAR was scanned for TLDs yet contained no TLDs. Enable debug logging for this logger for a complete list of JARs that were scanned but no TLDs were found in them. Skipping unneeded JARs during scanning can improve startup time and JSP compilation time.
birt        | 2025-04-10 11:31:12.356 | 10-Apr-2025 14:31:12.356 INFO [main] org.apache.catalina.startup.HostConfig.deployWAR Deployment of web application archive [/usr/local/tomcat/webapps/birt.war] has finished in [643] ms
birt        | 2025-04-10 11:31:12.359 | 10-Apr-2025 14:31:12.359 INFO [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["http-nio-8080"]
birt        | 2025-04-10 11:31:12.369 | 10-Apr-2025 14:31:12.369 INFO [main] org.apache.catalina.startup.Catalina.start Server startup in [705] milliseconds
db          | 2025-04-10 11:31:13.391 | 2025-04-10T14:31:13.391433Z 6 [Warning] [MY-010453] [Server] root@localhost is created with an empty password ! Please consider switching off the --initialize-insecure option.
db          | 2025-04-10 11:31:15.517 | 2025-04-10T14:31:15.517162Z 0 [System] [MY-015018] [Server] MySQL Server Initialization - end.
db          | 2025-04-10 11:31:15.608 | 2025-04-10 14:31:15+00:00 [Note] [Entrypoint]: Database files initialized
db          | 2025-04-10 11:31:15.608 | 2025-04-10 14:31:15+00:00 [Note] [Entrypoint]: Starting temporary server
db          | 2025-04-10 11:31:15.797 | 2025-04-10T14:31:15.616785Z 0 [System] [MY-015015] [Server] MySQL Server - start.
db          | 2025-04-10 11:31:15.797 | 2025-04-10T14:31:15.791491Z 0 [System] [MY-010116] [Server] /usr/sbin/mysqld (mysqld 8.4.0) starting as process 122
db          | 2025-04-10 11:31:15.797 | 2025-04-10T14:31:15.793848Z 0 [Warning] [MY-010159] [Server] Setting lower_case_table_names=2 because file system for /var/lib/mysql/ is case insensitive
db          | 2025-04-10 11:31:15.804 | 2025-04-10T14:31:15.804071Z 1 [System] [MY-013576] [InnoDB] InnoDB initialization has started.
db          | 2025-04-10 11:31:16.277 | 2025-04-10T14:31:16.277164Z 1 [System] [MY-013577] [InnoDB] InnoDB initialization has ended.
db          | 2025-04-10 11:31:16.587 | 2025-04-10T14:31:16.587414Z 0 [Warning] [MY-010068] [Server] CA certificate ca.pem is self signed.
db          | 2025-04-10 11:31:16.587 | 2025-04-10T14:31:16.587560Z 0 [System] [MY-013602] [Server] Channel mysql_main configured to support TLS. Encrypted connections are now supported for this channel.
db          | 2025-04-10 11:31:16.599 | 2025-04-10T14:31:16.598935Z 0 [Warning] [MY-011810] [Server] Insecure configuration for --pid-file: Location '/var/run/mysqld' in the path is accessible to all OS users. Consider choosing a different directory.
db          | 2025-04-10 11:31:16.622 | 2025-04-10T14:31:16.622511Z 0 [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections. Version: '8.4.0'  socket: '/var/run/mysqld/mysqld.sock'  port: 0  MySQL Community Server - GPL.
db          | 2025-04-10 11:31:16.628 | 2025-04-10 14:31:16+00:00 [Note] [Entrypoint]: Temporary server started.
db          | 2025-04-10 11:31:16.644 | '/var/lib/mysql/mysql.sock' -> '/var/run/mysqld/mysqld.sock'
db          | 2025-04-10 11:31:16.877 | 2025-04-10T14:31:16.877802Z 0 [System] [MY-011323] [Server] X Plugin ready for connections. Socket: /var/run/mysqld/mysqlx.sock
db          | 2025-04-10 11:31:17.108 | Warning: Unable to load '/usr/share/zoneinfo/iso3166.tab' as time zone. Skipping it.
db          | 2025-04-10 11:31:17.108 | Warning: Unable to load '/usr/share/zoneinfo/leap-seconds.list' as time zone. Skipping it.
db          | 2025-04-10 11:31:17.108 | Warning: Unable to load '/usr/share/zoneinfo/leapseconds' as time zone. Skipping it.
nginx       | 2025-04-10 11:31:17.826 | 172.18.0.1 - - [10/Apr/2025:14:31:17 +0000] "GET /admin/reloj_fichador/registrodiario/ HTTP/1.1" 502 559 "http://localhost:5080/admin/reloj_fichador/registrodiario/1014/change/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 11:31:17.826 | 2025/04/10 14:31:17 [error] 29#29: *1 connect() failed (111: Connection refused) while connecting to upstream, client: 172.18.0.1, server: localhost, request: "GET /admin/reloj_fichador/registrodiario/ HTTP/1.1", upstream: "http://172.18.0.5:58000/admin/reloj_fichador/registrodiario/", host: "localhost:5080", referrer: "http://localhost:5080/admin/reloj_fichador/registrodiario/1014/change/"
db          | 2025-04-10 11:31:17.956 | Warning: Unable to load '/usr/share/zoneinfo/tzdata.zi' as time zone. Skipping it.
db          | 2025-04-10 11:31:17.956 | Warning: Unable to load '/usr/share/zoneinfo/zone.tab' as time zone. Skipping it.
db          | 2025-04-10 11:31:17.957 | Warning: Unable to load '/usr/share/zoneinfo/zone1970.tab' as time zone. Skipping it.
db          | 2025-04-10 11:31:18.052 | 2025-04-10 14:31:18+00:00 [Note] [Entrypoint]: Creating database docker_horesdb
db          | 2025-04-10 11:31:18.063 | 2025-04-10 14:31:18+00:00 [Note] [Entrypoint]: Creating user Leandro.3996
db          | 2025-04-10 11:31:18.072 | 2025-04-10 14:31:18+00:00 [Note] [Entrypoint]: Giving user Leandro.3996 access to schema docker_horesdb
db          | 2025-04-10 11:31:18.080 | 
db          | 2025-04-10 11:31:18.081 | 2025-04-10 14:31:18+00:00 [Note] [Entrypoint]: /usr/local/bin/docker-entrypoint.sh: running /docker-entrypoint-initdb.d/backup_2025-04-10_14.30.04.sql
nginx       | 2025-04-10 11:31:18.552 | 172.18.0.1 - - [10/Apr/2025:14:31:18 +0000] "GET /admin/reloj_fichador/registrodiario/ HTTP/1.1" 502 559 "http://localhost:5080/admin/reloj_fichador/registrodiario/1014/change/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 11:31:18.552 | 2025/04/10 14:31:18 [error] 29#29: *1 connect() failed (111: Connection refused) while connecting to upstream, client: 172.18.0.1, server: localhost, request: "GET /admin/reloj_fichador/registrodiario/ HTTP/1.1", upstream: "http://172.18.0.5:58000/admin/reloj_fichador/registrodiario/", host: "localhost:5080", referrer: "http://localhost:5080/admin/reloj_fichador/registrodiario/1014/change/"
nginx       | 2025-04-10 11:31:19.041 | 172.18.0.1 - - [10/Apr/2025:14:31:19 +0000] "GET /admin/reloj_fichador/registrodiario/ HTTP/1.1" 502 559 "http://localhost:5080/admin/reloj_fichador/registrodiario/1014/change/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 11:31:19.041 | 2025/04/10 14:31:19 [error] 29#29: *1 connect() failed (111: Connection refused) while connecting to upstream, client: 172.18.0.1, server: localhost, request: "GET /admin/reloj_fichador/registrodiario/ HTTP/1.1", upstream: "http://172.18.0.5:58000/admin/reloj_fichador/registrodiario/", host: "localhost:5080", referrer: "http://localhost:5080/admin/reloj_fichador/registrodiario/1014/change/"
db          | 2025-04-10 11:31:19.178 | 
db          | 2025-04-10 11:31:19.178 | 
db          | 2025-04-10 11:31:19.179 | 2025-04-10 14:31:19+00:00 [Note] [Entrypoint]: Stopping temporary server
db          | 2025-04-10 11:31:19.187 | 2025-04-10T14:31:19.187693Z 15 [System] [MY-013172] [Server] Received SHUTDOWN from user root. Shutting down mysqld (Version: 8.4.0).
nginx       | 2025-04-10 11:31:19.482 | 172.18.0.1 - - [10/Apr/2025:14:31:19 +0000] "GET /admin/reloj_fichador/registrodiario/ HTTP/1.1" 502 559 "http://localhost:5080/admin/reloj_fichador/registrodiario/1014/change/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 11:31:19.482 | 2025/04/10 14:31:19 [error] 29#29: *1 connect() failed (111: Connection refused) while connecting to upstream, client: 172.18.0.1, server: localhost, request: "GET /admin/reloj_fichador/registrodiario/ HTTP/1.1", upstream: "http://172.18.0.5:58000/admin/reloj_fichador/registrodiario/", host: "localhost:5080", referrer: "http://localhost:5080/admin/reloj_fichador/registrodiario/1014/change/"
db          | 2025-04-10 11:31:20.031 | 2025-04-10T14:31:20.030902Z 0 [System] [MY-010910] [Server] /usr/sbin/mysqld: Shutdown complete (mysqld 8.4.0)  MySQL Community Server - GPL.
db          | 2025-04-10 11:31:20.031 | 2025-04-10T14:31:20.030916Z 0 [System] [MY-015016] [Server] MySQL Server - end.
db          | 2025-04-10 11:31:20.189 | 2025-04-10 14:31:20+00:00 [Note] [Entrypoint]: Temporary server stopped
db          | 2025-04-10 11:31:20.189 | 
db          | 2025-04-10 11:31:20.190 | 2025-04-10 14:31:20+00:00 [Note] [Entrypoint]: MySQL init process done. Ready for start up.
db          | 2025-04-10 11:31:20.190 | 
db          | 2025-04-10 11:31:20.370 | 2025-04-10T14:31:20.197698Z 0 [System] [MY-015015] [Server] MySQL Server - start.
db          | 2025-04-10 11:31:20.370 | 2025-04-10T14:31:20.367242Z 0 [System] [MY-010116] [Server] /usr/sbin/mysqld (mysqld 8.4.0) starting as process 1
db          | 2025-04-10 11:31:20.370 | 2025-04-10T14:31:20.369969Z 0 [Warning] [MY-010159] [Server] Setting lower_case_table_names=2 because file system for /var/lib/mysql/ is case insensitive
db          | 2025-04-10 11:31:20.381 | 2025-04-10T14:31:20.381179Z 1 [System] [MY-013576] [InnoDB] InnoDB initialization has started.
db          | 2025-04-10 11:31:20.920 | 2025-04-10T14:31:20.920771Z 1 [System] [MY-013577] [InnoDB] InnoDB initialization has ended.
db          | 2025-04-10 11:31:21.393 | 2025-04-10T14:31:21.393001Z 0 [Warning] [MY-010068] [Server] CA certificate ca.pem is self signed.
db          | 2025-04-10 11:31:21.393 | 2025-04-10T14:31:21.393301Z 0 [System] [MY-013602] [Server] Channel mysql_main configured to support TLS. Encrypted connections are now supported for this channel.
db          | 2025-04-10 11:31:21.412 | 2025-04-10T14:31:21.412412Z 0 [Warning] [MY-011810] [Server] Insecure configuration for --pid-file: Location '/var/run/mysqld' in the path is accessible to all OS users. Consider choosing a different directory.
db          | 2025-04-10 11:31:21.479 | 2025-04-10T14:31:21.479204Z 0 [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections. Version: '8.4.0'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server - GPL.
db          | 2025-04-10 11:31:21.734 | 2025-04-10T14:31:21.734355Z 0 [System] [MY-011323] [Server] X Plugin ready for connections. Bind-address: '::' port: 33060, socket: /var/run/mysqld/mysqlx.sock
web         | 2025-04-10 11:31:21.784 | wait-for-it.sh: db:3306 is available after 11 seconds
celery      | 2025-04-10 11:31:21.784 | wait-for-it.sh: db:3306 is available after 11 seconds
celery-beat | 2025-04-10 11:31:21.784 | wait-for-it.sh: db:3306 is available after 11 seconds
celery      | 2025-04-10 11:31:23.237 |  
celery      | 2025-04-10 11:31:23.237 |  -------------- celery@c90cc3bac635 v5.4.0 (opalescent)
celery      | 2025-04-10 11:31:23.237 | --- ***** ----- 
celery      | 2025-04-10 11:31:23.237 | -- ******* ---- Linux-5.15.167.4-microsoft-standard-WSL2-x86_64-with-glibc2.36 2025-04-10 11:31:23
celery      | 2025-04-10 11:31:23.237 | - *** --- * --- 
celery      | 2025-04-10 11:31:23.237 | - ** ---------- [config]
celery      | 2025-04-10 11:31:23.237 | - ** ---------- .> app:         mantenedor:0x7f5f43491650
celery      | 2025-04-10 11:31:23.237 | - ** ---------- .> transport:   redis://redis:6379/5
celery      | 2025-04-10 11:31:23.237 | - ** ---------- .> results:     disabled://
celery      | 2025-04-10 11:31:23.237 | - *** --- * --- .> concurrency: 6 (prefork)
celery      | 2025-04-10 11:31:23.237 | -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
celery      | 2025-04-10 11:31:23.237 | --- ***** ----- 
celery      | 2025-04-10 11:31:23.237 |  -------------- [queues]
celery      | 2025-04-10 11:31:23.237 |                 .> celery           exchange=celery(direct) key=celery
celery      | 2025-04-10 11:31:23.237 |                 
celery      | 2025-04-10 11:31:23.237 | 
celery      | 2025-04-10 11:31:23.237 | [tasks]
celery      | 2025-04-10 11:31:23.237 |   . apps.reloj_fichador.tasks.crear_asistencia_prueba
celery      | 2025-04-10 11:31:23.237 |   . apps.reloj_fichador.tasks.generar_registros_asistencia
celery      | 2025-04-10 11:31:23.237 |   . apps.reloj_fichador.tasks.prueba_tarea
celery      | 2025-04-10 11:31:23.237 |   . mantenedor.celery.debug_task
celery      | 2025-04-10 11:31:23.237 | 
web         | 2025-04-10 11:31:23.352 | Operations to perform:
web         | 2025-04-10 11:31:23.352 |   Apply all migrations: admin, admin_interface, auth, contenttypes, django_celery_beat, django_celery_results, reloj_fichador, sessions
web         | 2025-04-10 11:31:23.352 | Running migrations:
web         | 2025-04-10 11:31:23.352 |   No migrations to apply.
celery-beat | 2025-04-10 11:31:23.352 | Operations to perform:
celery-beat | 2025-04-10 11:31:23.352 |   Apply all migrations: admin, admin_interface, auth, contenttypes, django_celery_beat, django_celery_results, reloj_fichador, sessions
celery-beat | 2025-04-10 11:31:23.352 | Running migrations:
celery-beat | 2025-04-10 11:31:23.352 |   No migrations to apply.
celery      | 2025-04-10 11:31:23.603 | [2025-04-10 11:31:23,603: INFO/MainProcess] Connected to redis://redis:6379/5
celery      | 2025-04-10 11:31:23.605 | [2025-04-10 11:31:23,605: INFO/MainProcess] mingle: searching for neighbors
web         | 2025-04-10 11:31:24.375 | Found another file with the destination path 'admin/js/cancel.js'. It will be ignored since only the first encountered file is collected. If this is not what you want, make sure every static file has a unique path.
web         | 2025-04-10 11:31:24.375 | Found another file with the destination path 'admin/js/popup_response.js'. It will be ignored since only the first encountered file is collected. If this is not what you want, make sure every static file has a unique path.
web         | 2025-04-10 11:31:24.375 | 
web         | 2025-04-10 11:31:24.375 | 0 static files copied to '/app/staticfiles', 225 unmodified.
web         | 2025-04-10 11:31:24.583 | [2025-04-10 14:31:24 +0000] [1] [INFO] Starting gunicorn 23.0.0
web         | 2025-04-10 11:31:24.584 | [2025-04-10 14:31:24 +0000] [1] [INFO] Listening at: http://0.0.0.0:58000 (1)
web         | 2025-04-10 11:31:24.584 | [2025-04-10 14:31:24 +0000] [1] [INFO] Using worker: sync
web         | 2025-04-10 11:31:24.585 | [2025-04-10 14:31:24 +0000] [102] [INFO] Booting worker with pid: 102
celery-beat | 2025-04-10 11:31:24.591 | [2025-04-10 11:31:24,591: INFO/MainProcess] beat: Starting...
web         | 2025-04-10 11:31:24.599 | [2025-04-10 14:31:24 +0000] [103] [INFO] Booting worker with pid: 103
celery      | 2025-04-10 11:31:24.611 | [2025-04-10 11:31:24,611: INFO/MainProcess] mingle: all alone
web         | 2025-04-10 11:31:24.619 | [2025-04-10 14:31:24 +0000] [104] [INFO] Booting worker with pid: 104
celery      | 2025-04-10 11:31:24.623 | [2025-04-10 11:31:24,622: INFO/MainProcess] celery@c90cc3bac635 ready.
celery-beat | 2025-04-10 11:31:24.633 | [2025-04-10 11:31:24,633: INFO/MainProcess] DatabaseScheduler: Schedule changed.
web         | 2025-04-10 11:31:30.138 | /usr/local/lib/python3.11/site-packages/admin_interface/templatetags/admin_interface_tags.py:38: UserWarning: Language chooser requires Django's `set_language` view: `urlpatterns += [url(r'^i18n/', include('django.conf.urls.i18n'))]`.
web         | 2025-04-10 11:31:30.138 |   warnings.warn(
nginx       | 2025-04-10 11:31:30.185 | 172.18.0.1 - - [10/Apr/2025:14:31:30 +0000] "GET /admin/reloj_fichador/registrodiario/ HTTP/1.1" 200 42773 "http://localhost:5080/admin/reloj_fichador/registrodiario/1014/change/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 11:31:30.203 | 172.18.0.1 - - [10/Apr/2025:14:31:30 +0000] "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1" 404 555 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 11:31:30.203 | 2025/04/10 14:31:30 [error] 29#29: *2 open() "/app/media/admin-interface/logo/logo_hores.png" failed (2: No such file or directory), client: 172.18.0.1, server: localhost, request: "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1", host: "localhost:5080", referrer: "http://localhost:5080/admin/reloj_fichador/registrodiario/"
nginx       | 2025-04-10 11:31:30.235 | 172.18.0.1 - - [10/Apr/2025:14:31:30 +0000] "GET /admin/jsi18n/ HTTP/1.1" 200 8691 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
web         | 2025-04-10 11:31:30.911 | /usr/local/lib/python3.11/site-packages/admin_interface/templatetags/admin_interface_tags.py:38: UserWarning: Language chooser requires Django's `set_language` view: `urlpatterns += [url(r'^i18n/', include('django.conf.urls.i18n'))]`.
web         | 2025-04-10 11:31:30.911 |   warnings.warn(
nginx       | 2025-04-10 11:31:30.959 | 172.18.0.1 - - [10/Apr/2025:14:31:30 +0000] "GET /admin/reloj_fichador/registrodiario/ HTTP/1.1" 200 42773 "http://localhost:5080/admin/reloj_fichador/registrodiario/1014/change/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 11:31:30.976 | 172.18.0.1 - - [10/Apr/2025:14:31:30 +0000] "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1" 404 555 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 11:31:30.976 | 2025/04/10 14:31:30 [error] 29#29: *2 open() "/app/media/admin-interface/logo/logo_hores.png" failed (2: No such file or directory), client: 172.18.0.1, server: localhost, request: "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1", host: "localhost:5080", referrer: "http://localhost:5080/admin/reloj_fichador/registrodiario/"
nginx       | 2025-04-10 11:31:30.983 | 172.18.0.1 - - [10/Apr/2025:14:31:30 +0000] "GET /admin/jsi18n/ HTTP/1.1" 200 8691 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 11:31:31.774 | 172.18.0.1 - - [10/Apr/2025:14:31:31 +0000] "GET /admin/reloj_fichador/registrodiario/ HTTP/1.1" 200 42773 "http://localhost:5080/admin/reloj_fichador/registrodiario/1014/change/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 11:31:31.790 | 2025/04/10 14:31:31 [error] 29#29: *2 open() "/app/media/admin-interface/logo/logo_hores.png" failed (2: No such file or directory), client: 172.18.0.1, server: localhost, request: "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1", host: "localhost:5080", referrer: "http://localhost:5080/admin/reloj_fichador/registrodiario/"
nginx       | 2025-04-10 11:31:31.790 | 172.18.0.1 - - [10/Apr/2025:14:31:31 +0000] "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1" 404 555 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 11:31:31.797 | 172.18.0.1 - - [10/Apr/2025:14:31:31 +0000] "GET /admin/jsi18n/ HTTP/1.1" 200 8691 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 11:31:32.754 | 172.18.0.1 - - [10/Apr/2025:14:31:32 +0000] "GET /admin/reloj_fichador/registrodiario/ HTTP/1.1" 200 42773 "http://localhost:5080/admin/reloj_fichador/registrodiario/1014/change/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 11:31:32.770 | 2025/04/10 14:31:32 [error] 29#29: *2 open() "/app/media/admin-interface/logo/logo_hores.png" failed (2: No such file or directory), client: 172.18.0.1, server: localhost, request: "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1", host: "localhost:5080", referrer: "http://localhost:5080/admin/reloj_fichador/registrodiario/"
nginx       | 2025-04-10 11:31:32.770 | 172.18.0.1 - - [10/Apr/2025:14:31:32 +0000] "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1" 404 555 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 11:31:32.802 | 172.18.0.1 - - [10/Apr/2025:14:31:32 +0000] "GET /admin/jsi18n/ HTTP/1.1" 200 8691 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
web         | 2025-04-10 11:31:33.625 | /usr/local/lib/python3.11/site-packages/admin_interface/templatetags/admin_interface_tags.py:38: UserWarning: Language chooser requires Django's `set_language` view: `urlpatterns += [url(r'^i18n/', include('django.conf.urls.i18n'))]`.
web         | 2025-04-10 11:31:33.625 |   warnings.warn(
nginx       | 2025-04-10 11:31:33.669 | 172.18.0.1 - - [10/Apr/2025:14:31:33 +0000] "GET /admin/reloj_fichador/registrodiario/ HTTP/1.1" 200 42773 "http://localhost:5080/admin/reloj_fichador/registrodiario/1014/change/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 11:31:33.686 | 2025/04/10 14:31:33 [error] 29#29: *2 open() "/app/media/admin-interface/logo/logo_hores.png" failed (2: No such file or directory), client: 172.18.0.1, server: localhost, request: "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1", host: "localhost:5080", referrer: "http://localhost:5080/admin/reloj_fichador/registrodiario/"
nginx       | 2025-04-10 11:31:33.686 | 172.18.0.1 - - [10/Apr/2025:14:31:33 +0000] "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1" 404 555 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 11:31:33.694 | 172.18.0.1 - - [10/Apr/2025:14:31:33 +0000] "GET /admin/jsi18n/ HTTP/1.1" 200 8691 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 11:31:33.773 | 172.18.0.1 - - [10/Apr/2025:14:31:33 +0000] "GET /admin/reloj_fichador/registrodiario/ HTTP/1.1" 200 42773 "http://localhost:5080/admin/reloj_fichador/registrodiario/1014/change/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 11:31:33.789 | 2025/04/10 14:31:33 [error] 29#29: *2 open() "/app/media/admin-interface/logo/logo_hores.png" failed (2: No such file or directory), client: 172.18.0.1, server: localhost, request: "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1", host: "localhost:5080", referrer: "http://localhost:5080/admin/reloj_fichador/registrodiario/"
nginx       | 2025-04-10 11:31:33.789 | 172.18.0.1 - - [10/Apr/2025:14:31:33 +0000] "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1" 404 555 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 11:31:33.796 | 172.18.0.1 - - [10/Apr/2025:14:31:33 +0000] "GET /admin/jsi18n/ HTTP/1.1" 200 8691 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 11:31:33.918 | 172.18.0.1 - - [10/Apr/2025:14:31:33 +0000] "GET /admin/reloj_fichador/registrodiario/ HTTP/1.1" 200 42773 "http://localhost:5080/admin/reloj_fichador/registrodiario/1014/change/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 11:31:33.938 | 2025/04/10 14:31:33 [error] 29#29: *2 open() "/app/media/admin-interface/logo/logo_hores.png" failed (2: No such file or directory), client: 172.18.0.1, server: localhost, request: "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1", host: "localhost:5080", referrer: "http://localhost:5080/admin/reloj_fichador/registrodiario/"
nginx       | 2025-04-10 11:31:33.938 | 172.18.0.1 - - [10/Apr/2025:14:31:33 +0000] "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1" 404 555 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 11:31:33.945 | 172.18.0.1 - - [10/Apr/2025:14:31:33 +0000] "GET /admin/jsi18n/ HTTP/1.1" 200 8691 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
backup      | 2025-04-10 11:59:58.674 | wait-for-it.sh: waiting 15 seconds for db:3306
backup      | 2025-04-10 11:59:58.678 | wait-for-it.sh: db:3306 is available after 0 seconds
backup      | 2025-04-10 11:59:58.690 | mysqldump: [Warning] Using a password on the command line interface can be insecure.
backup      | 2025-04-10 11:59:58.845 | Limpiando backups antiguos...
backup      | 2025-04-10 11:59:59.878 | Limpieza completada. Se mantienen los 10 backups más recientes.
backup      | 2025-04-10 12:00:51.565 | wait-for-it.sh: waiting 15 seconds for db:3306
backup      | 2025-04-10 12:00:51.568 | wait-for-it.sh: db:3306 is available after 0 seconds
backup      | 2025-04-10 12:00:51.571 | mysqldump: [Warning] Using a password on the command line interface can be insecure.
backup      | 2025-04-10 12:00:51.730 | Limpiando backups antiguos...
backup      | 2025-04-10 12:00:51.740 | Limpieza completada. Se mantienen los 10 backups más recientes.
nginx       | 2025-04-10 12:01:37.356 | 172.18.0.1 - - [10/Apr/2025:15:01:37 +0000] "GET / HTTP/1.1" 200 14839 "-" "Expanse, a Palo Alto Networks company, searches across the global IPv4 space multiple times per day to identify customers&#39; presences on the Internet. If you would like to be excluded from our scans, please send IP addresses/domains to: scaninfo@paloaltonetworks.com"
nginx       | 2025-04-10 12:08:23.787 | 172.18.0.1 - - [10/Apr/2025:15:08:23 +0000] "\x16\x03\x01\x00\xEE\x01\x00\x00\xEA\x03\x03I\x06\xB2\xF9\xBC\x99i\xC0Y\xFB\xF8\xBAe-\x83Ud]\x0E\x8D\xB7b8\xB4g\xC6\xDD9dZ8f g\xC1\x81i\xB3\xF6\xF2\xCB\xB0\xA9\x19N\xD6\xBD\x95g|p\xFC\xE9<Z\xA1\x90T\xB7\xE9\xA58'O;\x00&\xC0+\xC0/\xC0,\xC00\xCC\xA9\xCC\xA8\xC0\x09\xC0\x13\xC0" 400 157 "-" "-"
nginx       | 2025-04-10 12:08:50.211 | 172.18.0.1 - - [10/Apr/2025:15:08:50 +0000] "GET / HTTP/1.1" 200 14839 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
nginx       | 2025-04-10 12:08:51.779 | 172.18.0.1 - - [10/Apr/2025:15:08:51 +0000] "GET / HTTP/1.1" 200 14839 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
web         | 2025-04-10 12:08:57.701 | Not Found: /favicon.ico
nginx       | 2025-04-10 12:08:57.701 | 172.18.0.1 - - [10/Apr/2025:15:08:57 +0000] "GET /favicon.ico HTTP/1.1" 404 3638 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
redis       | 2025-04-10 12:31:11.043 | 1:M 10 Apr 2025 15:31:11.043 * 1 changes in 3600 seconds. Saving...
redis       | 2025-04-10 12:31:11.045 | 1:M 10 Apr 2025 15:31:11.043 * Background saving started by pid 21
redis       | 2025-04-10 12:31:11.050 | 21:C 10 Apr 2025 15:31:11.050 * DB saved on disk
redis       | 2025-04-10 12:31:11.050 | 21:C 10 Apr 2025 15:31:11.050 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
redis       | 2025-04-10 12:31:11.144 | 1:M 10 Apr 2025 15:31:11.144 * Background saving terminated with success
backup      | 2025-04-10 12:34:13.562 | timeout: invalid time interval ''
backup      | 2025-04-10 12:34:13.564 | Try 'timeout --help' for more information.
backup      | 2025-04-10 12:34:13.564 | wait-for-it.sh: timeout occurred after waiting 15 seconds for db:3306
backup      | 2025-04-10 12:34:13.576 | mysqldump: [Warning] Using a password on the command line interface can be insecure.
backup      | 2025-04-10 12:34:13.768 | Limpiando backups antiguos...
backup      | 2025-04-10 12:34:13.784 | Limpieza completada. Se mantienen los 10 backups más recientes.
nginx       | 2025-04-10 12:34:48.169 | 172.18.0.1 - - [10/Apr/2025:15:34:48 +0000] "GET /admin/reloj_fichador/registrodiario/1014/change/ HTTP/1.1" 200 56003 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 12:34:48.190 | 2025/04/10 15:34:48 [error] 29#29: *32 open() "/app/media/admin-interface/logo/logo_hores.png" failed (2: No such file or directory), client: 172.18.0.1, server: localhost, request: "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1", host: "localhost:5080", referrer: "http://localhost:5080/admin/reloj_fichador/registrodiario/1014/change/"
nginx       | 2025-04-10 12:34:48.190 | 172.18.0.1 - - [10/Apr/2025:15:34:48 +0000] "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1" 404 555 "http://localhost:5080/admin/reloj_fichador/registrodiario/1014/change/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 12:34:48.198 | 172.18.0.1 - - [10/Apr/2025:15:34:48 +0000] "GET /admin/jsi18n/ HTTP/1.1" 200 8691 "http://localhost:5080/admin/reloj_fichador/registrodiario/1014/change/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
redis       | 2025-04-10 12:45:43.143 | 1:signal-handler (1744299943) Received SIGTERM scheduling shutdown...
birt        | 2025-04-10 12:45:43.146 | 10-Apr-2025 15:45:43.146 INFO [Thread-1] org.apache.coyote.AbstractProtocol.pause Pausing ProtocolHandler ["http-nio-8080"]
db          | 2025-04-10 12:45:43.151 | 2025-04-10T15:45:43.151684Z 0 [System] [MY-013172] [Server] Received SHUTDOWN from user <via user signal>. Shutting down mysqld (Version: 8.4.0).
birt        | 2025-04-10 12:45:43.151 | 10-Apr-2025 15:45:43.150 INFO [Thread-1] org.apache.catalina.core.StandardService.stopInternal Stopping service [Catalina]
redis       | 2025-04-10 12:45:43.162 | 1:M 10 Apr 2025 15:45:43.162 * User requested shutdown...
redis       | 2025-04-10 12:45:43.162 | 1:M 10 Apr 2025 15:45:43.162 * Saving the final RDB snapshot before exiting.
birt        | 2025-04-10 12:45:43.163 | 10-Apr-2025 15:45:43.163 INFO [Thread-1] org.apache.coyote.AbstractProtocol.stop Stopping ProtocolHandler ["http-nio-8080"]
redis       | 2025-04-10 12:45:43.167 | 1:M 10 Apr 2025 15:45:43.167 * DB saved on disk
redis       | 2025-04-10 12:45:43.167 | 1:M 10 Apr 2025 15:45:43.167 # Redis is now ready to exit, bye bye...
web         | 2025-04-10 12:45:43.170 | [2025-04-10 15:45:43 +0000] [1] [INFO] Handling signal: term
web         | 2025-04-10 12:45:43.171 | [2025-04-10 12:45:43 -0300] [102] [INFO] Worker exiting (pid: 102)
celery      | 2025-04-10 12:45:43.178 | [2025-04-10 12:45:43,168: WARNING/MainProcess] consumer: Connection to broker lost. Trying to re-establish the connection...
celery      | 2025-04-10 12:45:43.178 | Traceback (most recent call last):
celery      | 2025-04-10 12:45:43.178 |   File "/usr/local/lib/python3.11/site-packages/celery/worker/consumer/consumer.py", line 340, in start
celery      | 2025-04-10 12:45:43.178 |     blueprint.start(self)
celery      | 2025-04-10 12:45:43.178 |   File "/usr/local/lib/python3.11/site-packages/celery/bootsteps.py", line 116, in start
celery      | 2025-04-10 12:45:43.178 |     step.start(parent)
celery      | 2025-04-10 12:45:43.178 |   File "/usr/local/lib/python3.11/site-packages/celery/worker/consumer/consumer.py", line 746, in start
celery      | 2025-04-10 12:45:43.178 |     c.loop(*c.loop_args())
celery      | 2025-04-10 12:45:43.178 |   File "/usr/local/lib/python3.11/site-packages/celery/worker/loops.py", line 97, in asynloop
celery      | 2025-04-10 12:45:43.178 |     next(loop)
celery      | 2025-04-10 12:45:43.178 |   File "/usr/local/lib/python3.11/site-packages/kombu/asynchronous/hub.py", line 373, in create_loop
celery      | 2025-04-10 12:45:43.178 |     cb(*cbargs)
celery      | 2025-04-10 12:45:43.178 |   File "/usr/local/lib/python3.11/site-packages/kombu/transport/redis.py", line 1352, in on_readable
celery      | 2025-04-10 12:45:43.178 |     self.cycle.on_readable(fileno)
celery      | 2025-04-10 12:45:43.178 |   File "/usr/local/lib/python3.11/site-packages/kombu/transport/redis.py", line 569, in on_readable
celery      | 2025-04-10 12:45:43.178 |     chan.handlers[type]()
celery      | 2025-04-10 12:45:43.178 |   File "/usr/local/lib/python3.11/site-packages/kombu/transport/redis.py", line 918, in _receive
celery      | 2025-04-10 12:45:43.178 |     ret.append(self._receive_one(c))
celery      | 2025-04-10 12:45:43.178 |                ^^^^^^^^^^^^^^^^^^^^
celery      | 2025-04-10 12:45:43.178 |   File "/usr/local/lib/python3.11/site-packages/kombu/transport/redis.py", line 928, in _receive_one
celery      | 2025-04-10 12:45:43.178 |     response = c.parse_response()
celery      | 2025-04-10 12:45:43.178 |                ^^^^^^^^^^^^^^^^^^
celery      | 2025-04-10 12:45:43.178 |   File "/usr/local/lib/python3.11/site-packages/redis/client.py", line 840, in parse_response
celery      | 2025-04-10 12:45:43.178 |     response = self._execute(conn, try_read)
celery      | 2025-04-10 12:45:43.178 |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-04-10 12:45:43.178 |   File "/usr/local/lib/python3.11/site-packages/redis/client.py", line 816, in _execute
celery      | 2025-04-10 12:45:43.178 |     return conn.retry.call_with_retry(
celery      | 2025-04-10 12:45:43.178 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-04-10 12:45:43.178 |   File "/usr/local/lib/python3.11/site-packages/redis/retry.py", line 65, in call_with_retry
celery      | 2025-04-10 12:45:43.178 |     fail(error)
celery      | 2025-04-10 12:45:43.178 |   File "/usr/local/lib/python3.11/site-packages/redis/client.py", line 818, in <lambda>
celery      | 2025-04-10 12:45:43.178 |     lambda error: self._disconnect_raise_connect(conn, error),
celery      | 2025-04-10 12:45:43.178 |                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-04-10 12:45:43.178 |   File "/usr/local/lib/python3.11/site-packages/redis/client.py", line 805, in _disconnect_raise_connect
celery      | 2025-04-10 12:45:43.178 |     raise error
celery      | 2025-04-10 12:45:43.178 |   File "/usr/local/lib/python3.11/site-packages/redis/retry.py", line 62, in call_with_retry
celery      | 2025-04-10 12:45:43.178 |     return do()
celery      | 2025-04-10 12:45:43.178 |            ^^^^
celery      | 2025-04-10 12:45:43.178 |   File "/usr/local/lib/python3.11/site-packages/redis/client.py", line 817, in <lambda>
celery      | 2025-04-10 12:45:43.178 |     lambda: command(*args, **kwargs),
celery      | 2025-04-10 12:45:43.178 |             ^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-04-10 12:45:43.178 |   File "/usr/local/lib/python3.11/site-packages/redis/client.py", line 838, in try_read
celery      | 2025-04-10 12:45:43.178 |     return conn.read_response(disconnect_on_error=False, push_request=True)
celery      | 2025-04-10 12:45:43.178 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-04-10 12:45:43.178 |   File "/usr/local/lib/python3.11/site-packages/redis/connection.py", line 512, in read_response
celery      | 2025-04-10 12:45:43.178 |     response = self._parser.read_response(disable_decoding=disable_decoding)
celery      | 2025-04-10 12:45:43.178 |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-04-10 12:45:43.178 |   File "/usr/local/lib/python3.11/site-packages/redis/_parsers/resp2.py", line 15, in read_response
celery      | 2025-04-10 12:45:43.178 |     result = self._read_response(disable_decoding=disable_decoding)
celery      | 2025-04-10 12:45:43.178 |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-04-10 12:45:43.178 |   File "/usr/local/lib/python3.11/site-packages/redis/_parsers/resp2.py", line 25, in _read_response
celery      | 2025-04-10 12:45:43.178 |     raw = self._buffer.readline()
celery      | 2025-04-10 12:45:43.178 |           ^^^^^^^^^^^^^^^^^^^^^^^
celery      | 2025-04-10 12:45:43.178 |   File "/usr/local/lib/python3.11/site-packages/redis/_parsers/socket.py", line 115, in readline
celery      | 2025-04-10 12:45:43.178 |     self._read_from_socket()
celery      | 2025-04-10 12:45:43.178 |   File "/usr/local/lib/python3.11/site-packages/redis/_parsers/socket.py", line 68, in _read_from_socket
celery      | 2025-04-10 12:45:43.178 |     raise ConnectionError(SERVER_CLOSED_CONNECTION_ERROR)
celery      | 2025-04-10 12:45:43.178 | redis.exceptions.ConnectionError: Connection closed by server.
celery      | 2025-04-10 12:45:43.179 | /usr/local/lib/python3.11/site-packages/celery/worker/consumer/consumer.py:391: CPendingDeprecationWarning: 
celery      | 2025-04-10 12:45:43.179 | In Celery 5.1 we introduced an optional breaking change which
celery      | 2025-04-10 12:45:43.179 | on connection loss cancels all currently executed tasks with late acknowledgement enabled.
celery      | 2025-04-10 12:45:43.179 | These tasks cannot be acknowledged as the connection is gone, and the tasks are automatically redelivered
celery      | 2025-04-10 12:45:43.179 | back to the queue. You can enable this behavior using the worker_cancel_long_running_tasks_on_connection_loss
celery      | 2025-04-10 12:45:43.179 | setting. In Celery 5.1 it is set to False by default. The setting will be set to True by default in Celery 6.0.
celery      | 2025-04-10 12:45:43.179 | 
celery      | 2025-04-10 12:45:43.179 |   warnings.warn(CANCEL_TASKS_BY_DEFAULT, CPendingDeprecationWarning)
celery      | 2025-04-10 12:45:43.179 | 
celery      | 2025-04-10 12:45:43.179 | [2025-04-10 12:45:43,179: WARNING/MainProcess] /usr/local/lib/python3.11/site-packages/celery/worker/consumer/consumer.py:391: CPendingDeprecationWarning: 
celery      | 2025-04-10 12:45:43.179 | In Celery 5.1 we introduced an optional breaking change which
celery      | 2025-04-10 12:45:43.179 | on connection loss cancels all currently executed tasks with late acknowledgement enabled.
celery      | 2025-04-10 12:45:43.179 | These tasks cannot be acknowledged as the connection is gone, and the tasks are automatically redelivered
celery      | 2025-04-10 12:45:43.179 | back to the queue. You can enable this behavior using the worker_cancel_long_running_tasks_on_connection_loss
celery      | 2025-04-10 12:45:43.179 | setting. In Celery 5.1 it is set to False by default. The setting will be set to True by default in Celery 6.0.
celery      | 2025-04-10 12:45:43.179 | 
celery      | 2025-04-10 12:45:43.179 |   warnings.warn(CANCEL_TASKS_BY_DEFAULT, CPendingDeprecationWarning)
celery      | 2025-04-10 12:45:43.179 | 
celery      | 2025-04-10 12:45:43.180 | 
celery      | 2025-04-10 12:45:43.180 | worker: Warm shutdown (MainProcess)
web         | 2025-04-10 12:45:43.190 | [2025-04-10 12:45:43 -0300] [104] [INFO] Worker exiting (pid: 104)
web         | 2025-04-10 12:45:43.190 | [2025-04-10 12:45:43 -0300] [103] [INFO] Worker exiting (pid: 103)
birt        | 2025-04-10 12:45:43.192 | 10-Apr-2025 15:45:43.191 INFO [Thread-1] org.apache.coyote.AbstractProtocol.destroy Destroying ProtocolHandler ["http-nio-8080"]
celery-beat | 2025-04-10 12:45:43.341 | celery beat v5.4.0 (opalescent) is starting.
celery-beat | 2025-04-10 12:45:43.341 | __    -    ... __   -        _
celery-beat | 2025-04-10 12:45:43.341 | LocalTime -> 2025-04-10 11:31:24
celery-beat | 2025-04-10 12:45:43.341 | Configuration ->
celery-beat | 2025-04-10 12:45:43.341 |     . broker -> redis://redis:6379/5
celery-beat | 2025-04-10 12:45:43.341 |     . loader -> celery.loaders.app.AppLoader
celery-beat | 2025-04-10 12:45:43.341 |     . scheduler -> django_celery_beat.schedulers.DatabaseScheduler
celery-beat | 2025-04-10 12:45:43.341 | 
celery-beat | 2025-04-10 12:45:43.341 |     . logfile -> [stderr]@%INFO
celery-beat | 2025-04-10 12:45:43.341 |     . maxinterval -> 5.00 seconds (5s)
web         | 2025-04-10 12:45:43.491 | [2025-04-10 15:45:43 +0000] [1] [INFO] Shutting down: Master
db          | 2025-04-10 12:45:43.771 | 2025-04-10T15:45:43.771293Z 0 [System] [MY-010910] [Server] /usr/sbin/mysqld: Shutdown complete (mysqld 8.4.0)  MySQL Community Server - GPL.
db          | 2025-04-10 12:45:43.771 | 2025-04-10T15:45:43.771315Z 0 [System] [MY-015016] [Server] MySQL Server - end.
celery-beat | 2025-04-10 12:45:48.820 | timeout: invalid time interval ‘’
celery-beat | 2025-04-10 12:45:48.820 | Try 'timeout --help' for more information.
celery-beat | 2025-04-10 12:45:48.820 | wait-for-it.sh: timeout occurred after waiting 15 seconds for db:3306
birt        | 2025-04-10 12:45:48.915 | NOTE: Picked up JDK_JAVA_OPTIONS:  --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.rmi/sun.rmi.transport=ALL-UNNAMED
redis       | 2025-04-10 12:45:48.926 | 1:C 10 Apr 2025 15:45:48.926 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
redis       | 2025-04-10 12:45:48.926 | 1:C 10 Apr 2025 15:45:48.926 * Redis version=7.4.2, bits=64, commit=00000000, modified=0, pid=1, just started
redis       | 2025-04-10 12:45:48.926 | 1:C 10 Apr 2025 15:45:48.926 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
redis       | 2025-04-10 12:45:48.926 | 1:M 10 Apr 2025 15:45:48.926 * monotonic clock: POSIX clock_gettime
redis       | 2025-04-10 12:45:48.926 | 1:M 10 Apr 2025 15:45:48.926 * Running mode=standalone, port=6379.
redis       | 2025-04-10 12:45:48.927 | 1:M 10 Apr 2025 15:45:48.927 * Server initialized
redis       | 2025-04-10 12:45:48.927 | 1:M 10 Apr 2025 15:45:48.927 * Loading RDB produced by version 7.4.2
redis       | 2025-04-10 12:45:48.927 | 1:M 10 Apr 2025 15:45:48.927 * RDB age 5 seconds
redis       | 2025-04-10 12:45:48.927 | 1:M 10 Apr 2025 15:45:48.927 * RDB memory usage when created 1.38 Mb
redis       | 2025-04-10 12:45:48.927 | 1:M 10 Apr 2025 15:45:48.927 * Done loading RDB, keys loaded: 3, keys expired: 0.
redis       | 2025-04-10 12:45:48.927 | 1:M 10 Apr 2025 15:45:48.927 * DB loaded from disk: 0.000 seconds
redis       | 2025-04-10 12:45:48.927 | 1:M 10 Apr 2025 15:45:48.927 * Ready to accept connections tcp
web         | 2025-04-10 12:45:48.954 | timeout: invalid time interval ‘’
web         | 2025-04-10 12:45:48.954 | Try 'timeout --help' for more information.
web         | 2025-04-10 12:45:48.954 | wait-for-it.sh: timeout occurred after waiting 15 seconds for db:3306
nginx       | 2025-04-10 12:45:49.000 | /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
nginx       | 2025-04-10 12:45:49.001 | /docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
nginx       | 2025-04-10 12:45:49.002 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
nginx       | 2025-04-10 12:45:49.006 | 10-listen-on-ipv6-by-default.sh: info: IPv6 listen already enabled
nginx       | 2025-04-10 12:45:49.006 | /docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
nginx       | 2025-04-10 12:45:49.006 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
nginx       | 2025-04-10 12:45:49.009 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
nginx       | 2025-04-10 12:45:49.010 | /docker-entrypoint.sh: Configuration complete; ready for start up
celery      | 2025-04-10 12:45:49.167 | timeout: invalid time interval ‘’
celery      | 2025-04-10 12:45:49.167 | Try 'timeout --help' for more information.
celery      | 2025-04-10 12:45:49.167 | wait-for-it.sh: timeout occurred after waiting 15 seconds for db:3306
db          | 2025-04-10 12:45:49.231 | 2025-04-10 15:45:49+00:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 8.4.0-1.el9 started.
birt        | 2025-04-10 12:45:49.501 | 10-Apr-2025 15:45:49.496 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Server version name:   Apache Tomcat/9.0.102
birt        | 2025-04-10 12:45:49.501 | 10-Apr-2025 15:45:49.501 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Server built:          Mar 3 2025 19:33:14 UTC
birt        | 2025-04-10 12:45:49.501 | 10-Apr-2025 15:45:49.501 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Server version number: 9.0.102.0
birt        | 2025-04-10 12:45:49.501 | 10-Apr-2025 15:45:49.501 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log OS Name:               Linux
birt        | 2025-04-10 12:45:49.501 | 10-Apr-2025 15:45:49.501 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log OS Version:            5.15.167.4-microsoft-standard-WSL2
birt        | 2025-04-10 12:45:49.501 | 10-Apr-2025 15:45:49.501 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Architecture:          amd64
birt        | 2025-04-10 12:45:49.502 | 10-Apr-2025 15:45:49.501 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Java Home:             /opt/java/openjdk
birt        | 2025-04-10 12:45:49.502 | 10-Apr-2025 15:45:49.502 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log JVM Version:           21.0.6+7-LTS
birt        | 2025-04-10 12:45:49.502 | 10-Apr-2025 15:45:49.502 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log JVM Vendor:            Eclipse Adoptium
birt        | 2025-04-10 12:45:49.502 | 10-Apr-2025 15:45:49.502 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log CATALINA_BASE:         /usr/local/tomcat
birt        | 2025-04-10 12:45:49.502 | 10-Apr-2025 15:45:49.502 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log CATALINA_HOME:         /usr/local/tomcat
birt        | 2025-04-10 12:45:49.516 | 10-Apr-2025 15:45:49.515 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.lang=ALL-UNNAMED
birt        | 2025-04-10 12:45:49.516 | 10-Apr-2025 15:45:49.516 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.lang.invoke=ALL-UNNAMED
birt        | 2025-04-10 12:45:49.516 | 10-Apr-2025 15:45:49.516 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.lang.reflect=ALL-UNNAMED
birt        | 2025-04-10 12:45:49.517 | 10-Apr-2025 15:45:49.516 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.io=ALL-UNNAMED
birt        | 2025-04-10 12:45:49.517 | 10-Apr-2025 15:45:49.517 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.util=ALL-UNNAMED
birt        | 2025-04-10 12:45:49.517 | 10-Apr-2025 15:45:49.517 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.util.concurrent=ALL-UNNAMED
birt        | 2025-04-10 12:45:49.517 | 10-Apr-2025 15:45:49.517 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.rmi/sun.rmi.transport=ALL-UNNAMED
birt        | 2025-04-10 12:45:49.517 | 10-Apr-2025 15:45:49.517 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.util.logging.config.file=/usr/local/tomcat/conf/logging.properties
birt        | 2025-04-10 12:45:49.517 | 10-Apr-2025 15:45:49.517 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager
birt        | 2025-04-10 12:45:49.517 | 10-Apr-2025 15:45:49.517 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.awt.headless=true
birt        | 2025-04-10 12:45:49.518 | 10-Apr-2025 15:45:49.517 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djdk.tls.ephemeralDHKeySize=2048
birt        | 2025-04-10 12:45:49.518 | 10-Apr-2025 15:45:49.518 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.protocol.handler.pkgs=org.apache.catalina.webresources
birt        | 2025-04-10 12:45:49.518 | 10-Apr-2025 15:45:49.518 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dsun.io.useCanonCaches=false
birt        | 2025-04-10 12:45:49.518 | 10-Apr-2025 15:45:49.518 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dorg.apache.catalina.security.SecurityListener.UMASK=0027
birt        | 2025-04-10 12:45:49.518 | 10-Apr-2025 15:45:49.518 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dignore.endorsed.dirs=
birt        | 2025-04-10 12:45:49.518 | 10-Apr-2025 15:45:49.518 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dcatalina.base=/usr/local/tomcat
birt        | 2025-04-10 12:45:49.518 | 10-Apr-2025 15:45:49.518 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dcatalina.home=/usr/local/tomcat
birt        | 2025-04-10 12:45:49.518 | 10-Apr-2025 15:45:49.518 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.io.tmpdir=/usr/local/tomcat/temp
birt        | 2025-04-10 12:45:49.525 | 10-Apr-2025 15:45:49.525 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent Loaded Apache Tomcat Native library [1.3.1] using APR version [1.7.2].
birt        | 2025-04-10 12:45:49.525 | 10-Apr-2025 15:45:49.525 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent APR capabilities: IPv6 [true], sendfile [true], accept filters [false], random [true], UDS [true].
birt        | 2025-04-10 12:45:49.525 | 10-Apr-2025 15:45:49.525 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent APR/OpenSSL configuration: useAprConnector [false], useOpenSSL [true]
birt        | 2025-04-10 12:45:49.529 | 10-Apr-2025 15:45:49.528 INFO [main] org.apache.catalina.core.AprLifecycleListener.initializeSSL OpenSSL successfully initialized [OpenSSL 3.0.13 30 Jan 2024]
db          | 2025-04-10 12:45:49.639 | 2025-04-10 15:45:49+00:00 [Note] [Entrypoint]: Switching to dedicated user 'mysql'
db          | 2025-04-10 12:45:49.660 | 2025-04-10 15:45:49+00:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 8.4.0-1.el9 started.
db          | 2025-04-10 12:45:50.018 | '/var/lib/mysql/mysql.sock' -> '/var/run/mysqld/mysqld.sock'
birt        | 2025-04-10 12:45:50.078 | 10-Apr-2025 15:45:50.078 INFO [main] org.apache.coyote.AbstractProtocol.init Initializing ProtocolHandler ["http-nio-8080"]
birt        | 2025-04-10 12:45:50.124 | 10-Apr-2025 15:45:50.123 INFO [main] org.apache.catalina.startup.Catalina.load Server initialization in [953] milliseconds
birt        | 2025-04-10 12:45:50.189 | 10-Apr-2025 15:45:50.189 INFO [main] org.apache.catalina.core.StandardService.startInternal Starting service [Catalina]
birt        | 2025-04-10 12:45:50.189 | 10-Apr-2025 15:45:50.189 INFO [main] org.apache.catalina.core.StandardEngine.startInternal Starting Servlet engine: [Apache Tomcat/9.0.102]
birt        | 2025-04-10 12:45:50.210 | 10-Apr-2025 15:45:50.210 INFO [main] org.apache.catalina.startup.HostConfig.deployWAR Deploying web application archive [/usr/local/tomcat/webapps/birt.war]
db          | 2025-04-10 12:45:50.244 | 2025-04-10T15:45:50.038976Z 0 [System] [MY-015015] [Server] MySQL Server - start.
db          | 2025-04-10 12:45:50.244 | 2025-04-10T15:45:50.239034Z 0 [System] [MY-010116] [Server] /usr/sbin/mysqld (mysqld 8.4.0) starting as process 1
db          | 2025-04-10 12:45:50.244 | 2025-04-10T15:45:50.242531Z 0 [Warning] [MY-010159] [Server] Setting lower_case_table_names=2 because file system for /var/lib/mysql/ is case insensitive
db          | 2025-04-10 12:45:50.254 | 2025-04-10T15:45:50.254541Z 1 [System] [MY-013576] [InnoDB] InnoDB initialization has started.
web         | 2025-04-10 12:45:50.661 | Traceback (most recent call last):
web         | 2025-04-10 12:45:50.661 |   File "/usr/local/lib/python3.11/site-packages/django/db/backends/base/base.py", line 279, in ensure_connection
web         | 2025-04-10 12:45:50.662 |     self.connect()
web         | 2025-04-10 12:45:50.662 |   File "/usr/local/lib/python3.11/site-packages/django/utils/asyncio.py", line 26, in inner
web         | 2025-04-10 12:45:50.662 |     return func(*args, **kwargs)
web         | 2025-04-10 12:45:50.662 |            ^^^^^^^^^^^^^^^^^^^^^
web         | 2025-04-10 12:45:50.662 |   File "/usr/local/lib/python3.11/site-packages/django/db/backends/base/base.py", line 256, in connect
web         | 2025-04-10 12:45:50.662 |     self.connection = self.get_new_connection(conn_params)
web         | 2025-04-10 12:45:50.662 |                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
web         | 2025-04-10 12:45:50.662 |   File "/usr/local/lib/python3.11/site-packages/django/utils/asyncio.py", line 26, in inner
web         | 2025-04-10 12:45:50.662 |     return func(*args, **kwargs)
web         | 2025-04-10 12:45:50.662 |            ^^^^^^^^^^^^^^^^^^^^^
web         | 2025-04-10 12:45:50.662 |   File "/usr/local/lib/python3.11/site-packages/django/db/backends/mysql/base.py", line 256, in get_new_connection
web         | 2025-04-10 12:45:50.663 |     connection = Database.connect(**conn_params)
web         | 2025-04-10 12:45:50.663 |                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
web         | 2025-04-10 12:45:50.663 |   File "/usr/local/lib/python3.11/site-packages/MySQLdb/__init__.py", line 121, in Connect
web         | 2025-04-10 12:45:50.663 |     return Connection(*args, **kwargs)
web         | 2025-04-10 12:45:50.663 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
web         | 2025-04-10 12:45:50.663 |   File "/usr/local/lib/python3.11/site-packages/MySQLdb/connections.py", line 195, in __init__
web         | 2025-04-10 12:45:50.663 |     super().__init__(*args, **kwargs2)
web         | 2025-04-10 12:45:50.663 | MySQLdb.OperationalError: (2002, "Can't connect to server on 'db' (115)")
web         | 2025-04-10 12:45:50.663 | 
web         | 2025-04-10 12:45:50.663 | The above exception was the direct cause of the following exception:
web         | 2025-04-10 12:45:50.663 | 
web         | 2025-04-10 12:45:50.663 | Traceback (most recent call last):
web         | 2025-04-10 12:45:50.664 |   File "/app/manage.py", line 18, in <module>
web         | 2025-04-10 12:45:50.665 |     main()
web         | 2025-04-10 12:45:50.665 |   File "/app/manage.py", line 15, in main
web         | 2025-04-10 12:45:50.666 |     execute_from_command_line(sys.argv)
web         | 2025-04-10 12:45:50.666 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
web         | 2025-04-10 12:45:50.666 |     utility.execute()
web         | 2025-04-10 12:45:50.667 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 436, in execute
web         | 2025-04-10 12:45:50.667 |     self.fetch_command(subcommand).run_from_argv(self.argv)
web         | 2025-04-10 12:45:50.667 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/base.py", line 413, in run_from_argv
web         | 2025-04-10 12:45:50.667 |     self.execute(*args, **cmd_options)
web         | 2025-04-10 12:45:50.667 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/base.py", line 459, in execute
web         | 2025-04-10 12:45:50.667 |     output = self.handle(*args, **options)
web         | 2025-04-10 12:45:50.667 |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
web         | 2025-04-10 12:45:50.667 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/base.py", line 107, in wrapper
web         | 2025-04-10 12:45:50.667 |     res = handle_func(*args, **kwargs)
web         | 2025-04-10 12:45:50.668 |           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
web         | 2025-04-10 12:45:50.668 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/commands/migrate.py", line 101, in handle
web         | 2025-04-10 12:45:50.668 |     self.check(databases=[database])
web         | 2025-04-10 12:45:50.668 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/base.py", line 486, in check
web         | 2025-04-10 12:45:50.668 |     all_issues = checks.run_checks(
web         | 2025-04-10 12:45:50.668 |                  ^^^^^^^^^^^^^^^^^^
web         | 2025-04-10 12:45:50.668 |   File "/usr/local/lib/python3.11/site-packages/django/core/checks/registry.py", line 88, in run_checks
celery-beat | 2025-04-10 12:45:50.668 | Traceback (most recent call last):
celery-beat | 2025-04-10 12:45:50.668 |   File "/usr/local/lib/python3.11/site-packages/django/db/backends/base/base.py", line 279, in ensure_connection
celery-beat | 2025-04-10 12:45:50.668 |     self.connect()
celery-beat | 2025-04-10 12:45:50.668 |   File "/usr/local/lib/python3.11/site-packages/django/utils/asyncio.py", line 26, in inner
celery-beat | 2025-04-10 12:45:50.668 |     return func(*args, **kwargs)
celery-beat | 2025-04-10 12:45:50.668 |            ^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-04-10 12:45:50.668 |   File "/usr/local/lib/python3.11/site-packages/django/db/backends/base/base.py", line 256, in connect
celery-beat | 2025-04-10 12:45:50.668 |     self.connection = self.get_new_connection(conn_params)
celery-beat | 2025-04-10 12:45:50.668 |                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-04-10 12:45:50.668 |   File "/usr/local/lib/python3.11/site-packages/django/utils/asyncio.py", line 26, in inner
celery-beat | 2025-04-10 12:45:50.668 |     return func(*args, **kwargs)
celery-beat | 2025-04-10 12:45:50.668 |            ^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-04-10 12:45:50.668 |   File "/usr/local/lib/python3.11/site-packages/django/db/backends/mysql/base.py", line 256, in get_new_connection
web         | 2025-04-10 12:45:50.669 |     new_errors = check(app_configs=app_configs, databases=databases)
web         | 2025-04-10 12:45:50.669 |                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
web         | 2025-04-10 12:45:50.669 |   File "/usr/local/lib/python3.11/site-packages/django/core/checks/database.py", line 13, in check_database_backends
web         | 2025-04-10 12:45:50.669 |     issues.extend(conn.validation.check(**kwargs))
web         | 2025-04-10 12:45:50.669 |                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
web         | 2025-04-10 12:45:50.669 |   File "/usr/local/lib/python3.11/site-packages/django/db/backends/mysql/validation.py", line 9, in check
web         | 2025-04-10 12:45:50.669 |     issues.extend(self._check_sql_mode(**kwargs))
web         | 2025-04-10 12:45:50.669 |                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
web         | 2025-04-10 12:45:50.669 |   File "/usr/local/lib/python3.11/site-packages/django/db/backends/mysql/validation.py", line 14, in _check_sql_mode
web         | 2025-04-10 12:45:50.669 |     self.connection.sql_mode & {"STRICT_TRANS_TABLES", "STRICT_ALL_TABLES"}
web         | 2025-04-10 12:45:50.669 |     ^^^^^^^^^^^^^^^^^^^^^^^^
web         | 2025-04-10 12:45:50.669 |   File "/usr/local/lib/python3.11/site-packages/django/utils/functional.py", line 47, in __get__
celery-beat | 2025-04-10 12:45:50.669 |     connection = Database.connect(**conn_params)
celery-beat | 2025-04-10 12:45:50.669 |                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-04-10 12:45:50.669 |   File "/usr/local/lib/python3.11/site-packages/MySQLdb/__init__.py", line 121, in Connect
celery-beat | 2025-04-10 12:45:50.669 |     return Connection(*args, **kwargs)
celery-beat | 2025-04-10 12:45:50.669 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-04-10 12:45:50.669 |   File "/usr/local/lib/python3.11/site-packages/MySQLdb/connections.py", line 195, in __init__
celery-beat | 2025-04-10 12:45:50.669 |     super().__init__(*args, **kwargs2)
celery-beat | 2025-04-10 12:45:50.669 | MySQLdb.OperationalError: (2002, "Can't connect to server on 'db' (115)")
celery-beat | 2025-04-10 12:45:50.669 | 
celery-beat | 2025-04-10 12:45:50.669 | The above exception was the direct cause of the following exception:
celery-beat | 2025-04-10 12:45:50.669 | 
celery-beat | 2025-04-10 12:45:50.669 | Traceback (most recent call last):
celery-beat | 2025-04-10 12:45:50.669 |   File "/app/manage.py", line 18, in <module>
web         | 2025-04-10 12:45:50.670 |     res = instance.__dict__[self.name] = self.func(instance)
web         | 2025-04-10 12:45:50.670 |                                          ^^^^^^^^^^^^^^^^^^^
web         | 2025-04-10 12:45:50.670 |   File "/usr/local/lib/python3.11/site-packages/django/db/backends/mysql/base.py", line 448, in sql_mode
web         | 2025-04-10 12:45:50.670 |     sql_mode = self.mysql_server_data["sql_mode"]
web         | 2025-04-10 12:45:50.670 |                ^^^^^^^^^^^^^^^^^^^^^^
web         | 2025-04-10 12:45:50.670 |   File "/usr/local/lib/python3.11/site-packages/django/utils/functional.py", line 47, in __get__
web         | 2025-04-10 12:45:50.670 |     res = instance.__dict__[self.name] = self.func(instance)
web         | 2025-04-10 12:45:50.670 |                                          ^^^^^^^^^^^^^^^^^^^
web         | 2025-04-10 12:45:50.670 |   File "/usr/local/lib/python3.11/site-packages/django/db/backends/mysql/base.py", line 404, in mysql_server_data
web         | 2025-04-10 12:45:50.670 |     with self.temporary_connection() as cursor:
web         | 2025-04-10 12:45:50.670 |   File "/usr/local/lib/python3.11/contextlib.py", line 137, in __enter__
web         | 2025-04-10 12:45:50.671 |     return next(self.gen)
web         | 2025-04-10 12:45:50.671 |            ^^^^^^^^^^^^^^
web         | 2025-04-10 12:45:50.671 |   File "/usr/local/lib/python3.11/site-packages/django/db/backends/base/base.py", line 695, in temporary_connection
web         | 2025-04-10 12:45:50.671 |     with self.cursor() as cursor:
web         | 2025-04-10 12:45:50.671 |          ^^^^^^^^^^^^^
web         | 2025-04-10 12:45:50.671 |   File "/usr/local/lib/python3.11/site-packages/django/utils/asyncio.py", line 26, in inner
web         | 2025-04-10 12:45:50.671 |     return func(*args, **kwargs)
web         | 2025-04-10 12:45:50.671 |            ^^^^^^^^^^^^^^^^^^^^^
web         | 2025-04-10 12:45:50.671 |   File "/usr/local/lib/python3.11/site-packages/django/db/backends/base/base.py", line 320, in cursor
web         | 2025-04-10 12:45:50.671 |     return self._cursor()
web         | 2025-04-10 12:45:50.671 |            ^^^^^^^^^^^^^^
web         | 2025-04-10 12:45:50.671 |   File "/usr/local/lib/python3.11/site-packages/django/db/backends/base/base.py", line 296, in _cursor
web         | 2025-04-10 12:45:50.671 |     self.ensure_connection()
web         | 2025-04-10 12:45:50.671 |   File "/usr/local/lib/python3.11/site-packages/django/utils/asyncio.py", line 26, in inner
web         | 2025-04-10 12:45:50.671 |     return func(*args, **kwargs)
web         | 2025-04-10 12:45:50.671 |            ^^^^^^^^^^^^^^^^^^^^^
web         | 2025-04-10 12:45:50.671 |   File "/usr/local/lib/python3.11/site-packages/django/db/backends/base/base.py", line 278, in ensure_connection
web         | 2025-04-10 12:45:50.671 |     with self.wrap_database_errors:
web         | 2025-04-10 12:45:50.671 |   File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
celery-beat | 2025-04-10 12:45:50.671 |     main()
celery-beat | 2025-04-10 12:45:50.671 |   File "/app/manage.py", line 15, in main
web         | 2025-04-10 12:45:50.672 |     raise dj_exc_value.with_traceback(traceback) from exc_value
web         | 2025-04-10 12:45:50.672 |   File "/usr/local/lib/python3.11/site-packages/django/db/backends/base/base.py", line 279, in ensure_connection
web         | 2025-04-10 12:45:50.672 |     self.connect()
web         | 2025-04-10 12:45:50.672 |   File "/usr/local/lib/python3.11/site-packages/django/utils/asyncio.py", line 26, in inner
web         | 2025-04-10 12:45:50.672 |     return func(*args, **kwargs)
web         | 2025-04-10 12:45:50.672 |            ^^^^^^^^^^^^^^^^^^^^^
web         | 2025-04-10 12:45:50.672 |   File "/usr/local/lib/python3.11/site-packages/django/db/backends/base/base.py", line 256, in connect
web         | 2025-04-10 12:45:50.672 |     self.connection = self.get_new_connection(conn_params)
web         | 2025-04-10 12:45:50.672 |                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
web         | 2025-04-10 12:45:50.672 |   File "/usr/local/lib/python3.11/site-packages/django/utils/asyncio.py", line 26, in inner
web         | 2025-04-10 12:45:50.672 |     return func(*args, **kwargs)
web         | 2025-04-10 12:45:50.672 |            ^^^^^^^^^^^^^^^^^^^^^
web         | 2025-04-10 12:45:50.672 |   File "/usr/local/lib/python3.11/site-packages/django/db/backends/mysql/base.py", line 256, in get_new_connection
web         | 2025-04-10 12:45:50.672 |     connection = Database.connect(**conn_params)
web         | 2025-04-10 12:45:50.672 |                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
web         | 2025-04-10 12:45:50.672 |   File "/usr/local/lib/python3.11/site-packages/MySQLdb/__init__.py", line 121, in Connect
web         | 2025-04-10 12:45:50.672 |     return Connection(*args, **kwargs)
web         | 2025-04-10 12:45:50.672 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
web         | 2025-04-10 12:45:50.672 |   File "/usr/local/lib/python3.11/site-packages/MySQLdb/connections.py", line 195, in __init__
web         | 2025-04-10 12:45:50.672 |     super().__init__(*args, **kwargs2)
web         | 2025-04-10 12:45:50.672 | django.db.utils.OperationalError: (2002, "Can't connect to server on 'db' (115)")
celery-beat | 2025-04-10 12:45:50.673 |     execute_from_command_line(sys.argv)
celery-beat | 2025-04-10 12:45:50.673 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
celery-beat | 2025-04-10 12:45:50.673 |     utility.execute()
celery-beat | 2025-04-10 12:45:50.673 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 436, in execute
celery-beat | 2025-04-10 12:45:50.673 |     self.fetch_command(subcommand).run_from_argv(self.argv)
celery-beat | 2025-04-10 12:45:50.673 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/base.py", line 413, in run_from_argv
celery-beat | 2025-04-10 12:45:50.673 |     self.execute(*args, **cmd_options)
celery-beat | 2025-04-10 12:45:50.673 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/base.py", line 459, in execute
celery-beat | 2025-04-10 12:45:50.673 |     output = self.handle(*args, **options)
celery-beat | 2025-04-10 12:45:50.673 |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-04-10 12:45:50.673 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/base.py", line 107, in wrapper
celery-beat | 2025-04-10 12:45:50.673 |     res = handle_func(*args, **kwargs)
celery-beat | 2025-04-10 12:45:50.673 |           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-04-10 12:45:50.673 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/commands/migrate.py", line 101, in handle
celery-beat | 2025-04-10 12:45:50.673 |     self.check(databases=[database])
celery-beat | 2025-04-10 12:45:50.673 |   File "/usr/local/lib/python3.11/site-packages/django/core/management/base.py", line 486, in check
celery-beat | 2025-04-10 12:45:50.673 |     all_issues = checks.run_checks(
celery-beat | 2025-04-10 12:45:50.673 |                  ^^^^^^^^^^^^^^^^^^
celery-beat | 2025-04-10 12:45:50.673 |   File "/usr/local/lib/python3.11/site-packages/django/core/checks/registry.py", line 88, in run_checks
celery-beat | 2025-04-10 12:45:50.673 |     new_errors = check(app_configs=app_configs, databases=databases)
celery-beat | 2025-04-10 12:45:50.673 |                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-04-10 12:45:50.673 |   File "/usr/local/lib/python3.11/site-packages/django/core/checks/database.py", line 13, in check_database_backends
celery-beat | 2025-04-10 12:45:50.673 |     issues.extend(conn.validation.check(**kwargs))
celery-beat | 2025-04-10 12:45:50.673 |                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-04-10 12:45:50.673 |   File "/usr/local/lib/python3.11/site-packages/django/db/backends/mysql/validation.py", line 9, in check
celery-beat | 2025-04-10 12:45:50.674 |     issues.extend(self._check_sql_mode(**kwargs))
celery-beat | 2025-04-10 12:45:50.674 |                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-04-10 12:45:50.674 |   File "/usr/local/lib/python3.11/site-packages/django/db/backends/mysql/validation.py", line 14, in _check_sql_mode
celery-beat | 2025-04-10 12:45:50.674 |     self.connection.sql_mode & {"STRICT_TRANS_TABLES", "STRICT_ALL_TABLES"}
celery-beat | 2025-04-10 12:45:50.674 |     ^^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-04-10 12:45:50.674 |   File "/usr/local/lib/python3.11/site-packages/django/utils/functional.py", line 47, in __get__
celery-beat | 2025-04-10 12:45:50.674 |     res = instance.__dict__[self.name] = self.func(instance)
celery-beat | 2025-04-10 12:45:50.674 |                                          ^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-04-10 12:45:50.674 |   File "/usr/local/lib/python3.11/site-packages/django/db/backends/mysql/base.py", line 448, in sql_mode
celery-beat | 2025-04-10 12:45:50.674 |     sql_mode = self.mysql_server_data["sql_mode"]
celery-beat | 2025-04-10 12:45:50.674 |                ^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-04-10 12:45:50.674 |   File "/usr/local/lib/python3.11/site-packages/django/utils/functional.py", line 47, in __get__
celery-beat | 2025-04-10 12:45:50.674 |     res = instance.__dict__[self.name] = self.func(instance)
celery-beat | 2025-04-10 12:45:50.674 |                                          ^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-04-10 12:45:50.674 |   File "/usr/local/lib/python3.11/site-packages/django/db/backends/mysql/base.py", line 404, in mysql_server_data
celery-beat | 2025-04-10 12:45:50.674 |     with self.temporary_connection() as cursor:
celery-beat | 2025-04-10 12:45:50.674 |   File "/usr/local/lib/python3.11/contextlib.py", line 137, in __enter__
celery-beat | 2025-04-10 12:45:50.674 |     return next(self.gen)
celery-beat | 2025-04-10 12:45:50.674 |            ^^^^^^^^^^^^^^
celery-beat | 2025-04-10 12:45:50.674 |   File "/usr/local/lib/python3.11/site-packages/django/db/backends/base/base.py", line 695, in temporary_connection
celery-beat | 2025-04-10 12:45:50.674 |     with self.cursor() as cursor:
celery-beat | 2025-04-10 12:45:50.674 |          ^^^^^^^^^^^^^
celery-beat | 2025-04-10 12:45:50.674 |   File "/usr/local/lib/python3.11/site-packages/django/utils/asyncio.py", line 26, in inner
celery-beat | 2025-04-10 12:45:50.674 |     return func(*args, **kwargs)
celery-beat | 2025-04-10 12:45:50.674 |            ^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-04-10 12:45:50.674 |   File "/usr/local/lib/python3.11/site-packages/django/db/backends/base/base.py", line 320, in cursor
celery-beat | 2025-04-10 12:45:50.674 |     return self._cursor()
celery-beat | 2025-04-10 12:45:50.674 |            ^^^^^^^^^^^^^^
celery-beat | 2025-04-10 12:45:50.674 |   File "/usr/local/lib/python3.11/site-packages/django/db/backends/base/base.py", line 296, in _cursor
celery-beat | 2025-04-10 12:45:50.675 |     self.ensure_connection()
celery-beat | 2025-04-10 12:45:50.675 |   File "/usr/local/lib/python3.11/site-packages/django/utils/asyncio.py", line 26, in inner
celery-beat | 2025-04-10 12:45:50.675 |     return func(*args, **kwargs)
celery-beat | 2025-04-10 12:45:50.675 |            ^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-04-10 12:45:50.675 |   File "/usr/local/lib/python3.11/site-packages/django/db/backends/base/base.py", line 278, in ensure_connection
celery-beat | 2025-04-10 12:45:50.675 |     with self.wrap_database_errors:
celery-beat | 2025-04-10 12:45:50.675 |   File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
celery-beat | 2025-04-10 12:45:50.675 |     raise dj_exc_value.with_traceback(traceback) from exc_value
celery-beat | 2025-04-10 12:45:50.675 |   File "/usr/local/lib/python3.11/site-packages/django/db/backends/base/base.py", line 279, in ensure_connection
celery-beat | 2025-04-10 12:45:50.675 |     self.connect()
celery-beat | 2025-04-10 12:45:50.675 |   File "/usr/local/lib/python3.11/site-packages/django/utils/asyncio.py", line 26, in inner
celery-beat | 2025-04-10 12:45:50.675 |     return func(*args, **kwargs)
celery-beat | 2025-04-10 12:45:50.675 |            ^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-04-10 12:45:50.675 |   File "/usr/local/lib/python3.11/site-packages/django/db/backends/base/base.py", line 256, in connect
celery-beat | 2025-04-10 12:45:50.675 |     self.connection = self.get_new_connection(conn_params)
celery-beat | 2025-04-10 12:45:50.675 |                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-04-10 12:45:50.675 |   File "/usr/local/lib/python3.11/site-packages/django/utils/asyncio.py", line 26, in inner
celery-beat | 2025-04-10 12:45:50.675 |     return func(*args, **kwargs)
celery-beat | 2025-04-10 12:45:50.675 |            ^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-04-10 12:45:50.675 |   File "/usr/local/lib/python3.11/site-packages/django/db/backends/mysql/base.py", line 256, in get_new_connection
celery-beat | 2025-04-10 12:45:50.675 |     connection = Database.connect(**conn_params)
celery-beat | 2025-04-10 12:45:50.675 |                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-04-10 12:45:50.675 |   File "/usr/local/lib/python3.11/site-packages/MySQLdb/__init__.py", line 121, in Connect
celery-beat | 2025-04-10 12:45:50.675 |     return Connection(*args, **kwargs)
celery-beat | 2025-04-10 12:45:50.675 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-04-10 12:45:50.675 |   File "/usr/local/lib/python3.11/site-packages/MySQLdb/connections.py", line 195, in __init__
celery-beat | 2025-04-10 12:45:50.675 |     super().__init__(*args, **kwargs2)
celery-beat | 2025-04-10 12:45:50.675 | django.db.utils.OperationalError: (2002, "Can't connect to server on 'db' (115)")
celery      | 2025-04-10 12:45:50.891 |  
celery      | 2025-04-10 12:45:50.891 |  -------------- celery@c90cc3bac635 v5.4.0 (opalescent)
celery      | 2025-04-10 12:45:50.891 | --- ***** ----- 
celery      | 2025-04-10 12:45:50.891 | -- ******* ---- Linux-5.15.167.4-microsoft-standard-WSL2-x86_64-with-glibc2.36 2025-04-10 12:45:50
celery      | 2025-04-10 12:45:50.891 | - *** --- * --- 
celery      | 2025-04-10 12:45:50.891 | - ** ---------- [config]
celery      | 2025-04-10 12:45:50.891 | - ** ---------- .> app:         mantenedor:0x7f6fc5fcf1d0
celery      | 2025-04-10 12:45:50.891 | - ** ---------- .> transport:   redis://redis:6379/5
celery      | 2025-04-10 12:45:50.891 | - ** ---------- .> results:     disabled://
celery      | 2025-04-10 12:45:50.891 | - *** --- * --- .> concurrency: 6 (prefork)
celery      | 2025-04-10 12:45:50.891 | -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
celery      | 2025-04-10 12:45:50.891 | --- ***** ----- 
celery      | 2025-04-10 12:45:50.891 |  -------------- [queues]
celery      | 2025-04-10 12:45:50.891 |                 .> celery           exchange=celery(direct) key=celery
celery      | 2025-04-10 12:45:50.891 |                 
celery      | 2025-04-10 12:45:50.891 | 
celery      | 2025-04-10 12:45:50.891 | [tasks]
celery      | 2025-04-10 12:45:50.891 |   . apps.reloj_fichador.tasks.crear_asistencia_prueba
celery      | 2025-04-10 12:45:50.891 |   . apps.reloj_fichador.tasks.generar_registros_asistencia
celery      | 2025-04-10 12:45:50.891 |   . apps.reloj_fichador.tasks.prueba_tarea
celery      | 2025-04-10 12:45:50.891 |   . mantenedor.celery.debug_task
celery      | 2025-04-10 12:45:50.891 | 
db          | 2025-04-10 12:45:50.900 | 2025-04-10T15:45:50.900670Z 1 [System] [MY-013577] [InnoDB] InnoDB initialization has ended.
birt        | 2025-04-10 12:45:51.069 | 10-Apr-2025 15:45:51.069 INFO [main] org.apache.jasper.servlet.TldScanner.scanJars At least one JAR was scanned for TLDs yet contained no TLDs. Enable debug logging for this logger for a complete list of JARs that were scanned but no TLDs were found in them. Skipping unneeded JARs during scanning can improve startup time and JSP compilation time.
birt        | 2025-04-10 12:45:51.129 | 10-Apr-2025 15:45:51.129 INFO [main] org.apache.catalina.startup.HostConfig.deployWAR Deployment of web application archive [/usr/local/tomcat/webapps/birt.war] has finished in [919] ms
birt        | 2025-04-10 12:45:51.132 | 10-Apr-2025 15:45:51.132 INFO [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["http-nio-8080"]
birt        | 2025-04-10 12:45:51.145 | 10-Apr-2025 15:45:51.145 INFO [main] org.apache.catalina.startup.Catalina.start Server startup in [1017] milliseconds
celery      | 2025-04-10 12:45:51.341 | [2025-04-10 12:45:51,340: INFO/MainProcess] Connected to redis://redis:6379/5
celery      | 2025-04-10 12:45:51.343 | [2025-04-10 12:45:51,343: INFO/MainProcess] mingle: searching for neighbors
db          | 2025-04-10 12:45:51.377 | 2025-04-10T15:45:51.377082Z 0 [Warning] [MY-010068] [Server] CA certificate ca.pem is self signed.
db          | 2025-04-10 12:45:51.377 | 2025-04-10T15:45:51.377383Z 0 [System] [MY-013602] [Server] Channel mysql_main configured to support TLS. Encrypted connections are now supported for this channel.
db          | 2025-04-10 12:45:51.389 | 2025-04-10T15:45:51.388958Z 0 [Warning] [MY-011810] [Server] Insecure configuration for --pid-file: Location '/var/run/mysqld' in the path is accessible to all OS users. Consider choosing a different directory.
db          | 2025-04-10 12:45:51.431 | 2025-04-10T15:45:51.431770Z 0 [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections. Version: '8.4.0'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server - GPL.
celery-beat | 2025-04-10 12:45:51.586 | timeout: invalid time interval ‘’
celery-beat | 2025-04-10 12:45:51.586 | Try 'timeout --help' for more information.
celery-beat | 2025-04-10 12:45:51.587 | wait-for-it.sh: timeout occurred after waiting 15 seconds for db:3306
web         | 2025-04-10 12:45:51.667 | timeout: invalid time interval ‘’
web         | 2025-04-10 12:45:51.667 | Try 'timeout --help' for more information.
web         | 2025-04-10 12:45:51.667 | wait-for-it.sh: timeout occurred after waiting 15 seconds for db:3306
db          | 2025-04-10 12:45:51.687 | 2025-04-10T15:45:51.687239Z 0 [System] [MY-011323] [Server] X Plugin ready for connections. Bind-address: '::' port: 33060, socket: /var/run/mysqld/mysqlx.sock
celery      | 2025-04-10 12:45:52.353 | [2025-04-10 12:45:52,352: INFO/MainProcess] mingle: all alone
celery      | 2025-04-10 12:45:52.361 | [2025-04-10 12:45:52,361: INFO/MainProcess] celery@c90cc3bac635 ready.
celery-beat | 2025-04-10 12:45:52.719 | Operations to perform:
celery-beat | 2025-04-10 12:45:52.719 |   Apply all migrations: admin, admin_interface, auth, contenttypes, django_celery_beat, django_celery_results, reloj_fichador, sessions
celery-beat | 2025-04-10 12:45:52.719 | Running migrations:
celery-beat | 2025-04-10 12:45:52.719 |   No migrations to apply.
web         | 2025-04-10 12:45:52.804 | Operations to perform:
web         | 2025-04-10 12:45:52.804 |   Apply all migrations: admin, admin_interface, auth, contenttypes, django_celery_beat, django_celery_results, reloj_fichador, sessions
web         | 2025-04-10 12:45:52.804 | Running migrations:
web         | 2025-04-10 12:45:52.804 |   No migrations to apply.
celery-beat | 2025-04-10 12:45:53.804 | [2025-04-10 12:45:53,804: INFO/MainProcess] beat: Starting...
web         | 2025-04-10 12:45:53.834 | Found another file with the destination path 'admin/js/cancel.js'. It will be ignored since only the first encountered file is collected. If this is not what you want, make sure every static file has a unique path.
web         | 2025-04-10 12:45:53.834 | Found another file with the destination path 'admin/js/popup_response.js'. It will be ignored since only the first encountered file is collected. If this is not what you want, make sure every static file has a unique path.
web         | 2025-04-10 12:45:53.834 | 
web         | 2025-04-10 12:45:53.834 | 0 static files copied to '/app/staticfiles', 225 unmodified.
celery-beat | 2025-04-10 12:45:53.849 | [2025-04-10 12:45:53,849: INFO/MainProcess] DatabaseScheduler: Schedule changed.
web         | 2025-04-10 12:45:54.037 | [2025-04-10 15:45:54 +0000] [1] [INFO] Starting gunicorn 23.0.0
web         | 2025-04-10 12:45:54.037 | [2025-04-10 15:45:54 +0000] [1] [INFO] Listening at: http://0.0.0.0:58000 (1)
web         | 2025-04-10 12:45:54.037 | [2025-04-10 15:45:54 +0000] [1] [INFO] Using worker: sync
web         | 2025-04-10 12:45:54.039 | [2025-04-10 15:45:54 +0000] [73] [INFO] Booting worker with pid: 73
web         | 2025-04-10 12:45:54.102 | [2025-04-10 15:45:54 +0000] [74] [INFO] Booting worker with pid: 74
web         | 2025-04-10 12:45:54.202 | [2025-04-10 15:45:54 +0000] [75] [INFO] Booting worker with pid: 75
backup      | 2025-04-10 12:45:56.888 | timeout: invalid time interval ''
backup      | 2025-04-10 12:45:56.888 | Try 'timeout --help' for more information.
backup      | 2025-04-10 12:45:56.888 | wait-for-it.sh: timeout occurred after waiting 15 seconds for db:3306
backup      | 2025-04-10 12:45:56.895 | mysqldump: [Warning] Using a password on the command line interface can be insecure.
backup      | 2025-04-10 12:45:57.107 | Limpiando backups antiguos...
backup      | 2025-04-10 12:45:57.124 | Limpieza completada. Se mantienen los 10 backups más recientes.
backup      | 2025-04-10 13:18:07.305 | timeout: invalid time interval ''
backup      | 2025-04-10 13:18:07.305 | Try 'timeout --help' for more information.
backup      | 2025-04-10 13:18:07.305 | wait-for-it.sh: timeout occurred after waiting 15 seconds for db:3306
backup      | 2025-04-10 13:18:07.316 | mysqldump: [Warning] Using a password on the command line interface can be insecure.
backup      | 2025-04-10 13:18:07.482 | Limpiando backups antiguos...
backup      | 2025-04-10 13:18:07.495 | Limpieza completada. Se mantienen los 10 backups más recientes.
redis       | 2025-04-10 13:45:49.069 | 1:M 10 Apr 2025 16:45:49.068 * 1 changes in 3600 seconds. Saving...
redis       | 2025-04-10 13:45:49.070 | 1:M 10 Apr 2025 16:45:49.069 * Background saving started by pid 21
redis       | 2025-04-10 13:45:49.074 | 21:C 10 Apr 2025 16:45:49.074 * DB saved on disk
redis       | 2025-04-10 13:45:49.074 | 21:C 10 Apr 2025 16:45:49.074 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
redis       | 2025-04-10 13:45:49.169 | 1:M 10 Apr 2025 16:45:49.169 * Background saving terminated with success
backup      | 2025-04-10 13:48:18.838 | timeout: invalid time interval ''
backup      | 2025-04-10 13:48:18.838 | Try 'timeout --help' for more information.
backup      | 2025-04-10 13:48:18.838 | wait-for-it.sh: timeout occurred after waiting 15 seconds for db:3306
backup      | 2025-04-10 13:48:18.850 | mysqldump: [Warning] Using a password on the command line interface can be insecure.
backup      | 2025-04-10 13:48:19.010 | Limpiando backups antiguos...
backup      | 2025-04-10 13:48:19.021 | Limpieza completada. Se mantienen los 10 backups más recientes.
backup      | 2025-04-10 14:18:22.643 | timeout: invalid time interval ''
backup      | 2025-04-10 14:18:22.643 | Try 'timeout --help' for more information.
backup      | 2025-04-10 14:18:22.643 | wait-for-it.sh: timeout occurred after waiting 15 seconds for db:3306
backup      | 2025-04-10 14:18:22.646 | mysqldump: [Warning] Using a password on the command line interface can be insecure.
backup      | 2025-04-10 14:18:22.796 | Limpiando backups antiguos...
backup      | 2025-04-10 14:18:22.806 | Limpieza completada. Se mantienen los 10 backups más recientes.
nginx       | 2025-04-10 14:30:54.396 | 172.18.0.1 - - [10/Apr/2025:17:30:54 +0000] "GET / HTTP/1.1" 200 14839 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
web         | 2025-04-10 14:30:58.385 | Inconsistencia detectada en registro: No puede registrar una entrada sin una salida previa.; Después de entrada solo puede ir salida, salida_transitoria.
web         | 2025-04-10 14:30:58.389 | Bad Request: /registrar/entrada/
nginx       | 2025-04-10 14:30:58.389 | 172.18.0.1 - - [10/Apr/2025:17:30:58 +0000] "POST /registrar/entrada/ HTTP/1.1" 400 226 "http://localhost:5080/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 14:31:08.256 | 172.18.0.1 - - [10/Apr/2025:17:31:08 +0000] "POST /registrar/salida_transitoria/ HTTP/1.1" 200 108 "http://localhost:5080/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
web         | 2025-04-10 14:31:23.555 | Inconsistencia detectada en registro: Después de salida_transitoria solo puede ir entrada_transitoria.
web         | 2025-04-10 14:31:23.559 | Bad Request: /registrar/salida_transitoria/
nginx       | 2025-04-10 14:31:23.559 | 172.18.0.1 - - [10/Apr/2025:17:31:23 +0000] "POST /registrar/salida_transitoria/ HTTP/1.1" 400 186 "http://localhost:5080/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
web         | 2025-04-10 14:31:30.126 | /usr/local/lib/python3.11/site-packages/admin_interface/templatetags/admin_interface_tags.py:38: UserWarning: Language chooser requires Django's `set_language` view: `urlpatterns += [url(r'^i18n/', include('django.conf.urls.i18n'))]`.
web         | 2025-04-10 14:31:30.126 |   warnings.warn(
nginx       | 2025-04-10 14:31:30.177 | 172.18.0.1 - - [10/Apr/2025:17:31:30 +0000] "GET /admin/reloj_fichador/registrodiario/ HTTP/1.1" 200 43700 "http://localhost:5080/admin/reloj_fichador/registrodiario/1014/change/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 14:31:30.210 | 172.18.0.1 - - [10/Apr/2025:17:31:30 +0000] "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1" 404 555 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 14:31:30.210 | 2025/04/10 17:31:30 [error] 22#22: *1 open() "/app/media/admin-interface/logo/logo_hores.png" failed (2: No such file or directory), client: 172.18.0.1, server: localhost, request: "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1", host: "localhost:5080", referrer: "http://localhost:5080/admin/reloj_fichador/registrodiario/"
nginx       | 2025-04-10 14:31:30.220 | 172.18.0.1 - - [10/Apr/2025:17:31:30 +0000] "GET /admin/jsi18n/ HTTP/1.1" 200 8691 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"