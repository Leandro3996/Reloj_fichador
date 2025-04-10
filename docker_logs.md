db          | 2025-04-10 08:52:40.157 | 2025-04-10 11:52:40+00:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 8.4.0-1.el9 started.
celery      | 2025-04-10 08:52:40.408 | wait-for-it.sh: waiting 15 seconds for db:3306
backup      | 2025-04-10 08:52:40.525 | wait-for-it.sh: waiting 15 seconds for db:3306
db          | 2025-04-10 08:52:40.610 | 2025-04-10 11:52:40+00:00 [Note] [Entrypoint]: Switching to dedicated user 'mysql'
db          | 2025-04-10 08:52:40.615 | 2025-04-10 11:52:40+00:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 8.4.0-1.el9 started.
db          | 2025-04-10 08:52:40.824 | '/var/lib/mysql/mysql.sock' -> '/var/run/mysqld/mysqld.sock'
db          | 2025-04-10 08:52:41.065 | 2025-04-10T11:52:40.835345Z 0 [System] [MY-015015] [Server] MySQL Server - start.
db          | 2025-04-10 08:52:41.065 | 2025-04-10T11:52:41.061869Z 0 [System] [MY-010116] [Server] /usr/sbin/mysqld (mysqld 8.4.0) starting as process 1
db          | 2025-04-10 08:52:41.065 | 2025-04-10T11:52:41.064684Z 0 [Warning] [MY-010159] [Server] Setting lower_case_table_names=2 because file system for /var/lib/mysql/ is case insensitive
db          | 2025-04-10 08:52:41.074 | 2025-04-10T11:52:41.074195Z 1 [System] [MY-013576] [InnoDB] InnoDB initialization has started.
db          | 2025-04-10 08:52:42.317 | 2025-04-10T11:52:42.317595Z 1 [System] [MY-013577] [InnoDB] InnoDB initialization has ended.
db          | 2025-04-10 08:52:42.589 | 2025-04-10T11:52:42.589079Z 0 [System] [MY-010229] [Server] Starting XA crash recovery...
db          | 2025-04-10 08:52:42.596 | 2025-04-10T11:52:42.595882Z 0 [System] [MY-010232] [Server] XA crash recovery finished.
db          | 2025-04-10 08:52:42.701 | 2025-04-10T11:52:42.700791Z 0 [Warning] [MY-010068] [Server] CA certificate ca.pem is self signed.
db          | 2025-04-10 08:52:42.701 | 2025-04-10T11:52:42.700975Z 0 [System] [MY-013602] [Server] Channel mysql_main configured to support TLS. Encrypted connections are now supported for this channel.
db          | 2025-04-10 08:52:42.709 | 2025-04-10T11:52:42.708971Z 0 [Warning] [MY-011810] [Server] Insecure configuration for --pid-file: Location '/var/run/mysqld' in the path is accessible to all OS users. Consider choosing a different directory.
db          | 2025-04-10 08:52:42.725 | 2025-04-10T11:52:42.725274Z 0 [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections. Version: '8.4.0'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server - GPL.
db          | 2025-04-10 08:52:42.980 | 2025-04-10T11:52:42.980805Z 0 [System] [MY-011323] [Server] X Plugin ready for connections. Bind-address: '::' port: 33060, socket: /var/run/mysqld/mysqlx.sock
celery      | 2025-04-10 08:52:43.415 | wait-for-it.sh: db:3306 is available after 3 seconds
backup      | 2025-04-10 08:52:43.533 | wait-for-it.sh: db:3306 is available after 3 seconds
backup      | 2025-04-10 08:52:43.537 | mysqldump: [Warning] Using a password on the command line interface can be insecure.
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
celery      | 2025-04-10 08:52:44.920 | [2025-04-10 08:52:44,919: INFO/MainProcess] Connected to redis://redis:6379/5
celery      | 2025-04-10 08:52:44.922 | [2025-04-10 08:52:44,921: INFO/MainProcess] mingle: searching for neighbors
celery      | 2025-04-10 08:52:45.928 | [2025-04-10 08:52:45,928: INFO/MainProcess] mingle: all alone
celery      | 2025-04-10 08:52:45.938 | [2025-04-10 08:52:45,938: INFO/MainProcess] celery@336749e752ac ready.
db          | 2025-04-10 09:04:11.599 | 2025-04-10T12:04:11.599397Z 0 [System] [MY-013172] [Server] Received SHUTDOWN from user <via user signal>. Shutting down mysqld (Version: 8.4.0).
celery      | 2025-04-10 09:04:11.618 | 
celery      | 2025-04-10 09:04:11.618 | worker: Warm shutdown (MainProcess)
celery      | 2025-04-10 09:04:17.473 | wait-for-it.sh: waiting 15 seconds for db:3306
db          | 2025-04-10 09:04:18.131 | 2025-04-10T12:04:18.130907Z 0 [System] [MY-010910] [Server] /usr/sbin/mysqld: Shutdown complete (mysqld 8.4.0)  MySQL Community Server - GPL.
db          | 2025-04-10 09:04:18.131 | 2025-04-10T12:04:18.130988Z 0 [System] [MY-015016] [Server] MySQL Server - end.
db          | 2025-04-10 09:04:18.809 | 2025-04-10 12:04:18+00:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 8.4.0-1.el9 started.
db          | 2025-04-10 09:04:19.127 | 2025-04-10 12:04:19+00:00 [Note] [Entrypoint]: Switching to dedicated user 'mysql'
db          | 2025-04-10 09:04:19.130 | 2025-04-10 12:04:19+00:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 8.4.0-1.el9 started.
db          | 2025-04-10 09:04:19.276 | '/var/lib/mysql/mysql.sock' -> '/var/run/mysqld/mysqld.sock'
db          | 2025-04-10 09:04:19.465 | 2025-04-10T12:04:19.284113Z 0 [System] [MY-015015] [Server] MySQL Server - start.
db          | 2025-04-10 09:04:19.465 | 2025-04-10T12:04:19.462646Z 0 [System] [MY-010116] [Server] /usr/sbin/mysqld (mysqld 8.4.0) starting as process 1
db          | 2025-04-10 09:04:19.465 | 2025-04-10T12:04:19.464529Z 0 [Warning] [MY-010159] [Server] Setting lower_case_table_names=2 because file system for /var/lib/mysql/ is case insensitive
db          | 2025-04-10 09:04:19.471 | 2025-04-10T12:04:19.471565Z 1 [System] [MY-013576] [InnoDB] InnoDB initialization has started.
db          | 2025-04-10 09:04:20.116 | 2025-04-10T12:04:20.116623Z 1 [System] [MY-013577] [InnoDB] InnoDB initialization has ended.
db          | 2025-04-10 09:04:20.552 | 2025-04-10T12:04:20.552606Z 0 [Warning] [MY-010068] [Server] CA certificate ca.pem is self signed.
db          | 2025-04-10 09:04:20.552 | 2025-04-10T12:04:20.552901Z 0 [System] [MY-013602] [Server] Channel mysql_main configured to support TLS. Encrypted connections are now supported for this channel.
db          | 2025-04-10 09:04:20.564 | 2025-04-10T12:04:20.564325Z 0 [Warning] [MY-011810] [Server] Insecure configuration for --pid-file: Location '/var/run/mysqld' in the path is accessible to all OS users. Consider choosing a different directory.
celery      | 2025-04-10 09:04:20.571 | wait-for-it.sh: db:3306 is available after 3 seconds
db          | 2025-04-10 09:04:20.595 | 2025-04-10T12:04:20.595667Z 0 [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections. Version: '8.4.0'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server - GPL.
db          | 2025-04-10 09:04:20.851 | 2025-04-10T12:04:20.851438Z 0 [System] [MY-011323] [Server] X Plugin ready for connections. Bind-address: '::' port: 33060, socket: /var/run/mysqld/mysqlx.sock
celery      | 2025-04-10 09:04:21.478 |  
celery      | 2025-04-10 09:04:21.478 |  -------------- celery@336749e752ac v5.4.0 (opalescent)
celery      | 2025-04-10 09:04:21.478 | --- ***** ----- 
celery      | 2025-04-10 09:04:21.478 | -- ******* ---- Linux-5.15.167.4-microsoft-standard-WSL2-x86_64-with-glibc2.36 2025-04-10 09:04:21
celery      | 2025-04-10 09:04:21.478 | - *** --- * --- 
celery      | 2025-04-10 09:04:21.478 | - ** ---------- [config]
celery      | 2025-04-10 09:04:21.478 | - ** ---------- .> app:         mantenedor:0x7f85f9f57a50
celery      | 2025-04-10 09:04:21.478 | - ** ---------- .> transport:   redis://redis:6379/5
celery      | 2025-04-10 09:04:21.478 | - ** ---------- .> results:     disabled://
celery      | 2025-04-10 09:04:21.478 | - *** --- * --- .> concurrency: 6 (prefork)
celery      | 2025-04-10 09:04:21.478 | -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
celery      | 2025-04-10 09:04:21.478 | --- ***** ----- 
celery      | 2025-04-10 09:04:21.478 |  -------------- [queues]
celery      | 2025-04-10 09:04:21.478 |                 .> celery           exchange=celery(direct) key=celery
celery      | 2025-04-10 09:04:21.478 |                 
celery      | 2025-04-10 09:04:21.478 | 
celery      | 2025-04-10 09:04:21.478 | [tasks]
celery      | 2025-04-10 09:04:21.478 |   . apps.reloj_fichador.tasks.crear_asistencia_prueba
celery      | 2025-04-10 09:04:21.478 |   . apps.reloj_fichador.tasks.generar_registros_asistencia
celery      | 2025-04-10 09:04:21.478 |   . apps.reloj_fichador.tasks.prueba_tarea
celery      | 2025-04-10 09:04:21.478 |   . mantenedor.celery.debug_task
celery      | 2025-04-10 09:04:21.478 | 
celery      | 2025-04-10 09:04:21.828 | [2025-04-10 09:04:21,827: INFO/MainProcess] Connected to redis://redis:6379/5
celery      | 2025-04-10 09:04:21.830 | [2025-04-10 09:04:21,830: INFO/MainProcess] mingle: searching for neighbors
celery      | 2025-04-10 09:04:22.836 | [2025-04-10 09:04:22,835: INFO/MainProcess] mingle: all alone
celery      | 2025-04-10 09:04:22.846 | [2025-04-10 09:04:22,845: INFO/MainProcess] celery@336749e752ac ready.
backup      | 2025-04-10 09:04:25.386 | wait-for-it.sh: waiting 15 seconds for db:3306
backup      | 2025-04-10 09:04:25.388 | wait-for-it.sh: db:3306 is available after 0 seconds
backup      | 2025-04-10 09:04:25.391 | mysqldump: [Warning] Using a password on the command line interface can be insecure.
celery      | 2025-04-10 09:05:00.010 | [2025-04-10 09:05:00,010: INFO/MainProcess] Task apps.reloj_fichador.tasks.generar_registros_asistencia[ca9e5fef-4305-425b-bb92-ed3c2802793f] received
celery      | 2025-04-10 09:05:00.019 | [2025-04-10 09:05:00,019: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para BALDAZAR, RAUL - 14281172 en 2025-04-10.
celery      | 2025-04-10 09:05:00.022 | [2025-04-10 09:05:00,022: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para BAINOTTI, JORGE - 35669855 en 2025-04-10.
celery      | 2025-04-10 09:05:00.024 | [2025-04-10 09:05:00,024: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para CALDERON, CARLOS - 25040357 en 2025-04-10.
celery      | 2025-04-10 09:05:00.027 | [2025-04-10 09:05:00,026: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para GAUNA, LUCIANO - 29161251 en 2025-04-10.
celery      | 2025-04-10 09:05:00.029 | [2025-04-10 09:05:00,028: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para JARA, RAMIRO - 34965695 en 2025-04-10.
celery      | 2025-04-10 09:05:00.031 | [2025-04-10 09:05:00,030: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para LIOI, VICTOR - 22384294 en 2025-04-10.
celery      | 2025-04-10 09:05:00.033 | [2025-04-10 09:05:00,033: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para PEREZ, NICOLAS - 28757702 en 2025-04-10.
celery      | 2025-04-10 09:05:00.035 | [2025-04-10 09:05:00,035: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para PIAZZA, JORGE - 29884270 en 2025-04-10.
celery      | 2025-04-10 09:05:00.037 | [2025-04-10 09:05:00,037: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para DIAZ, LUCAS - 33920821 en 2025-04-10.
celery      | 2025-04-10 09:05:00.039 | [2025-04-10 09:05:00,039: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para LOPEZ, DANILO - 33349984 en 2025-04-10.
celery      | 2025-04-10 09:05:00.041 | [2025-04-10 09:05:00,041: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para SANTUCHO, MAXIMILIANO - 31731146 en 2025-04-10.
celery      | 2025-04-10 09:05:00.043 | [2025-04-10 09:05:00,043: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para MARTINEZ, CARLOS - 13108031 en 2025-04-10.
celery      | 2025-04-10 09:05:00.045 | [2025-04-10 09:05:00,045: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para VIOLA, HERNÁN MANUEL - 38279671 en 2025-04-10.
celery      | 2025-04-10 09:05:00.047 | [2025-04-10 09:05:00,047: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para DECO, RAFAEL EZEQUIEL - 39022473 en 2025-04-10.
celery      | 2025-04-10 09:05:00.049 | [2025-04-10 09:05:00,049: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para CANTARUTTI, FERNANDO - 37627948 en 2025-04-10.
celery      | 2025-04-10 09:05:00.051 | [2025-04-10 09:05:00,051: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para MATEUCI, SILVINA BELEN - 34965669 en 2025-04-10.
celery      | 2025-04-10 09:05:00.053 | [2025-04-10 09:05:00,053: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para VIDELA, MAURICIO - 27673387 en 2025-04-10.
celery      | 2025-04-10 09:05:00.055 | [2025-04-10 09:05:00,055: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para GOLINELLI, MARTIN - 29519506 en 2025-04-10.
celery      | 2025-04-10 09:05:00.057 | [2025-04-10 09:05:00,057: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para ZABALA, CARLOS F. - 37233007 en 2025-04-10.
celery      | 2025-04-10 09:05:00.059 | [2025-04-10 09:05:00,059: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para PIZARRO, LEANDRO E. - 39610329 en 2025-04-10.
celery      | 2025-04-10 09:05:00.061 | [2025-04-10 09:05:00,061: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para MONTI, CHRISTIAN - 36707055 en 2025-04-10.
celery      | 2025-04-10 09:05:00.063 | [2025-04-10 09:05:00,063: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para MORALES, LUCIANO N. - 36707429 en 2025-04-10.
celery      | 2025-04-10 09:05:00.065 | [2025-04-10 09:05:00,065: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para ROJAS, OSCAR - 62778461 en 2025-04-10.
celery      | 2025-04-10 09:05:00.067 | [2025-04-10 09:05:00,067: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para ALMENARA, LIHUEN ANDRES - 41484063 en 2025-04-10.
celery      | 2025-04-10 09:05:00.069 | [2025-04-10 09:05:00,069: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para FERREYRA, TOMAS - 40026784 en 2025-04-10.
celery      | 2025-04-10 09:05:00.071 | [2025-04-10 09:05:00,071: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para MARIA, GONZALO - 38159134 en 2025-04-10.
celery      | 2025-04-10 09:05:00.073 | [2025-04-10 09:05:00,073: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para AVENDAÑO, DAREL - 40678696 en 2025-04-10.
celery      | 2025-04-10 09:05:00.075 | [2025-04-10 09:05:00,075: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para RODRIGUEZ, GASTON - 37165416 en 2025-04-10.
celery      | 2025-04-10 09:05:00.077 | [2025-04-10 09:05:00,077: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para MATULICH, JOSE - 37850500 en 2025-04-10.
celery      | 2025-04-10 09:05:00.079 | [2025-04-10 09:05:00,079: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para MARUCCO, NOELIA - 32599619 en 2025-04-10.
celery      | 2025-04-10 09:05:00.081 | [2025-04-10 09:05:00,081: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para MOLINERO, JOAQUIN - 41280170 en 2025-04-10.
celery      | 2025-04-10 09:05:00.083 | [2025-04-10 09:05:00,083: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para GOMEZ, FRANCISCO - 41994218 en 2025-04-10.
celery      | 2025-04-10 09:05:00.085 | [2025-04-10 09:05:00,085: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para ALLASIA, DAMIAN - 39824996 en 2025-04-10.
celery      | 2025-04-10 09:05:00.087 | [2025-04-10 09:05:00,087: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para ACEVEDO, JULIETA - 40314005 en 2025-04-10.
celery      | 2025-04-10 09:05:00.089 | [2025-04-10 09:05:00,089: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para MANIAS, LUCAS GABRIEL - 40026647 en 2025-04-10.
celery      | 2025-04-10 09:05:00.091 | [2025-04-10 09:05:00,091: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para LOPEZ, RAYMUNDO - 37232850 en 2025-04-10.
celery      | 2025-04-10 09:05:00.093 | [2025-04-10 09:05:00,093: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para MASSAFARA, BRAIAN - 41888232 en 2025-04-10.
celery      | 2025-04-10 09:05:00.095 | [2025-04-10 09:05:00,095: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para CORONEL, ROMINA - 39176825 en 2025-04-10.
celery      | 2025-04-10 09:05:00.097 | [2025-04-10 09:05:00,097: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para LOMELLO, GONZALO - 30287386 en 2025-04-10.
celery      | 2025-04-10 09:05:00.099 | [2025-04-10 09:05:00,099: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para FERRERI, MILTON - 40299956 en 2025-04-10.
celery      | 2025-04-10 09:05:00.101 | [2025-04-10 09:05:00,101: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para QUINTEROS, BRUNO AGUSTIN - 42696371 en 2025-04-10.
celery      | 2025-04-10 09:05:00.103 | [2025-04-10 09:05:00,103: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para ARNAUD, JERONIMO - 43134653 en 2025-04-10.
celery      | 2025-04-10 09:05:00.105 | [2025-04-10 09:05:00,105: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para BELTRAN, GABRIEL - 38279571 en 2025-04-10.
celery      | 2025-04-10 09:05:00.107 | [2025-04-10 09:05:00,107: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para MARIZZA, JORGE - 40678625 en 2025-04-10.
celery      | 2025-04-10 09:05:00.109 | [2025-04-10 09:05:00,109: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para GIUSTI, JULIO - 41484043 en 2025-04-10.
celery      | 2025-04-10 09:05:00.111 | [2025-04-10 09:05:00,111: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para CABRAL, FACUNDO JULIAN - 43607689 en 2025-04-10.
celery      | 2025-04-10 09:05:00.113 | [2025-04-10 09:05:00,113: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para TESTA, ENZO NICOLAS - 43230436 en 2025-04-10.
celery      | 2025-04-10 09:05:00.115 | [2025-04-10 09:05:00,115: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para FIOL, JORGE LISANDRO - 38279683 en 2025-04-10.
celery      | 2025-04-10 09:05:00.117 | [2025-04-10 09:05:00,117: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para CEBALLOS, FERNANDO - 39610460 en 2025-04-10.
celery      | 2025-04-10 09:05:00.119 | [2025-04-10 09:05:00,119: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para ALBA, GERARDO - 43675993 en 2025-04-10.
celery      | 2025-04-10 09:05:00.121 | [2025-04-10 09:05:00,121: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para DI CROCE, JESSICA - 43015155 en 2025-04-10.
celery      | 2025-04-10 09:05:00.123 | [2025-04-10 09:05:00,123: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para JARA, DIEGO - 28816742 en 2025-04-10.
celery      | 2025-04-10 09:05:00.125 | [2025-04-10 09:05:00,125: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para SAAB, AGUSTIN GABRIEL - 37627901 en 2025-04-10.
celery      | 2025-04-10 09:05:00.127 | [2025-04-10 09:05:00,127: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para ARGUELLO, HUGO FABRICIO - 38279585 en 2025-04-10.
celery      | 2025-04-10 09:05:00.129 | [2025-04-10 09:05:00,129: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para VILLEGAS, EMMANUEL - 36707330 en 2025-04-10.
celery      | 2025-04-10 09:05:00.131 | [2025-04-10 09:05:00,131: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para WYSS, TOBIAS - 45836909 en 2025-04-10.
celery      | 2025-04-10 09:05:00.133 | [2025-04-10 09:05:00,133: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para LAZO, MATIAS - 45352705 en 2025-04-10.
celery      | 2025-04-10 09:05:00.135 | [2025-04-10 09:05:00,135: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para TURRIN, AXEL ARIEL - 38158188 en 2025-04-10.
celery      | 2025-04-10 09:05:00.137 | [2025-04-10 09:05:00,137: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para VILLALBA, RICARDO ALFREDO - 35669686 en 2025-04-10.
celery      | 2025-04-10 09:05:00.139 | [2025-04-10 09:05:00,139: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para RODRIGUEZ, TICIANO - 45836980 en 2025-04-10.
celery      | 2025-04-10 09:05:00.141 | [2025-04-10 09:05:00,141: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para BELTRAN, GERMAN - 39326346 en 2025-04-10.
celery      | 2025-04-10 09:05:00.143 | [2025-04-10 09:05:00,143: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para BAIOCCHI, SANTIAGO NICOLAS - 37232760 en 2025-04-10.
celery      | 2025-04-10 09:05:00.145 | [2025-04-10 09:05:00,145: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para DOMINGUEZ, FERNANDO ARIEL - 24726499 en 2025-04-10.
celery      | 2025-04-10 09:05:00.147 | [2025-04-10 09:05:00,147: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para JARA, DANIEL ELIAS - 38164470 en 2025-04-10.
celery      | 2025-04-10 09:05:00.149 | [2025-04-10 09:05:00,149: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para BURGOS, FACUNDO SEBASTIAN - 41280065 en 2025-04-10.
celery      | 2025-04-10 09:05:00.151 | [2025-04-10 09:05:00,151: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para FUENTES, FRANCISCO LUIS - 44296925 en 2025-04-10.
celery      | 2025-04-10 09:05:00.153 | [2025-04-10 09:05:00,152: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para GIMENEZ, BENJAMIN JOSUE - 45937356 en 2025-04-10.
celery      | 2025-04-10 09:05:00.154 | [2025-04-10 09:05:00,154: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para CROGNALI, LEONARLO DAVID - 44898882 en 2025-04-10.
celery      | 2025-04-10 09:05:00.157 | [2025-04-10 09:05:00,156: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para FUSI, LUCAS ALEJANDRO - 43675844 en 2025-04-10.
celery      | 2025-04-10 09:05:00.159 | [2025-04-10 09:05:00,159: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para GOLINELLI, BLAS - 37232833 en 2025-04-10.
celery      | 2025-04-10 09:05:00.161 | [2025-04-10 09:05:00,160: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para PIERMARINI, FACUNDO FABIAN - 41484145 en 2025-04-10.
celery      | 2025-04-10 09:05:00.162 | [2025-04-10 09:05:00,162: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para MORANGE, AGUSTIN - 46512137 en 2025-04-10.
celery      | 2025-04-10 09:05:00.164 | [2025-04-10 09:05:00,164: INFO/ForkPoolWorker-4] Task apps.reloj_fichador.tasks.generar_registros_asistencia[ca9e5fef-4305-425b-bb92-ed3c2802793f] succeeded in 0.15326706299674697s: None
celery      | 2025-04-10 09:06:50.034 | 
celery      | 2025-04-10 09:06:50.034 | worker: Warm shutdown (MainProcess)
db          | 2025-04-10 09:07:03.673 | 2025-04-10T12:07:03.673414Z 0 [System] [MY-013172] [Server] Received SHUTDOWN from user <via user signal>. Shutting down mysqld (Version: 8.4.0).
db          | 2025-04-10 09:07:04.358 | 2025-04-10T12:07:04.358309Z 0 [System] [MY-010910] [Server] /usr/sbin/mysqld: Shutdown complete (mysqld 8.4.0)  MySQL Community Server - GPL.
db          | 2025-04-10 09:07:04.358 | 2025-04-10T12:07:04.358337Z 0 [System] [MY-015016] [Server] MySQL Server - end.
db          | 2025-04-10 09:07:08.865 | 2025-04-10 12:07:08+00:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 8.4.0-1.el9 started.
backup      | 2025-04-10 09:07:09.056 | wait-for-it.sh: waiting 15 seconds for db:3306
celery      | 2025-04-10 09:07:09.254 | wait-for-it.sh: waiting 15 seconds for db:3306
db          | 2025-04-10 09:07:09.333 | 2025-04-10 12:07:09+00:00 [Note] [Entrypoint]: Switching to dedicated user 'mysql'
db          | 2025-04-10 09:07:09.344 | 2025-04-10 12:07:09+00:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 8.4.0-1.el9 started.
db          | 2025-04-10 09:07:09.539 | '/var/lib/mysql/mysql.sock' -> '/var/run/mysqld/mysqld.sock'
db          | 2025-04-10 09:07:09.731 | 2025-04-10T12:07:09.548581Z 0 [System] [MY-015015] [Server] MySQL Server - start.
db          | 2025-04-10 09:07:09.731 | 2025-04-10T12:07:09.728153Z 0 [System] [MY-010116] [Server] /usr/sbin/mysqld (mysqld 8.4.0) starting as process 1
db          | 2025-04-10 09:07:09.731 | 2025-04-10T12:07:09.730555Z 0 [Warning] [MY-010159] [Server] Setting lower_case_table_names=2 because file system for /var/lib/mysql/ is case insensitive
db          | 2025-04-10 09:07:09.739 | 2025-04-10T12:07:09.739032Z 1 [System] [MY-013576] [InnoDB] InnoDB initialization has started.
db          | 2025-04-10 09:07:10.593 | 2025-04-10T12:07:10.593342Z 1 [System] [MY-013577] [InnoDB] InnoDB initialization has ended.
db          | 2025-04-10 09:07:10.948 | 2025-04-10T12:07:10.947941Z 0 [Warning] [MY-010068] [Server] CA certificate ca.pem is self signed.
db          | 2025-04-10 09:07:10.948 | 2025-04-10T12:07:10.948155Z 0 [System] [MY-013602] [Server] Channel mysql_main configured to support TLS. Encrypted connections are now supported for this channel.
db          | 2025-04-10 09:07:10.960 | 2025-04-10T12:07:10.960312Z 0 [Warning] [MY-011810] [Server] Insecure configuration for --pid-file: Location '/var/run/mysqld' in the path is accessible to all OS users. Consider choosing a different directory.
db          | 2025-04-10 09:07:10.990 | 2025-04-10T12:07:10.989983Z 0 [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections. Version: '8.4.0'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server - GPL.
backup      | 2025-04-10 09:07:11.062 | wait-for-it.sh: db:3306 is available after 2 seconds
backup      | 2025-04-10 09:07:11.065 | mysqldump: [Warning] Using a password on the command line interface can be insecure.
db          | 2025-04-10 09:07:11.246 | 2025-04-10T12:07:11.246309Z 0 [System] [MY-011323] [Server] X Plugin ready for connections. Bind-address: '::' port: 33060, socket: /var/run/mysqld/mysqlx.sock
celery      | 2025-04-10 09:07:11.261 | wait-for-it.sh: db:3306 is available after 2 seconds
celery      | 2025-04-10 09:07:12.229 |  
celery      | 2025-04-10 09:07:12.229 |  -------------- celery@336749e752ac v5.4.0 (opalescent)
celery      | 2025-04-10 09:07:12.229 | --- ***** ----- 
celery      | 2025-04-10 09:07:12.229 | -- ******* ---- Linux-5.15.167.4-microsoft-standard-WSL2-x86_64-with-glibc2.36 2025-04-10 09:07:12
celery      | 2025-04-10 09:07:12.229 | - *** --- * --- 
celery      | 2025-04-10 09:07:12.229 | - ** ---------- [config]
celery      | 2025-04-10 09:07:12.229 | - ** ---------- .> app:         mantenedor:0x7fb04e457190
celery      | 2025-04-10 09:07:12.229 | - ** ---------- .> transport:   redis://redis:6379/5
celery      | 2025-04-10 09:07:12.229 | - ** ---------- .> results:     disabled://
celery      | 2025-04-10 09:07:12.229 | - *** --- * --- .> concurrency: 6 (prefork)
celery      | 2025-04-10 09:07:12.229 | -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
celery      | 2025-04-10 09:07:12.229 | --- ***** ----- 
celery      | 2025-04-10 09:07:12.229 |  -------------- [queues]
celery      | 2025-04-10 09:07:12.229 |                 .> celery           exchange=celery(direct) key=celery
celery      | 2025-04-10 09:07:12.229 |                 
celery      | 2025-04-10 09:07:12.229 | 
celery      | 2025-04-10 09:07:12.229 | [tasks]
celery      | 2025-04-10 09:07:12.229 |   . apps.reloj_fichador.tasks.crear_asistencia_prueba
celery      | 2025-04-10 09:07:12.229 |   . apps.reloj_fichador.tasks.generar_registros_asistencia
celery      | 2025-04-10 09:07:12.229 |   . apps.reloj_fichador.tasks.prueba_tarea
celery      | 2025-04-10 09:07:12.229 |   . mantenedor.celery.debug_task
celery      | 2025-04-10 09:07:12.229 | 
celery      | 2025-04-10 09:07:12.567 | [2025-04-10 09:07:12,566: INFO/MainProcess] Connected to redis://redis:6379/5
celery      | 2025-04-10 09:07:12.569 | [2025-04-10 09:07:12,569: INFO/MainProcess] mingle: searching for neighbors
celery      | 2025-04-10 09:07:13.575 | [2025-04-10 09:07:13,575: INFO/MainProcess] mingle: all alone
celery      | 2025-04-10 09:07:13.582 | [2025-04-10 09:07:13,582: INFO/MainProcess] celery@336749e752ac ready.
db          | 2025-04-10 09:08:38.476 | 2025-04-10T12:08:38.476571Z 0 [System] [MY-013172] [Server] Received SHUTDOWN from user <via user signal>. Shutting down mysqld (Version: 8.4.0).
celery      | 2025-04-10 09:08:38.487 | 
celery      | 2025-04-10 09:08:38.487 | worker: Warm shutdown (MainProcess)
db          | 2025-04-10 09:08:43.342 | 2025-04-10T12:08:43.342184Z 0 [System] [MY-010910] [Server] /usr/sbin/mysqld: Shutdown complete (mysqld 8.4.0)  MySQL Community Server - GPL.
db          | 2025-04-10 09:08:43.342 | 2025-04-10T12:08:43.342212Z 0 [System] [MY-015016] [Server] MySQL Server - end.
celery      | 2025-04-10 09:08:44.482 | wait-for-it.sh: waiting 15 seconds for db:3306
db          | 2025-04-10 09:08:44.586 | 2025-04-10 12:08:44+00:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 8.4.0-1.el9 started.
db          | 2025-04-10 09:08:44.958 | 2025-04-10 12:08:44+00:00 [Note] [Entrypoint]: Switching to dedicated user 'mysql'
db          | 2025-04-10 09:08:44.962 | 2025-04-10 12:08:44+00:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 8.4.0-1.el9 started.
db          | 2025-04-10 09:08:45.125 | '/var/lib/mysql/mysql.sock' -> '/var/run/mysqld/mysqld.sock'
db          | 2025-04-10 09:08:45.308 | 2025-04-10T12:08:45.134807Z 0 [System] [MY-015015] [Server] MySQL Server - start.
db          | 2025-04-10 09:08:45.308 | 2025-04-10T12:08:45.305670Z 0 [System] [MY-010116] [Server] /usr/sbin/mysqld (mysqld 8.4.0) starting as process 1
db          | 2025-04-10 09:08:45.308 | 2025-04-10T12:08:45.307979Z 0 [Warning] [MY-010159] [Server] Setting lower_case_table_names=2 because file system for /var/lib/mysql/ is case insensitive
db          | 2025-04-10 09:08:45.315 | 2025-04-10T12:08:45.315732Z 1 [System] [MY-013576] [InnoDB] InnoDB initialization has started.
db          | 2025-04-10 09:08:45.955 | 2025-04-10T12:08:45.955178Z 1 [System] [MY-013577] [InnoDB] InnoDB initialization has ended.
db          | 2025-04-10 09:08:46.319 | 2025-04-10T12:08:46.319275Z 0 [Warning] [MY-010068] [Server] CA certificate ca.pem is self signed.
db          | 2025-04-10 09:08:46.319 | 2025-04-10T12:08:46.319714Z 0 [System] [MY-013602] [Server] Channel mysql_main configured to support TLS. Encrypted connections are now supported for this channel.
db          | 2025-04-10 09:08:46.330 | 2025-04-10T12:08:46.330140Z 0 [Warning] [MY-011810] [Server] Insecure configuration for --pid-file: Location '/var/run/mysqld' in the path is accessible to all OS users. Consider choosing a different directory.
db          | 2025-04-10 09:08:46.356 | 2025-04-10T12:08:46.356032Z 0 [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections. Version: '8.4.0'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server - GPL.
celery      | 2025-04-10 09:08:46.566 | wait-for-it.sh: db:3306 is available after 2 seconds
db          | 2025-04-10 09:08:46.611 | 2025-04-10T12:08:46.611228Z 0 [System] [MY-011323] [Server] X Plugin ready for connections. Bind-address: '::' port: 33060, socket: /var/run/mysqld/mysqlx.sock
celery      | 2025-04-10 09:08:47.436 |  
celery      | 2025-04-10 09:08:47.436 |  -------------- celery@336749e752ac v5.4.0 (opalescent)
celery      | 2025-04-10 09:08:47.436 | --- ***** ----- 
celery      | 2025-04-10 09:08:47.436 | -- ******* ---- Linux-5.15.167.4-microsoft-standard-WSL2-x86_64-with-glibc2.36 2025-04-10 09:08:47
celery      | 2025-04-10 09:08:47.436 | - *** --- * --- 
celery      | 2025-04-10 09:08:47.436 | - ** ---------- [config]
celery      | 2025-04-10 09:08:47.436 | - ** ---------- .> app:         mantenedor:0x7f0a7191bdd0
celery      | 2025-04-10 09:08:47.436 | - ** ---------- .> transport:   redis://redis:6379/5
celery      | 2025-04-10 09:08:47.436 | - ** ---------- .> results:     disabled://
celery      | 2025-04-10 09:08:47.436 | - *** --- * --- .> concurrency: 6 (prefork)
celery      | 2025-04-10 09:08:47.436 | -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
celery      | 2025-04-10 09:08:47.436 | --- ***** ----- 
celery      | 2025-04-10 09:08:47.436 |  -------------- [queues]
celery      | 2025-04-10 09:08:47.436 |                 .> celery           exchange=celery(direct) key=celery
celery      | 2025-04-10 09:08:47.436 |                 
celery      | 2025-04-10 09:08:47.436 | 
celery      | 2025-04-10 09:08:47.436 | [tasks]
celery      | 2025-04-10 09:08:47.436 |   . apps.reloj_fichador.tasks.crear_asistencia_prueba
celery      | 2025-04-10 09:08:47.436 |   . apps.reloj_fichador.tasks.generar_registros_asistencia
celery      | 2025-04-10 09:08:47.436 |   . apps.reloj_fichador.tasks.prueba_tarea
celery      | 2025-04-10 09:08:47.436 |   . mantenedor.celery.debug_task
celery      | 2025-04-10 09:08:47.436 | 
celery      | 2025-04-10 09:08:47.695 | [2025-04-10 09:08:47,694: INFO/MainProcess] Connected to redis://redis:6379/5
celery      | 2025-04-10 09:08:47.697 | [2025-04-10 09:08:47,697: INFO/MainProcess] mingle: searching for neighbors
celery      | 2025-04-10 09:08:48.702 | [2025-04-10 09:08:48,702: INFO/MainProcess] mingle: all alone
celery      | 2025-04-10 09:08:48.708 | [2025-04-10 09:08:48,708: INFO/MainProcess] celery@336749e752ac ready.
backup      | 2025-04-10 09:08:52.342 | wait-for-it.sh: waiting 15 seconds for db:3306
backup      | 2025-04-10 09:08:52.344 | wait-for-it.sh: db:3306 is available after 0 seconds
backup      | 2025-04-10 09:08:52.347 | mysqldump: [Warning] Using a password on the command line interface can be insecure.
db          | 2025-04-10 09:09:10.869 | 2025-04-10T12:09:10.869586Z 0 [System] [MY-013172] [Server] Received SHUTDOWN from user <via user signal>. Shutting down mysqld (Version: 8.4.0).
celery      | 2025-04-10 09:09:10.883 | 
celery      | 2025-04-10 09:09:10.884 | worker: Warm shutdown (MainProcess)
db          | 2025-04-10 09:09:11.697 | 2025-04-10T12:09:11.697334Z 0 [System] [MY-010910] [Server] /usr/sbin/mysqld: Shutdown complete (mysqld 8.4.0)  MySQL Community Server - GPL.
db          | 2025-04-10 09:09:11.697 | 2025-04-10T12:09:11.697356Z 0 [System] [MY-015016] [Server] MySQL Server - end.
celery-beat | 2025-04-10 08:52:40.604 | wait-for-it.sh: waiting 15 seconds for db:3306
celery-beat | 2025-04-10 08:52:43.611 | wait-for-it.sh: db:3306 is available after 3 seconds
celery-beat | 2025-04-10 08:52:45.969 | [2025-04-10 08:52:45,969: INFO/MainProcess] beat: Starting...
celery-beat | 2025-04-10 08:52:46.006 | [2025-04-10 08:52:46,006: INFO/MainProcess] DatabaseScheduler: Schedule changed.
celery-beat | 2025-04-10 09:04:17.202 | wait-for-it.sh: waiting 15 seconds for db:3306
celery-beat | 2025-04-10 09:04:21.210 | wait-for-it.sh: db:3306 is available after 4 seconds
celery-beat | 2025-04-10 08:52:44.760 | Operations to perform:
celery-beat | 2025-04-10 08:52:44.760 |   Apply all migrations: admin, admin_interface, auth, contenttypes, django_celery_beat, django_celery_results, reloj_fichador, sessions
celery-beat | 2025-04-10 08:52:44.760 | Running migrations:
celery-beat | 2025-04-10 08:52:44.760 |   No migrations to apply.
celery-beat | 2025-04-10 09:04:11.822 | celery beat v5.4.0 (opalescent) is starting.
celery-beat | 2025-04-10 09:04:11.822 | __    -    ... __   -        _
celery-beat | 2025-04-10 09:04:11.822 | LocalTime -> 2025-04-10 08:52:45
celery-beat | 2025-04-10 09:04:11.822 | Configuration ->
celery-beat | 2025-04-10 09:04:11.822 |     . broker -> redis://redis:6379/5
celery-beat | 2025-04-10 09:04:11.822 |     . loader -> celery.loaders.app.AppLoader
celery-beat | 2025-04-10 09:04:11.822 |     . scheduler -> django_celery_beat.schedulers.DatabaseScheduler
celery-beat | 2025-04-10 09:04:11.822 | 
celery-beat | 2025-04-10 09:04:11.822 |     . logfile -> [stderr]@%INFO
celery-beat | 2025-04-10 09:04:11.822 |     . maxinterval -> 5.00 seconds (5s)
celery-beat | 2025-04-10 09:04:22.367 | Operations to perform:
celery-beat | 2025-04-10 09:04:22.367 |   Apply all migrations: admin, admin_interface, auth, contenttypes, django_celery_beat, django_celery_results, reloj_fichador, sessions
celery-beat | 2025-04-10 09:04:22.367 | Running migrations:
celery-beat | 2025-04-10 09:04:22.367 |   No migrations to apply.
celery-beat | 2025-04-10 09:04:23.507 | [2025-04-10 09:04:23,507: INFO/MainProcess] beat: Starting...
celery-beat | 2025-04-10 09:04:23.551 | [2025-04-10 09:04:23,551: INFO/MainProcess] DatabaseScheduler: Schedule changed.
celery-beat | 2025-04-10 09:05:00.003 | [2025-04-10 09:05:00,002: INFO/MainProcess] Scheduler: Sending due task generar-registros-asistencia-5am (apps.reloj_fichador.tasks.generar_registros_asistencia)
celery-beat | 2025-04-10 09:06:50.076 | [2025-04-10 09:06:50,061: CRITICAL/MainProcess] beat raised exception <class 'ValueError'>: ValueError('MySQL backend does not support timezone-aware datetimes when USE_TZ is False.')
celery-beat | 2025-04-10 09:06:50.076 | Traceback (most recent call last):
celery-beat | 2025-04-10 09:06:50.076 |   File "/usr/local/lib/python3.11/site-packages/celery/apps/beat.py", line 113, in start_scheduler
celery-beat | 2025-04-10 09:06:50.076 |     service.start()
celery-beat | 2025-04-10 09:06:50.076 |   File "/usr/local/lib/python3.11/site-packages/celery/beat.py", line 647, in start
celery-beat | 2025-04-10 09:06:50.076 |     time.sleep(interval)
celery-beat | 2025-04-10 09:06:50.076 |   File "/usr/local/lib/python3.11/site-packages/celery/apps/beat.py", line 158, in _sync
celery-beat | 2025-04-10 09:06:50.076 |     service.sync()
celery-beat | 2025-04-10 09:06:50.076 |   File "/usr/local/lib/python3.11/site-packages/celery/beat.py", line 656, in sync
celery-beat | 2025-04-10 09:06:50.076 |     self.scheduler.close()
celery-beat | 2025-04-10 09:06:50.076 |   File "/usr/local/lib/python3.11/site-packages/celery/beat.py", line 437, in close
celery-beat | 2025-04-10 09:06:50.076 |     self.sync()
celery-beat | 2025-04-10 09:06:50.076 |   File "/usr/local/lib/python3.11/site-packages/django_celery_beat/schedulers.py", line 303, in sync
celery-beat | 2025-04-10 09:06:50.076 |     self._schedule[name].save()
celery-beat | 2025-04-10 09:06:50.076 |   File "/usr/local/lib/python3.11/site-packages/django_celery_beat/schedulers.py", line 161, in save
celery-beat | 2025-04-10 09:06:50.076 |     obj.save()
celery-beat | 2025-04-10 09:06:50.076 |   File "/usr/local/lib/python3.11/site-packages/django_celery_beat/models.py", line 620, in save
celery-beat | 2025-04-10 09:06:50.076 |     super().save(*args, **kwargs)
celery-beat | 2025-04-10 09:06:50.076 |   File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 892, in save
celery-beat | 2025-04-10 09:06:50.076 |     self.save_base(
celery-beat | 2025-04-10 09:06:50.076 |   File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 998, in save_base
celery-beat | 2025-04-10 09:06:50.076 |     updated = self._save_table(
celery-beat | 2025-04-10 09:06:50.076 |               ^^^^^^^^^^^^^^^^^
celery-beat | 2025-04-10 09:06:50.076 |   File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1130, in _save_table
celery-beat | 2025-04-10 09:06:50.076 |     updated = self._do_update(
celery-beat | 2025-04-10 09:06:50.076 |               ^^^^^^^^^^^^^^^^
celery-beat | 2025-04-10 09:06:50.076 |   File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1195, in _do_update
celery-beat | 2025-04-10 09:06:50.076 |     return filtered._update(values) > 0
celery-beat | 2025-04-10 09:06:50.076 |            ^^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-04-10 09:06:50.076 |   File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1278, in _update
celery-beat | 2025-04-10 09:06:50.076 |     return query.get_compiler(self.db).execute_sql(CURSOR)
celery-beat | 2025-04-10 09:06:50.076 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-04-10 09:06:50.076 |   File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 2003, in execute_sql
celery-beat | 2025-04-10 09:06:50.076 |     cursor = super().execute_sql(result_type)
celery-beat | 2025-04-10 09:06:50.076 |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-04-10 09:06:50.076 |   File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1561, in execute_sql
celery-beat | 2025-04-10 09:06:50.076 |     sql, params = self.as_sql()
celery-beat | 2025-04-10 09:06:50.076 |                   ^^^^^^^^^^^^^
celery-beat | 2025-04-10 09:06:50.076 |   File "/usr/local/lib/python3.11/site-packages/django/db/backends/mysql/compiler.py", line 57, in as_sql
celery-beat | 2025-04-10 09:06:50.076 |     update_query, update_params = super().as_sql()
celery-beat | 2025-04-10 09:06:50.076 |                                   ^^^^^^^^^^^^^^^^
celery-beat | 2025-04-10 09:06:50.076 |   File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1966, in as_sql
celery-beat | 2025-04-10 09:06:50.076 |     val = field.get_db_prep_save(val, connection=self.connection)
celery-beat | 2025-04-10 09:06:50.076 |           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-04-10 09:06:50.076 |   File "/usr/local/lib/python3.11/site-packages/django/db/models/fields/__init__.py", line 1008, in get_db_prep_save
celery-beat | 2025-04-10 09:06:50.076 |     return self.get_db_prep_value(value, connection=connection, prepared=False)
celery-beat | 2025-04-10 09:06:50.076 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-04-10 09:06:50.076 |   File "/usr/local/lib/python3.11/site-packages/django/db/models/fields/__init__.py", line 1678, in get_db_prep_value
celery-beat | 2025-04-10 09:06:50.076 |     return connection.ops.adapt_datetimefield_value(value)
celery-beat | 2025-04-10 09:06:50.076 |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery-beat | 2025-04-10 09:06:50.076 |   File "/usr/local/lib/python3.11/site-packages/django/db/backends/mysql/operations.py", line 267, in adapt_datetimefield_value
celery-beat | 2025-04-10 09:06:50.076 |     raise ValueError(
celery-beat | 2025-04-10 09:06:50.076 | ValueError: MySQL backend does not support timezone-aware datetimes when USE_TZ is False.
celery-beat | 2025-04-10 09:06:50.076 | [2025-04-10 09:06:50,076: WARNING/MainProcess] Traceback (most recent call last):
celery-beat | 2025-04-10 09:06:50.076 | [2025-04-10 09:06:50,076: WARNING/MainProcess]   File "/usr/local/bin/celery", line 8, in <module>
celery-beat | 2025-04-10 09:06:50.076 | [2025-04-10 09:06:50,076: WARNING/MainProcess]     
celery-beat | 2025-04-10 09:06:50.076 | [2025-04-10 09:06:50,076: WARNING/MainProcess] sys.exit(main())
celery-beat | 2025-04-10 09:06:50.076 | [2025-04-10 09:06:50,076: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.076 | [2025-04-10 09:06:50,076: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.076 | [2025-04-10 09:06:50,076: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.076 | [2025-04-10 09:06:50,076: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.076 | [2025-04-10 09:06:50,076: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.076 | [2025-04-10 09:06:50,076: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.076 | [2025-04-10 09:06:50,076: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.076 | [2025-04-10 09:06:50,076: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.076 | [2025-04-10 09:06:50,076: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.076 | [2025-04-10 09:06:50,076: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.076 | [2025-04-10 09:06:50,076: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.076 | [2025-04-10 09:06:50,076: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.076 | [2025-04-10 09:06:50,076: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.076 | [2025-04-10 09:06:50,076: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.076 | [2025-04-10 09:06:50,076: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.076 | [2025-04-10 09:06:50,076: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.076 | [2025-04-10 09:06:50,076: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.076 | [2025-04-10 09:06:50,076: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.076 | [2025-04-10 09:06:50,076: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.076 | [2025-04-10 09:06:50,076: WARNING/MainProcess]   File "/usr/local/lib/python3.11/site-packages/celery/__main__.py", line 15, in main
celery-beat | 2025-04-10 09:06:50.077 | [2025-04-10 09:06:50,077: WARNING/MainProcess]     
celery-beat | 2025-04-10 09:06:50.077 | [2025-04-10 09:06:50,077: WARNING/MainProcess] sys.exit(_main())
celery-beat | 2025-04-10 09:06:50.077 | [2025-04-10 09:06:50,077: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.077 | [2025-04-10 09:06:50,077: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.077 | [2025-04-10 09:06:50,077: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.077 | [2025-04-10 09:06:50,077: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.077 | [2025-04-10 09:06:50,077: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.077 | [2025-04-10 09:06:50,077: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.077 | [2025-04-10 09:06:50,077: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.077 | [2025-04-10 09:06:50,077: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.077 | [2025-04-10 09:06:50,077: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.077 | [2025-04-10 09:06:50,077: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.077 | [2025-04-10 09:06:50,077: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.077 | [2025-04-10 09:06:50,077: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.077 | [2025-04-10 09:06:50,077: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.077 | [2025-04-10 09:06:50,077: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.077 | [2025-04-10 09:06:50,077: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.077 | [2025-04-10 09:06:50,077: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.077 | [2025-04-10 09:06:50,077: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.077 | [2025-04-10 09:06:50,077: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.077 | [2025-04-10 09:06:50,077: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.077 | [2025-04-10 09:06:50,077: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.077 | [2025-04-10 09:06:50,077: WARNING/MainProcess]   File "/usr/local/lib/python3.11/site-packages/celery/bin/celery.py", line 236, in main
celery-beat | 2025-04-10 09:06:50.078 | [2025-04-10 09:06:50,078: WARNING/MainProcess]     
celery-beat | 2025-04-10 09:06:50.078 | [2025-04-10 09:06:50,078: WARNING/MainProcess] return celery(auto_envvar_prefix="CELERY")
celery-beat | 2025-04-10 09:06:50.078 | [2025-04-10 09:06:50,078: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.078 | [2025-04-10 09:06:50,078: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.078 | [2025-04-10 09:06:50,078: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.078 | [2025-04-10 09:06:50,078: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.078 | [2025-04-10 09:06:50,078: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.078 | [2025-04-10 09:06:50,078: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.078 | [2025-04-10 09:06:50,078: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.078 | [2025-04-10 09:06:50,078: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.078 | [2025-04-10 09:06:50,078: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.078 | [2025-04-10 09:06:50,078: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.078 | [2025-04-10 09:06:50,078: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.078 | [2025-04-10 09:06:50,078: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.078 | [2025-04-10 09:06:50,078: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.078 | [2025-04-10 09:06:50,078: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.078 | [2025-04-10 09:06:50,078: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.078 | [2025-04-10 09:06:50,078: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.078 | [2025-04-10 09:06:50,078: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.078 | [2025-04-10 09:06:50,078: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.078 | [2025-04-10 09:06:50,078: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.079 | [2025-04-10 09:06:50,078: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.079 | [2025-04-10 09:06:50,078: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.079 | [2025-04-10 09:06:50,078: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.079 | [2025-04-10 09:06:50,078: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.079 | [2025-04-10 09:06:50,079: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.079 | [2025-04-10 09:06:50,079: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.079 | [2025-04-10 09:06:50,079: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.079 | [2025-04-10 09:06:50,079: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.079 | [2025-04-10 09:06:50,079: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.079 | [2025-04-10 09:06:50,079: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.079 | [2025-04-10 09:06:50,079: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.079 | [2025-04-10 09:06:50,079: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.079 | [2025-04-10 09:06:50,079: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.079 | [2025-04-10 09:06:50,079: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.079 | [2025-04-10 09:06:50,079: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.079 | [2025-04-10 09:06:50,079: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.079 | [2025-04-10 09:06:50,079: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.079 | [2025-04-10 09:06:50,079: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.079 | [2025-04-10 09:06:50,079: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.079 | [2025-04-10 09:06:50,079: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.079 | [2025-04-10 09:06:50,079: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.079 | [2025-04-10 09:06:50,079: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.079 | [2025-04-10 09:06:50,079: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.079 | [2025-04-10 09:06:50,079: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.079 | [2025-04-10 09:06:50,079: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.079 | [2025-04-10 09:06:50,079: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.079 | [2025-04-10 09:06:50,079: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.079 | [2025-04-10 09:06:50,079: WARNING/MainProcess]   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1157, in __call__
celery-beat | 2025-04-10 09:06:50.080 | [2025-04-10 09:06:50,080: WARNING/MainProcess]     
celery-beat | 2025-04-10 09:06:50.080 | [2025-04-10 09:06:50,080: WARNING/MainProcess] return self.main(*args, **kwargs)
celery-beat | 2025-04-10 09:06:50.080 | [2025-04-10 09:06:50,080: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.080 | [2025-04-10 09:06:50,080: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.080 | [2025-04-10 09:06:50,080: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.080 | [2025-04-10 09:06:50,080: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.080 | [2025-04-10 09:06:50,080: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.080 | [2025-04-10 09:06:50,080: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.080 | [2025-04-10 09:06:50,080: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.080 | [2025-04-10 09:06:50,080: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.080 | [2025-04-10 09:06:50,080: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.080 | [2025-04-10 09:06:50,080: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.080 | [2025-04-10 09:06:50,080: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.080 | [2025-04-10 09:06:50,080: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.080 | [2025-04-10 09:06:50,080: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.080 | [2025-04-10 09:06:50,080: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.080 | [2025-04-10 09:06:50,080: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.080 | [2025-04-10 09:06:50,080: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.080 | [2025-04-10 09:06:50,080: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.080 | [2025-04-10 09:06:50,080: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.080 | [2025-04-10 09:06:50,080: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.080 | [2025-04-10 09:06:50,080: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.080 | [2025-04-10 09:06:50,080: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.081 | [2025-04-10 09:06:50,080: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.081 | [2025-04-10 09:06:50,081: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.081 | [2025-04-10 09:06:50,081: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.081 | [2025-04-10 09:06:50,081: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.081 | [2025-04-10 09:06:50,081: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.081 | [2025-04-10 09:06:50,081: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.081 | [2025-04-10 09:06:50,081: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.081 | [2025-04-10 09:06:50,081: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.081 | [2025-04-10 09:06:50,081: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.081 | [2025-04-10 09:06:50,081: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.081 | [2025-04-10 09:06:50,081: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.081 | [2025-04-10 09:06:50,081: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.081 | [2025-04-10 09:06:50,081: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.081 | [2025-04-10 09:06:50,081: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.081 | [2025-04-10 09:06:50,081: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.081 | [2025-04-10 09:06:50,081: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.081 | [2025-04-10 09:06:50,081: WARNING/MainProcess]   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1078, in main
celery-beat | 2025-04-10 09:06:50.081 | [2025-04-10 09:06:50,081: WARNING/MainProcess]     
celery-beat | 2025-04-10 09:06:50.081 | [2025-04-10 09:06:50,081: WARNING/MainProcess] rv = self.invoke(ctx)
celery-beat | 2025-04-10 09:06:50.081 | [2025-04-10 09:06:50,081: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.081 | [2025-04-10 09:06:50,081: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.081 | [2025-04-10 09:06:50,081: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.081 | [2025-04-10 09:06:50,081: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.081 | [2025-04-10 09:06:50,081: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.081 | [2025-04-10 09:06:50,081: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.081 | [2025-04-10 09:06:50,081: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.082 | [2025-04-10 09:06:50,081: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.082 | [2025-04-10 09:06:50,081: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.082 | [2025-04-10 09:06:50,081: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.082 | [2025-04-10 09:06:50,082: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.082 | [2025-04-10 09:06:50,082: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.082 | [2025-04-10 09:06:50,082: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.082 | [2025-04-10 09:06:50,082: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.082 | [2025-04-10 09:06:50,082: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.082 | [2025-04-10 09:06:50,082: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.082 | [2025-04-10 09:06:50,082: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.082 | [2025-04-10 09:06:50,082: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.082 | [2025-04-10 09:06:50,082: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.082 | [2025-04-10 09:06:50,082: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.082 | [2025-04-10 09:06:50,082: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.082 | [2025-04-10 09:06:50,082: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.082 | [2025-04-10 09:06:50,082: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.082 | [2025-04-10 09:06:50,082: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.082 | [2025-04-10 09:06:50,082: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.082 | [2025-04-10 09:06:50,082: WARNING/MainProcess]   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1688, in invoke
celery-beat | 2025-04-10 09:06:50.082 | [2025-04-10 09:06:50,082: WARNING/MainProcess]     
celery-beat | 2025-04-10 09:06:50.082 | [2025-04-10 09:06:50,082: WARNING/MainProcess] return _process_result(sub_ctx.command.invoke(sub_ctx))
celery-beat | 2025-04-10 09:06:50.082 | [2025-04-10 09:06:50,082: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.082 | [2025-04-10 09:06:50,082: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.083 | [2025-04-10 09:06:50,082: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.083 | [2025-04-10 09:06:50,082: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.083 | [2025-04-10 09:06:50,083: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.083 | [2025-04-10 09:06:50,083: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.083 | [2025-04-10 09:06:50,083: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.083 | [2025-04-10 09:06:50,083: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.083 | [2025-04-10 09:06:50,083: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.083 | [2025-04-10 09:06:50,083: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.083 | [2025-04-10 09:06:50,083: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.083 | [2025-04-10 09:06:50,083: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.083 | [2025-04-10 09:06:50,083: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.083 | [2025-04-10 09:06:50,083: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.083 | [2025-04-10 09:06:50,083: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.083 | [2025-04-10 09:06:50,083: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.083 | [2025-04-10 09:06:50,083: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.083 | [2025-04-10 09:06:50,083: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.083 | [2025-04-10 09:06:50,083: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.083 | [2025-04-10 09:06:50,083: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.083 | [2025-04-10 09:06:50,083: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.083 | [2025-04-10 09:06:50,083: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.083 | [2025-04-10 09:06:50,083: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.083 | [2025-04-10 09:06:50,083: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.083 | [2025-04-10 09:06:50,083: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.084 | [2025-04-10 09:06:50,083: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.084 | [2025-04-10 09:06:50,083: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.084 | [2025-04-10 09:06:50,084: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.084 | [2025-04-10 09:06:50,084: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.084 | [2025-04-10 09:06:50,084: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.084 | [2025-04-10 09:06:50,084: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.084 | [2025-04-10 09:06:50,084: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.084 | [2025-04-10 09:06:50,084: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.084 | [2025-04-10 09:06:50,084: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.084 | [2025-04-10 09:06:50,084: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.084 | [2025-04-10 09:06:50,084: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.084 | [2025-04-10 09:06:50,084: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.084 | [2025-04-10 09:06:50,084: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.084 | [2025-04-10 09:06:50,084: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.084 | [2025-04-10 09:06:50,084: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.084 | [2025-04-10 09:06:50,084: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.084 | [2025-04-10 09:06:50,084: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.084 | [2025-04-10 09:06:50,084: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.084 | [2025-04-10 09:06:50,084: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.085 | [2025-04-10 09:06:50,084: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.085 | [2025-04-10 09:06:50,084: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.085 | [2025-04-10 09:06:50,085: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.085 | [2025-04-10 09:06:50,085: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.085 | [2025-04-10 09:06:50,085: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.085 | [2025-04-10 09:06:50,085: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.085 | [2025-04-10 09:06:50,085: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.085 | [2025-04-10 09:06:50,085: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.085 | [2025-04-10 09:06:50,085: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.085 | [2025-04-10 09:06:50,085: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.085 | [2025-04-10 09:06:50,085: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.085 | [2025-04-10 09:06:50,085: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.086 | [2025-04-10 09:06:50,085: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.086 | [2025-04-10 09:06:50,085: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.086 | [2025-04-10 09:06:50,085: WARNING/MainProcess]   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 1434, in invoke
celery-beat | 2025-04-10 09:06:50.086 | [2025-04-10 09:06:50,086: WARNING/MainProcess]     
celery-beat | 2025-04-10 09:06:50.086 | [2025-04-10 09:06:50,086: WARNING/MainProcess] return ctx.invoke(self.callback, **ctx.params)
celery-beat | 2025-04-10 09:06:50.086 | [2025-04-10 09:06:50,086: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.086 | [2025-04-10 09:06:50,086: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.086 | [2025-04-10 09:06:50,086: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.086 | [2025-04-10 09:06:50,086: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.086 | [2025-04-10 09:06:50,086: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.086 | [2025-04-10 09:06:50,086: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.086 | [2025-04-10 09:06:50,086: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.086 | [2025-04-10 09:06:50,086: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.086 | [2025-04-10 09:06:50,086: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.086 | [2025-04-10 09:06:50,086: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.086 | [2025-04-10 09:06:50,086: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.086 | [2025-04-10 09:06:50,086: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.086 | [2025-04-10 09:06:50,086: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.086 | [2025-04-10 09:06:50,086: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.086 | [2025-04-10 09:06:50,086: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.086 | [2025-04-10 09:06:50,086: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.086 | [2025-04-10 09:06:50,086: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.087 | [2025-04-10 09:06:50,086: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.087 | [2025-04-10 09:06:50,087: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.087 | [2025-04-10 09:06:50,087: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.087 | [2025-04-10 09:06:50,087: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.087 | [2025-04-10 09:06:50,087: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.087 | [2025-04-10 09:06:50,087: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.087 | [2025-04-10 09:06:50,087: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.087 | [2025-04-10 09:06:50,087: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.087 | [2025-04-10 09:06:50,087: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.087 | [2025-04-10 09:06:50,087: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.087 | [2025-04-10 09:06:50,087: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.087 | [2025-04-10 09:06:50,087: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.087 | [2025-04-10 09:06:50,087: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.087 | [2025-04-10 09:06:50,087: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.087 | [2025-04-10 09:06:50,087: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.087 | [2025-04-10 09:06:50,087: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.087 | [2025-04-10 09:06:50,087: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.087 | [2025-04-10 09:06:50,087: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.087 | [2025-04-10 09:06:50,087: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.088 | [2025-04-10 09:06:50,087: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.088 | [2025-04-10 09:06:50,087: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.088 | [2025-04-10 09:06:50,088: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.088 | [2025-04-10 09:06:50,088: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.088 | [2025-04-10 09:06:50,088: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.088 | [2025-04-10 09:06:50,088: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.088 | [2025-04-10 09:06:50,088: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.088 | [2025-04-10 09:06:50,088: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.088 | [2025-04-10 09:06:50,088: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.088 | [2025-04-10 09:06:50,088: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.088 | [2025-04-10 09:06:50,088: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.088 | [2025-04-10 09:06:50,088: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.088 | [2025-04-10 09:06:50,088: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.088 | [2025-04-10 09:06:50,088: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.089 | [2025-04-10 09:06:50,089: WARNING/MainProcess]   File "/usr/local/lib/python3.11/site-packages/click/core.py", line 783, in invoke
celery-beat | 2025-04-10 09:06:50.089 | [2025-04-10 09:06:50,089: WARNING/MainProcess]     
celery-beat | 2025-04-10 09:06:50.089 | [2025-04-10 09:06:50,089: WARNING/MainProcess] return __callback(*args, **kwargs)
celery-beat | 2025-04-10 09:06:50.089 | [2025-04-10 09:06:50,089: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.089 | [2025-04-10 09:06:50,089: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.089 | [2025-04-10 09:06:50,089: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.089 | [2025-04-10 09:06:50,089: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.089 | [2025-04-10 09:06:50,089: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.089 | [2025-04-10 09:06:50,089: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.089 | [2025-04-10 09:06:50,089: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.089 | [2025-04-10 09:06:50,089: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.089 | [2025-04-10 09:06:50,089: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.089 | [2025-04-10 09:06:50,089: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.089 | [2025-04-10 09:06:50,089: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.089 | [2025-04-10 09:06:50,089: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.090 | [2025-04-10 09:06:50,089: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.090 | [2025-04-10 09:06:50,089: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.090 | [2025-04-10 09:06:50,090: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.090 | [2025-04-10 09:06:50,090: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.090 | [2025-04-10 09:06:50,090: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.090 | [2025-04-10 09:06:50,090: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.090 | [2025-04-10 09:06:50,090: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.090 | [2025-04-10 09:06:50,090: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.090 | [2025-04-10 09:06:50,090: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.090 | [2025-04-10 09:06:50,090: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.090 | [2025-04-10 09:06:50,090: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.090 | [2025-04-10 09:06:50,090: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.090 | [2025-04-10 09:06:50,090: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.090 | [2025-04-10 09:06:50,090: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.090 | [2025-04-10 09:06:50,090: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.090 | [2025-04-10 09:06:50,090: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.090 | [2025-04-10 09:06:50,090: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.090 | [2025-04-10 09:06:50,090: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.090 | [2025-04-10 09:06:50,090: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.090 | [2025-04-10 09:06:50,090: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.090 | [2025-04-10 09:06:50,090: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.090 | [2025-04-10 09:06:50,090: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.090 | [2025-04-10 09:06:50,090: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.090 | [2025-04-10 09:06:50,090: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.090 | [2025-04-10 09:06:50,090: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.090 | [2025-04-10 09:06:50,090: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.090 | [2025-04-10 09:06:50,090: WARNING/MainProcess]   File "/usr/local/lib/python3.11/site-packages/click/decorators.py", line 33, in new_func
celery-beat | 2025-04-10 09:06:50.091 | [2025-04-10 09:06:50,091: WARNING/MainProcess]     
celery-beat | 2025-04-10 09:06:50.091 | [2025-04-10 09:06:50,091: WARNING/MainProcess] return f(get_current_context(), *args, **kwargs)
celery-beat | 2025-04-10 09:06:50.091 | [2025-04-10 09:06:50,091: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.091 | [2025-04-10 09:06:50,091: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.091 | [2025-04-10 09:06:50,091: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.091 | [2025-04-10 09:06:50,091: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.091 | [2025-04-10 09:06:50,091: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.091 | [2025-04-10 09:06:50,091: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.091 | [2025-04-10 09:06:50,091: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.091 | [2025-04-10 09:06:50,091: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.091 | [2025-04-10 09:06:50,091: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.091 | [2025-04-10 09:06:50,091: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.091 | [2025-04-10 09:06:50,091: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.091 | [2025-04-10 09:06:50,091: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.091 | [2025-04-10 09:06:50,091: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.091 | [2025-04-10 09:06:50,091: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.091 | [2025-04-10 09:06:50,091: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.091 | [2025-04-10 09:06:50,091: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.091 | [2025-04-10 09:06:50,091: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.091 | [2025-04-10 09:06:50,091: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.091 | [2025-04-10 09:06:50,091: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.091 | [2025-04-10 09:06:50,091: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.092 | [2025-04-10 09:06:50,091: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.092 | [2025-04-10 09:06:50,091: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.092 | [2025-04-10 09:06:50,091: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.092 | [2025-04-10 09:06:50,091: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.092 | [2025-04-10 09:06:50,092: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.092 | [2025-04-10 09:06:50,092: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.092 | [2025-04-10 09:06:50,092: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.092 | [2025-04-10 09:06:50,092: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.092 | [2025-04-10 09:06:50,092: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.092 | [2025-04-10 09:06:50,092: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.092 | [2025-04-10 09:06:50,092: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.092 | [2025-04-10 09:06:50,092: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.092 | [2025-04-10 09:06:50,092: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.092 | [2025-04-10 09:06:50,092: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.092 | [2025-04-10 09:06:50,092: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.092 | [2025-04-10 09:06:50,092: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.092 | [2025-04-10 09:06:50,092: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.092 | [2025-04-10 09:06:50,092: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.092 | [2025-04-10 09:06:50,092: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.092 | [2025-04-10 09:06:50,092: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.092 | [2025-04-10 09:06:50,092: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.092 | [2025-04-10 09:06:50,092: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.092 | [2025-04-10 09:06:50,092: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.092 | [2025-04-10 09:06:50,092: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.092 | [2025-04-10 09:06:50,092: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.092 | [2025-04-10 09:06:50,092: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.092 | [2025-04-10 09:06:50,092: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.092 | [2025-04-10 09:06:50,092: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.092 | [2025-04-10 09:06:50,092: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.092 | [2025-04-10 09:06:50,092: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.092 | [2025-04-10 09:06:50,092: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.092 | [2025-04-10 09:06:50,092: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.092 | [2025-04-10 09:06:50,092: WARNING/MainProcess]   File "/usr/local/lib/python3.11/site-packages/celery/bin/base.py", line 135, in caller
celery-beat | 2025-04-10 09:06:50.093 | [2025-04-10 09:06:50,093: WARNING/MainProcess]     
celery-beat | 2025-04-10 09:06:50.093 | [2025-04-10 09:06:50,093: WARNING/MainProcess] return f(ctx, *args, **kwargs)
celery-beat | 2025-04-10 09:06:50.093 | [2025-04-10 09:06:50,093: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.093 | [2025-04-10 09:06:50,093: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.093 | [2025-04-10 09:06:50,093: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.093 | [2025-04-10 09:06:50,093: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.093 | [2025-04-10 09:06:50,093: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.093 | [2025-04-10 09:06:50,093: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.093 | [2025-04-10 09:06:50,093: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.093 | [2025-04-10 09:06:50,093: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.093 | [2025-04-10 09:06:50,093: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.093 | [2025-04-10 09:06:50,093: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.093 | [2025-04-10 09:06:50,093: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.093 | [2025-04-10 09:06:50,093: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.093 | [2025-04-10 09:06:50,093: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.093 | [2025-04-10 09:06:50,093: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.093 | [2025-04-10 09:06:50,093: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.093 | [2025-04-10 09:06:50,093: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.093 | [2025-04-10 09:06:50,093: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.093 | [2025-04-10 09:06:50,093: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.093 | [2025-04-10 09:06:50,093: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.093 | [2025-04-10 09:06:50,093: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.093 | [2025-04-10 09:06:50,093: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.093 | [2025-04-10 09:06:50,093: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.093 | [2025-04-10 09:06:50,093: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.093 | [2025-04-10 09:06:50,093: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.093 | [2025-04-10 09:06:50,093: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.093 | [2025-04-10 09:06:50,093: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.093 | [2025-04-10 09:06:50,093: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.093 | [2025-04-10 09:06:50,093: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.093 | [2025-04-10 09:06:50,093: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.093 | [2025-04-10 09:06:50,093: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.093 | [2025-04-10 09:06:50,093: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.094 | [2025-04-10 09:06:50,093: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.094 | [2025-04-10 09:06:50,093: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.094 | [2025-04-10 09:06:50,093: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.094 | [2025-04-10 09:06:50,094: WARNING/MainProcess]   File "/usr/local/lib/python3.11/site-packages/celery/bin/beat.py", line 72, in beat
celery-beat | 2025-04-10 09:06:50.094 | [2025-04-10 09:06:50,094: WARNING/MainProcess]     
celery-beat | 2025-04-10 09:06:50.094 | [2025-04-10 09:06:50,094: WARNING/MainProcess] return beat().run()
celery-beat | 2025-04-10 09:06:50.094 | [2025-04-10 09:06:50,094: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.094 | [2025-04-10 09:06:50,094: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.094 | [2025-04-10 09:06:50,094: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.094 | [2025-04-10 09:06:50,094: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.094 | [2025-04-10 09:06:50,094: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.094 | [2025-04-10 09:06:50,094: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.094 | [2025-04-10 09:06:50,094: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.094 | [2025-04-10 09:06:50,094: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.094 | [2025-04-10 09:06:50,094: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.094 | [2025-04-10 09:06:50,094: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.094 | [2025-04-10 09:06:50,094: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.094 | [2025-04-10 09:06:50,094: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.094 | [2025-04-10 09:06:50,094: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.094 | [2025-04-10 09:06:50,094: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.094 | [2025-04-10 09:06:50,094: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.094 | [2025-04-10 09:06:50,094: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.095 | [2025-04-10 09:06:50,094: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.095 | [2025-04-10 09:06:50,094: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.095 | [2025-04-10 09:06:50,094: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.095 | [2025-04-10 09:06:50,095: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.095 | [2025-04-10 09:06:50,095: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.095 | [2025-04-10 09:06:50,095: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.095 | [2025-04-10 09:06:50,095: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.095 | [2025-04-10 09:06:50,095: WARNING/MainProcess]   File "/usr/local/lib/python3.11/site-packages/celery/apps/beat.py", line 84, in run
celery-beat | 2025-04-10 09:06:50.095 | [2025-04-10 09:06:50,095: WARNING/MainProcess]     
celery-beat | 2025-04-10 09:06:50.095 | [2025-04-10 09:06:50,095: WARNING/MainProcess] self.start_scheduler()
celery-beat | 2025-04-10 09:06:50.095 | [2025-04-10 09:06:50,095: WARNING/MainProcess]   File "/usr/local/lib/python3.11/site-packages/celery/apps/beat.py", line 113, in start_scheduler
celery-beat | 2025-04-10 09:06:50.095 | [2025-04-10 09:06:50,095: WARNING/MainProcess]     
celery-beat | 2025-04-10 09:06:50.095 | [2025-04-10 09:06:50,095: WARNING/MainProcess] service.start()
celery-beat | 2025-04-10 09:06:50.095 | [2025-04-10 09:06:50,095: WARNING/MainProcess]   File "/usr/local/lib/python3.11/site-packages/celery/beat.py", line 647, in start
celery-beat | 2025-04-10 09:06:50.095 | [2025-04-10 09:06:50,095: WARNING/MainProcess]     
celery-beat | 2025-04-10 09:06:50.095 | [2025-04-10 09:06:50,095: WARNING/MainProcess] time.sleep(interval)
celery-beat | 2025-04-10 09:06:50.095 | [2025-04-10 09:06:50,095: WARNING/MainProcess]   File "/usr/local/lib/python3.11/site-packages/celery/apps/beat.py", line 158, in _sync
celery-beat | 2025-04-10 09:06:50.095 | [2025-04-10 09:06:50,095: WARNING/MainProcess]     
celery-beat | 2025-04-10 09:06:50.095 | [2025-04-10 09:06:50,095: WARNING/MainProcess] service.sync()
celery-beat | 2025-04-10 09:06:50.095 | [2025-04-10 09:06:50,095: WARNING/MainProcess]   File "/usr/local/lib/python3.11/site-packages/celery/beat.py", line 656, in sync
celery-beat | 2025-04-10 09:06:50.096 | [2025-04-10 09:06:50,095: WARNING/MainProcess]     
celery-beat | 2025-04-10 09:06:50.096 | [2025-04-10 09:06:50,096: WARNING/MainProcess] self.scheduler.close()
celery-beat | 2025-04-10 09:06:50.096 | [2025-04-10 09:06:50,096: WARNING/MainProcess]   File "/usr/local/lib/python3.11/site-packages/celery/beat.py", line 437, in close
celery-beat | 2025-04-10 09:06:50.096 | [2025-04-10 09:06:50,096: WARNING/MainProcess]     
celery-beat | 2025-04-10 09:06:50.096 | [2025-04-10 09:06:50,096: WARNING/MainProcess] self.sync()
celery-beat | 2025-04-10 09:06:50.096 | [2025-04-10 09:06:50,096: WARNING/MainProcess]   File "/usr/local/lib/python3.11/site-packages/django_celery_beat/schedulers.py", line 303, in sync
celery-beat | 2025-04-10 09:06:50.096 | [2025-04-10 09:06:50,096: WARNING/MainProcess]     
celery-beat | 2025-04-10 09:06:50.096 | [2025-04-10 09:06:50,096: WARNING/MainProcess] self._schedule[name].save()
celery-beat | 2025-04-10 09:06:50.096 | [2025-04-10 09:06:50,096: WARNING/MainProcess]   File "/usr/local/lib/python3.11/site-packages/django_celery_beat/schedulers.py", line 161, in save
celery-beat | 2025-04-10 09:06:50.096 | [2025-04-10 09:06:50,096: WARNING/MainProcess]     
celery-beat | 2025-04-10 09:06:50.096 | [2025-04-10 09:06:50,096: WARNING/MainProcess] obj.save()
celery-beat | 2025-04-10 09:06:50.096 | [2025-04-10 09:06:50,096: WARNING/MainProcess]   File "/usr/local/lib/python3.11/site-packages/django_celery_beat/models.py", line 620, in save
celery-beat | 2025-04-10 09:06:50.096 | [2025-04-10 09:06:50,096: WARNING/MainProcess]     
celery-beat | 2025-04-10 09:06:50.096 | [2025-04-10 09:06:50,096: WARNING/MainProcess] super().save(*args, **kwargs)
celery-beat | 2025-04-10 09:06:50.096 | [2025-04-10 09:06:50,096: WARNING/MainProcess]   File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 892, in save
celery-beat | 2025-04-10 09:06:50.096 | [2025-04-10 09:06:50,096: WARNING/MainProcess]     
celery-beat | 2025-04-10 09:06:50.096 | [2025-04-10 09:06:50,096: WARNING/MainProcess] self.save_base(
celery-beat | 2025-04-10 09:06:50.096 | [2025-04-10 09:06:50,096: WARNING/MainProcess]   File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 998, in save_base
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,096: WARNING/MainProcess]     
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,096: WARNING/MainProcess] updated = self._save_table(
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,096: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,096: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,097: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,097: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,097: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,097: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,097: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,097: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,097: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,097: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,097: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,097: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,097: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,097: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,097: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,097: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,097: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,097: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,097: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,097: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,097: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,097: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,097: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,097: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,097: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,097: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,097: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,097: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,097: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,097: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,097: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,097: WARNING/MainProcess]   File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1130, in _save_table
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,097: WARNING/MainProcess]     
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,097: WARNING/MainProcess] updated = self._do_update(
celery-beat | 2025-04-10 09:06:50.097 | [2025-04-10 09:06:50,097: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,097: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,097: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess]   File "/usr/local/lib/python3.11/site-packages/django/db/models/base.py", line 1195, in _do_update
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess]     
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess] return filtered._update(values) > 0
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.098 | [2025-04-10 09:06:50,098: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.099 | [2025-04-10 09:06:50,098: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.099 | [2025-04-10 09:06:50,098: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.099 | [2025-04-10 09:06:50,099: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.099 | [2025-04-10 09:06:50,099: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.099 | [2025-04-10 09:06:50,099: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.099 | [2025-04-10 09:06:50,099: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.099 | [2025-04-10 09:06:50,099: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.099 | [2025-04-10 09:06:50,099: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.099 | [2025-04-10 09:06:50,099: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.099 | [2025-04-10 09:06:50,099: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.099 | [2025-04-10 09:06:50,099: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.099 | [2025-04-10 09:06:50,099: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.099 | [2025-04-10 09:06:50,099: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.099 | [2025-04-10 09:06:50,099: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.099 | [2025-04-10 09:06:50,099: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.099 | [2025-04-10 09:06:50,099: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.099 | [2025-04-10 09:06:50,099: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.099 | [2025-04-10 09:06:50,099: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.099 | [2025-04-10 09:06:50,099: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.099 | [2025-04-10 09:06:50,099: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.099 | [2025-04-10 09:06:50,099: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.099 | [2025-04-10 09:06:50,099: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.099 | [2025-04-10 09:06:50,099: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.099 | [2025-04-10 09:06:50,099: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.099 | [2025-04-10 09:06:50,099: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.099 | [2025-04-10 09:06:50,099: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.099 | [2025-04-10 09:06:50,099: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.099 | [2025-04-10 09:06:50,099: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.099 | [2025-04-10 09:06:50,099: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.099 | [2025-04-10 09:06:50,099: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.099 | [2025-04-10 09:06:50,099: WARNING/MainProcess]   File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 1278, in _update
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,099: WARNING/MainProcess]     
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,099: WARNING/MainProcess] return query.get_compiler(self.db).execute_sql(CURSOR)
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,099: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,099: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,099: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,099: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,099: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,099: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,099: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,099: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,099: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,099: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,099: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.100 | [2025-04-10 09:06:50,100: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.101 | [2025-04-10 09:06:50,100: WARNING/MainProcess]   File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 2003, in execute_sql
celery-beat | 2025-04-10 09:06:50.101 | [2025-04-10 09:06:50,101: WARNING/MainProcess]     
celery-beat | 2025-04-10 09:06:50.101 | [2025-04-10 09:06:50,101: WARNING/MainProcess] cursor = super().execute_sql(result_type)
celery-beat | 2025-04-10 09:06:50.101 | [2025-04-10 09:06:50,101: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.101 | [2025-04-10 09:06:50,101: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.101 | [2025-04-10 09:06:50,101: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.101 | [2025-04-10 09:06:50,101: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.101 | [2025-04-10 09:06:50,101: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.101 | [2025-04-10 09:06:50,101: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.101 | [2025-04-10 09:06:50,101: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.101 | [2025-04-10 09:06:50,101: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.101 | [2025-04-10 09:06:50,101: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.101 | [2025-04-10 09:06:50,101: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.101 | [2025-04-10 09:06:50,101: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.101 | [2025-04-10 09:06:50,101: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.101 | [2025-04-10 09:06:50,101: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.101 | [2025-04-10 09:06:50,101: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.101 | [2025-04-10 09:06:50,101: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.101 | [2025-04-10 09:06:50,101: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.101 | [2025-04-10 09:06:50,101: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.101 | [2025-04-10 09:06:50,101: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.101 | [2025-04-10 09:06:50,101: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.101 | [2025-04-10 09:06:50,101: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.101 | [2025-04-10 09:06:50,101: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.101 | [2025-04-10 09:06:50,101: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.101 | [2025-04-10 09:06:50,101: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.101 | [2025-04-10 09:06:50,101: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.101 | [2025-04-10 09:06:50,101: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.101 | [2025-04-10 09:06:50,101: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.101 | [2025-04-10 09:06:50,101: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.102 | [2025-04-10 09:06:50,101: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.102 | [2025-04-10 09:06:50,101: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.102 | [2025-04-10 09:06:50,102: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.102 | [2025-04-10 09:06:50,102: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.102 | [2025-04-10 09:06:50,102: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.102 | [2025-04-10 09:06:50,102: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.102 | [2025-04-10 09:06:50,102: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.102 | [2025-04-10 09:06:50,102: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.102 | [2025-04-10 09:06:50,102: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.102 | [2025-04-10 09:06:50,102: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.102 | [2025-04-10 09:06:50,102: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.102 | [2025-04-10 09:06:50,102: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.102 | [2025-04-10 09:06:50,102: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.102 | [2025-04-10 09:06:50,102: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.102 | [2025-04-10 09:06:50,102: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.102 | [2025-04-10 09:06:50,102: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.102 | [2025-04-10 09:06:50,102: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.102 | [2025-04-10 09:06:50,102: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.102 | [2025-04-10 09:06:50,102: WARNING/MainProcess]   File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1561, in execute_sql
celery-beat | 2025-04-10 09:06:50.102 | [2025-04-10 09:06:50,102: WARNING/MainProcess]     
celery-beat | 2025-04-10 09:06:50.102 | [2025-04-10 09:06:50,102: WARNING/MainProcess] sql, params = self.as_sql()
celery-beat | 2025-04-10 09:06:50.102 | [2025-04-10 09:06:50,102: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.102 | [2025-04-10 09:06:50,102: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.102 | [2025-04-10 09:06:50,102: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.102 | [2025-04-10 09:06:50,102: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.102 | [2025-04-10 09:06:50,102: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.102 | [2025-04-10 09:06:50,102: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.103 | [2025-04-10 09:06:50,102: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.103 | [2025-04-10 09:06:50,102: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.103 | [2025-04-10 09:06:50,103: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.103 | [2025-04-10 09:06:50,103: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.103 | [2025-04-10 09:06:50,103: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.103 | [2025-04-10 09:06:50,103: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.103 | [2025-04-10 09:06:50,103: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.103 | [2025-04-10 09:06:50,103: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.103 | [2025-04-10 09:06:50,103: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.103 | [2025-04-10 09:06:50,103: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.103 | [2025-04-10 09:06:50,103: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.103 | [2025-04-10 09:06:50,103: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.103 | [2025-04-10 09:06:50,103: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.103 | [2025-04-10 09:06:50,103: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.103 | [2025-04-10 09:06:50,103: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.103 | [2025-04-10 09:06:50,103: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.103 | [2025-04-10 09:06:50,103: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.103 | [2025-04-10 09:06:50,103: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.103 | [2025-04-10 09:06:50,103: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.103 | [2025-04-10 09:06:50,103: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.103 | [2025-04-10 09:06:50,103: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.103 | [2025-04-10 09:06:50,103: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.103 | [2025-04-10 09:06:50,103: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.103 | [2025-04-10 09:06:50,103: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.103 | [2025-04-10 09:06:50,103: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.103 | [2025-04-10 09:06:50,103: WARNING/MainProcess]   File "/usr/local/lib/python3.11/site-packages/django/db/backends/mysql/compiler.py", line 57, in as_sql
celery-beat | 2025-04-10 09:06:50.103 | [2025-04-10 09:06:50,103: WARNING/MainProcess]     
celery-beat | 2025-04-10 09:06:50.104 | [2025-04-10 09:06:50,103: WARNING/MainProcess] update_query, update_params = super().as_sql()
celery-beat | 2025-04-10 09:06:50.104 | [2025-04-10 09:06:50,104: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.104 | [2025-04-10 09:06:50,104: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.104 | [2025-04-10 09:06:50,104: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.104 | [2025-04-10 09:06:50,104: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.104 | [2025-04-10 09:06:50,104: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.104 | [2025-04-10 09:06:50,104: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.104 | [2025-04-10 09:06:50,104: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.104 | [2025-04-10 09:06:50,104: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.104 | [2025-04-10 09:06:50,104: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.104 | [2025-04-10 09:06:50,104: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.104 | [2025-04-10 09:06:50,104: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.104 | [2025-04-10 09:06:50,104: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.104 | [2025-04-10 09:06:50,104: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.104 | [2025-04-10 09:06:50,104: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.104 | [2025-04-10 09:06:50,104: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.104 | [2025-04-10 09:06:50,104: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.104 | [2025-04-10 09:06:50,104: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.104 | [2025-04-10 09:06:50,104: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.104 | [2025-04-10 09:06:50,104: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.104 | [2025-04-10 09:06:50,104: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.105 | [2025-04-10 09:06:50,104: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.105 | [2025-04-10 09:06:50,104: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.105 | [2025-04-10 09:06:50,104: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.105 | [2025-04-10 09:06:50,104: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.105 | [2025-04-10 09:06:50,104: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.105 | [2025-04-10 09:06:50,104: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.105 | [2025-04-10 09:06:50,105: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.105 | [2025-04-10 09:06:50,105: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.105 | [2025-04-10 09:06:50,105: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.105 | [2025-04-10 09:06:50,105: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.105 | [2025-04-10 09:06:50,105: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.105 | [2025-04-10 09:06:50,105: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.105 | [2025-04-10 09:06:50,105: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.105 | [2025-04-10 09:06:50,105: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.105 | [2025-04-10 09:06:50,105: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.105 | [2025-04-10 09:06:50,105: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.105 | [2025-04-10 09:06:50,105: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.105 | [2025-04-10 09:06:50,105: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.105 | [2025-04-10 09:06:50,105: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.105 | [2025-04-10 09:06:50,105: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.105 | [2025-04-10 09:06:50,105: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.105 | [2025-04-10 09:06:50,105: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.105 | [2025-04-10 09:06:50,105: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.105 | [2025-04-10 09:06:50,105: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.105 | [2025-04-10 09:06:50,105: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.105 | [2025-04-10 09:06:50,105: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.105 | [2025-04-10 09:06:50,105: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.105 | [2025-04-10 09:06:50,105: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.105 | [2025-04-10 09:06:50,105: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.105 | [2025-04-10 09:06:50,105: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.105 | [2025-04-10 09:06:50,105: WARNING/MainProcess]   File "/usr/local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1966, in as_sql
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,105: WARNING/MainProcess]     
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess] val = field.get_db_prep_save(val, connection=self.connection)
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.106 | [2025-04-10 09:06:50,106: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.107 | [2025-04-10 09:06:50,106: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.107 | [2025-04-10 09:06:50,106: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.107 | [2025-04-10 09:06:50,107: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.107 | [2025-04-10 09:06:50,107: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.107 | [2025-04-10 09:06:50,107: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.107 | [2025-04-10 09:06:50,107: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.107 | [2025-04-10 09:06:50,107: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.107 | [2025-04-10 09:06:50,107: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.107 | [2025-04-10 09:06:50,107: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.107 | [2025-04-10 09:06:50,107: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.107 | [2025-04-10 09:06:50,107: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.107 | [2025-04-10 09:06:50,107: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.107 | [2025-04-10 09:06:50,107: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.107 | [2025-04-10 09:06:50,107: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.107 | [2025-04-10 09:06:50,107: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.107 | [2025-04-10 09:06:50,107: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.107 | [2025-04-10 09:06:50,107: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.107 | [2025-04-10 09:06:50,107: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.107 | [2025-04-10 09:06:50,107: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.107 | [2025-04-10 09:06:50,107: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.107 | [2025-04-10 09:06:50,107: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.107 | [2025-04-10 09:06:50,107: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.107 | [2025-04-10 09:06:50,107: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.107 | [2025-04-10 09:06:50,107: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.107 | [2025-04-10 09:06:50,107: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.107 | [2025-04-10 09:06:50,107: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.107 | [2025-04-10 09:06:50,107: WARNING/MainProcess]   File "/usr/local/lib/python3.11/site-packages/django/db/models/fields/__init__.py", line 1008, in get_db_prep_save
celery-beat | 2025-04-10 09:06:50.108 | [2025-04-10 09:06:50,108: WARNING/MainProcess]     
celery-beat | 2025-04-10 09:06:50.108 | [2025-04-10 09:06:50,108: WARNING/MainProcess] return self.get_db_prep_value(value, connection=connection, prepared=False)
celery-beat | 2025-04-10 09:06:50.108 | [2025-04-10 09:06:50,108: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.108 | [2025-04-10 09:06:50,108: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.108 | [2025-04-10 09:06:50,108: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.108 | [2025-04-10 09:06:50,108: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.108 | [2025-04-10 09:06:50,108: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.108 | [2025-04-10 09:06:50,108: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.108 | [2025-04-10 09:06:50,108: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.108 | [2025-04-10 09:06:50,108: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.108 | [2025-04-10 09:06:50,108: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.108 | [2025-04-10 09:06:50,108: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.108 | [2025-04-10 09:06:50,108: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.108 | [2025-04-10 09:06:50,108: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.108 | [2025-04-10 09:06:50,108: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.108 | [2025-04-10 09:06:50,108: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.108 | [2025-04-10 09:06:50,108: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.108 | [2025-04-10 09:06:50,108: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.108 | [2025-04-10 09:06:50,108: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,108: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.109 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.110 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.110 | [2025-04-10 09:06:50,109: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.110 | [2025-04-10 09:06:50,110: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.110 | [2025-04-10 09:06:50,110: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.110 | [2025-04-10 09:06:50,110: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.110 | [2025-04-10 09:06:50,110: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.110 | [2025-04-10 09:06:50,110: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.110 | [2025-04-10 09:06:50,110: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.110 | [2025-04-10 09:06:50,110: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.110 | [2025-04-10 09:06:50,110: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.110 | [2025-04-10 09:06:50,110: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.110 | [2025-04-10 09:06:50,110: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.110 | [2025-04-10 09:06:50,110: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.110 | [2025-04-10 09:06:50,110: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.110 | [2025-04-10 09:06:50,110: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.110 | [2025-04-10 09:06:50,110: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.110 | [2025-04-10 09:06:50,110: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.110 | [2025-04-10 09:06:50,110: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.110 | [2025-04-10 09:06:50,110: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.110 | [2025-04-10 09:06:50,110: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.110 | [2025-04-10 09:06:50,110: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.110 | [2025-04-10 09:06:50,110: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.110 | [2025-04-10 09:06:50,110: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.110 | [2025-04-10 09:06:50,110: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.110 | [2025-04-10 09:06:50,110: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.110 | [2025-04-10 09:06:50,110: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.110 | [2025-04-10 09:06:50,110: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.110 | [2025-04-10 09:06:50,110: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.110 | [2025-04-10 09:06:50,110: WARNING/MainProcess]   File "/usr/local/lib/python3.11/site-packages/django/db/models/fields/__init__.py", line 1678, in get_db_prep_value
celery-beat | 2025-04-10 09:06:50.111 | [2025-04-10 09:06:50,110: WARNING/MainProcess]     
celery-beat | 2025-04-10 09:06:50.111 | [2025-04-10 09:06:50,111: WARNING/MainProcess] return connection.ops.adapt_datetimefield_value(value)
celery-beat | 2025-04-10 09:06:50.111 | [2025-04-10 09:06:50,111: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.111 | [2025-04-10 09:06:50,111: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.111 | [2025-04-10 09:06:50,111: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.111 | [2025-04-10 09:06:50,111: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.111 | [2025-04-10 09:06:50,111: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.111 | [2025-04-10 09:06:50,111: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.111 | [2025-04-10 09:06:50,111: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.111 | [2025-04-10 09:06:50,111: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.111 | [2025-04-10 09:06:50,111: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.111 | [2025-04-10 09:06:50,111: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.111 | [2025-04-10 09:06:50,111: WARNING/MainProcess]  
celery-beat | 2025-04-10 09:06:50.111 | [2025-04-10 09:06:50,111: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.111 | [2025-04-10 09:06:50,111: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.111 | [2025-04-10 09:06:50,111: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.111 | [2025-04-10 09:06:50,111: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.111 | [2025-04-10 09:06:50,111: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.111 | [2025-04-10 09:06:50,111: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.111 | [2025-04-10 09:06:50,111: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.111 | [2025-04-10 09:06:50,111: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.111 | [2025-04-10 09:06:50,111: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.111 | [2025-04-10 09:06:50,111: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.111 | [2025-04-10 09:06:50,111: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.111 | [2025-04-10 09:06:50,111: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.111 | [2025-04-10 09:06:50,111: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.111 | [2025-04-10 09:06:50,111: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.111 | [2025-04-10 09:06:50,111: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.111 | [2025-04-10 09:06:50,111: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.112 | [2025-04-10 09:06:50,111: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.112 | [2025-04-10 09:06:50,111: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.112 | [2025-04-10 09:06:50,111: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.112 | [2025-04-10 09:06:50,111: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.112 | [2025-04-10 09:06:50,112: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.112 | [2025-04-10 09:06:50,112: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.112 | [2025-04-10 09:06:50,112: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.112 | [2025-04-10 09:06:50,112: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.112 | [2025-04-10 09:06:50,112: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.112 | [2025-04-10 09:06:50,112: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.112 | [2025-04-10 09:06:50,112: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.112 | [2025-04-10 09:06:50,112: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.112 | [2025-04-10 09:06:50,112: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.112 | [2025-04-10 09:06:50,112: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.112 | [2025-04-10 09:06:50,112: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.112 | [2025-04-10 09:06:50,112: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.112 | [2025-04-10 09:06:50,112: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.112 | [2025-04-10 09:06:50,112: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.112 | [2025-04-10 09:06:50,112: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.112 | [2025-04-10 09:06:50,112: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.112 | [2025-04-10 09:06:50,112: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.112 | [2025-04-10 09:06:50,112: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.112 | [2025-04-10 09:06:50,112: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.112 | [2025-04-10 09:06:50,112: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.112 | [2025-04-10 09:06:50,112: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.112 | [2025-04-10 09:06:50,112: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.112 | [2025-04-10 09:06:50,112: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.112 | [2025-04-10 09:06:50,112: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.112 | [2025-04-10 09:06:50,112: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.112 | [2025-04-10 09:06:50,112: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.113 | [2025-04-10 09:06:50,112: WARNING/MainProcess] ^
celery-beat | 2025-04-10 09:06:50.113 | [2025-04-10 09:06:50,112: WARNING/MainProcess]   File "/usr/local/lib/python3.11/site-packages/django/db/backends/mysql/operations.py", line 267, in adapt_datetimefield_value
celery-beat | 2025-04-10 09:06:50.113 | [2025-04-10 09:06:50,112: WARNING/MainProcess]     
celery-beat | 2025-04-10 09:06:50.113 | [2025-04-10 09:06:50,112: WARNING/MainProcess] raise ValueError(
celery-beat | 2025-04-10 09:06:50.113 | [2025-04-10 09:06:50,112: WARNING/MainProcess] ValueError
celery-beat | 2025-04-10 09:06:50.113 | [2025-04-10 09:06:50,112: WARNING/MainProcess] : 
celery-beat | 2025-04-10 09:06:50.113 | [2025-04-10 09:06:50,112: WARNING/MainProcess] MySQL backend does not support timezone-aware datetimes when USE_TZ is False.
celery-beat | 2025-04-10 09:07:09.143 | wait-for-it.sh: waiting 15 seconds for db:3306
celery-beat | 2025-04-10 09:07:11.151 | wait-for-it.sh: db:3306 is available after 2 seconds
celery-beat | 2025-04-10 09:07:13.397 | [2025-04-10 09:07:13,397: INFO/MainProcess] beat: Starting...
celery-beat | 2025-04-10 09:07:13.432 | [2025-04-10 09:07:13,432: INFO/MainProcess] DatabaseScheduler: Schedule changed.
celery-beat | 2025-04-10 09:08:43.441 | wait-for-it.sh: waiting 15 seconds for db:3306
celery-beat | 2025-04-10 09:08:48.430 | wait-for-it.sh: db:3306 is available after 5 seconds
celery-beat | 2025-04-10 09:08:50.555 | [2025-04-10 09:08:50,555: INFO/MainProcess] beat: Starting...
celery-beat | 2025-04-10 09:08:50.597 | [2025-04-10 09:08:50,597: INFO/MainProcess] DatabaseScheduler: Schedule changed.
celery-beat | 2025-04-10 09:09:16.127 | wait-for-it.sh: waiting 15 seconds for db:3306
celery-beat | 2025-04-10 09:06:50.247 | celery beat v5.4.0 (opalescent) is starting.
celery-beat | 2025-04-10 09:06:50.247 | __    -    ... __   -        _
celery-beat | 2025-04-10 09:06:50.247 | LocalTime -> 2025-04-10 09:04:23
celery-beat | 2025-04-10 09:06:50.247 | Configuration ->
celery-beat | 2025-04-10 09:06:50.247 |     . broker -> redis://redis:6379/5
celery-beat | 2025-04-10 09:06:50.247 |     . loader -> celery.loaders.app.AppLoader
celery-beat | 2025-04-10 09:06:50.247 |     . scheduler -> django_celery_beat.schedulers.DatabaseScheduler
celery-beat | 2025-04-10 09:06:50.247 | 
celery-beat | 2025-04-10 09:06:50.247 |     . logfile -> [stderr]@%INFO
celery-beat | 2025-04-10 09:06:50.247 |     . maxinterval -> 5.00 seconds (5s)
celery-beat | 2025-04-10 09:07:12.313 | Operations to perform:
celery-beat | 2025-04-10 09:07:12.313 |   Apply all migrations: admin, admin_interface, auth, contenttypes, django_celery_beat, django_celery_results, reloj_fichador, sessions
celery-beat | 2025-04-10 09:07:12.313 | Running migrations:
celery-beat | 2025-04-10 09:07:12.313 |   No migrations to apply.
celery-beat | 2025-04-10 09:08:38.645 | celery beat v5.4.0 (opalescent) is starting.
celery-beat | 2025-04-10 09:08:38.646 | __    -    ... __   -        _
celery-beat | 2025-04-10 09:08:38.646 | LocalTime -> 2025-04-10 09:07:13
celery-beat | 2025-04-10 09:08:38.646 | Configuration ->
celery-beat | 2025-04-10 09:08:38.646 |     . broker -> redis://redis:6379/5
celery-beat | 2025-04-10 09:08:38.646 |     . loader -> celery.loaders.app.AppLoader
celery-beat | 2025-04-10 09:08:38.646 |     . scheduler -> django_celery_beat.schedulers.DatabaseScheduler
celery-beat | 2025-04-10 09:08:38.646 | 
celery-beat | 2025-04-10 09:08:38.646 |     . logfile -> [stderr]@%INFO
celery-beat | 2025-04-10 09:08:38.646 |     . maxinterval -> 5.00 seconds (5s)
celery-beat | 2025-04-10 09:08:49.476 | Operations to perform:
celery-beat | 2025-04-10 09:08:49.476 |   Apply all migrations: admin, admin_interface, auth, contenttypes, django_celery_beat, django_celery_results, reloj_fichador, sessions
celery-beat | 2025-04-10 09:08:49.476 | Running migrations:
celery-beat | 2025-04-10 09:08:49.476 |   No migrations to apply.
celery-beat | 2025-04-10 09:09:11.040 | celery beat v5.4.0 (opalescent) is starting.
celery-beat | 2025-04-10 09:09:11.040 | __    -    ... __   -        _
celery-beat | 2025-04-10 09:09:11.040 | LocalTime -> 2025-04-10 09:08:50
celery-beat | 2025-04-10 09:09:11.040 | Configuration ->
celery-beat | 2025-04-10 09:09:11.040 |     . broker -> redis://redis:6379/5
celery-beat | 2025-04-10 09:09:11.040 |     . loader -> celery.loaders.app.AppLoader
celery-beat | 2025-04-10 09:09:11.040 |     . scheduler -> django_celery_beat.schedulers.DatabaseScheduler
celery-beat | 2025-04-10 09:09:11.040 | 
celery-beat | 2025-04-10 09:09:11.040 |     . logfile -> [stderr]@%INFO
celery-beat | 2025-04-10 09:09:11.040 |     . maxinterval -> 5.00 seconds (5s)
birt        | 2025-04-10 08:52:40.513 | NOTE: Picked up JDK_JAVA_OPTIONS:  --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.rmi/sun.rmi.transport=ALL-UNNAMED
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
birt        | 2025-04-10 08:52:41.114 | 10-Apr-2025 11:52:41.114 INFO [main] org.apache.coyote.AbstractProtocol.init Initializing ProtocolHandler ["http-nio-8080"]
birt        | 2025-04-10 08:52:41.131 | 10-Apr-2025 11:52:41.131 INFO [main] org.apache.catalina.startup.Catalina.load Server initialization in [419] milliseconds
birt        | 2025-04-10 08:52:41.157 | 10-Apr-2025 11:52:41.157 INFO [main] org.apache.catalina.core.StandardService.startInternal Starting service [Catalina]
birt        | 2025-04-10 08:52:41.157 | 10-Apr-2025 11:52:41.157 INFO [main] org.apache.catalina.core.StandardEngine.startInternal Starting Servlet engine: [Apache Tomcat/9.0.102]
birt        | 2025-04-10 08:52:41.171 | 10-Apr-2025 11:52:41.170 INFO [main] org.apache.catalina.startup.HostConfig.deployWAR Deploying web application archive [/usr/local/tomcat/webapps/birt.war]
birt        | 2025-04-10 08:52:41.750 | 10-Apr-2025 11:52:41.750 INFO [main] org.apache.jasper.servlet.TldScanner.scanJars At least one JAR was scanned for TLDs yet contained no TLDs. Enable debug logging for this logger for a complete list of JARs that were scanned but no TLDs were found in them. Skipping unneeded JARs during scanning can improve startup time and JSP compilation time.
birt        | 2025-04-10 08:52:41.777 | 10-Apr-2025 11:52:41.777 INFO [main] org.apache.catalina.startup.HostConfig.deployWAR Deployment of web application archive [/usr/local/tomcat/webapps/birt.war] has finished in [606] ms
birt        | 2025-04-10 08:52:41.781 | 10-Apr-2025 11:52:41.780 INFO [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["http-nio-8080"]
birt        | 2025-04-10 08:52:41.788 | 10-Apr-2025 11:52:41.788 INFO [main] org.apache.catalina.startup.Catalina.start Server startup in [656] milliseconds
birt        | 2025-04-10 09:04:11.603 | 10-Apr-2025 12:04:11.601 INFO [Thread-1] org.apache.coyote.AbstractProtocol.pause Pausing ProtocolHandler ["http-nio-8080"]
birt        | 2025-04-10 09:04:11.603 | 10-Apr-2025 12:04:11.603 INFO [Thread-1] org.apache.catalina.core.StandardService.stopInternal Stopping service [Catalina]
birt        | 2025-04-10 09:04:11.609 | 10-Apr-2025 12:04:11.609 INFO [Thread-1] org.apache.coyote.AbstractProtocol.stop Stopping ProtocolHandler ["http-nio-8080"]
birt        | 2025-04-10 09:04:11.622 | 10-Apr-2025 12:04:11.622 INFO [Thread-1] org.apache.coyote.AbstractProtocol.destroy Destroying ProtocolHandler ["http-nio-8080"]
birt        | 2025-04-10 09:04:17.279 | NOTE: Picked up JDK_JAVA_OPTIONS:  --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.rmi/sun.rmi.transport=ALL-UNNAMED
birt        | 2025-04-10 09:04:17.596 | 10-Apr-2025 12:04:17.593 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Server version name:   Apache Tomcat/9.0.102
birt        | 2025-04-10 09:04:17.596 | 10-Apr-2025 12:04:17.596 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Server built:          Mar 3 2025 19:33:14 UTC
birt        | 2025-04-10 09:04:17.596 | 10-Apr-2025 12:04:17.596 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Server version number: 9.0.102.0
birt        | 2025-04-10 09:04:17.597 | 10-Apr-2025 12:04:17.596 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log OS Name:               Linux
birt        | 2025-04-10 09:04:17.597 | 10-Apr-2025 12:04:17.597 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log OS Version:            5.15.167.4-microsoft-standard-WSL2
birt        | 2025-04-10 09:04:17.597 | 10-Apr-2025 12:04:17.597 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Architecture:          amd64
birt        | 2025-04-10 09:04:17.597 | 10-Apr-2025 12:04:17.597 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Java Home:             /opt/java/openjdk
birt        | 2025-04-10 09:04:17.597 | 10-Apr-2025 12:04:17.597 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log JVM Version:           21.0.6+7-LTS
birt        | 2025-04-10 09:04:17.597 | 10-Apr-2025 12:04:17.597 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log JVM Vendor:            Eclipse Adoptium
birt        | 2025-04-10 09:04:17.597 | 10-Apr-2025 12:04:17.597 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log CATALINA_BASE:         /usr/local/tomcat
birt        | 2025-04-10 09:04:17.597 | 10-Apr-2025 12:04:17.597 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log CATALINA_HOME:         /usr/local/tomcat
birt        | 2025-04-10 09:04:17.602 | 10-Apr-2025 12:04:17.602 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.lang=ALL-UNNAMED
birt        | 2025-04-10 09:04:17.602 | 10-Apr-2025 12:04:17.602 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.lang.invoke=ALL-UNNAMED
birt        | 2025-04-10 09:04:17.602 | 10-Apr-2025 12:04:17.602 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.lang.reflect=ALL-UNNAMED
birt        | 2025-04-10 09:04:17.602 | 10-Apr-2025 12:04:17.602 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.io=ALL-UNNAMED
birt        | 2025-04-10 09:04:17.602 | 10-Apr-2025 12:04:17.602 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.util=ALL-UNNAMED
birt        | 2025-04-10 09:04:17.602 | 10-Apr-2025 12:04:17.602 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.util.concurrent=ALL-UNNAMED
birt        | 2025-04-10 09:04:17.602 | 10-Apr-2025 12:04:17.602 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.rmi/sun.rmi.transport=ALL-UNNAMED
birt        | 2025-04-10 09:04:17.602 | 10-Apr-2025 12:04:17.602 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.util.logging.config.file=/usr/local/tomcat/conf/logging.properties
birt        | 2025-04-10 09:04:17.602 | 10-Apr-2025 12:04:17.602 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager
birt        | 2025-04-10 09:04:17.602 | 10-Apr-2025 12:04:17.602 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.awt.headless=true
birt        | 2025-04-10 09:04:17.602 | 10-Apr-2025 12:04:17.602 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djdk.tls.ephemeralDHKeySize=2048
birt        | 2025-04-10 09:04:17.602 | 10-Apr-2025 12:04:17.602 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.protocol.handler.pkgs=org.apache.catalina.webresources
birt        | 2025-04-10 09:04:17.602 | 10-Apr-2025 12:04:17.602 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dsun.io.useCanonCaches=false
birt        | 2025-04-10 09:04:17.602 | 10-Apr-2025 12:04:17.602 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dorg.apache.catalina.security.SecurityListener.UMASK=0027
birt        | 2025-04-10 09:04:17.602 | 10-Apr-2025 12:04:17.602 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dignore.endorsed.dirs=
birt        | 2025-04-10 09:04:17.602 | 10-Apr-2025 12:04:17.602 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dcatalina.base=/usr/local/tomcat
birt        | 2025-04-10 09:04:17.603 | 10-Apr-2025 12:04:17.602 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dcatalina.home=/usr/local/tomcat
birt        | 2025-04-10 09:04:17.603 | 10-Apr-2025 12:04:17.603 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.io.tmpdir=/usr/local/tomcat/temp
birt        | 2025-04-10 09:04:17.605 | 10-Apr-2025 12:04:17.604 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent Loaded Apache Tomcat Native library [1.3.1] using APR version [1.7.2].
birt        | 2025-04-10 09:04:17.605 | 10-Apr-2025 12:04:17.605 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent APR capabilities: IPv6 [true], sendfile [true], accept filters [false], random [true], UDS [true].
birt        | 2025-04-10 09:04:17.605 | 10-Apr-2025 12:04:17.605 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent APR/OpenSSL configuration: useAprConnector [false], useOpenSSL [true]
birt        | 2025-04-10 09:04:17.607 | 10-Apr-2025 12:04:17.607 INFO [main] org.apache.catalina.core.AprLifecycleListener.initializeSSL OpenSSL successfully initialized [OpenSSL 3.0.13 30 Jan 2024]
birt        | 2025-04-10 09:04:17.848 | 10-Apr-2025 12:04:17.848 INFO [main] org.apache.coyote.AbstractProtocol.init Initializing ProtocolHandler ["http-nio-8080"]
birt        | 2025-04-10 09:04:17.863 | 10-Apr-2025 12:04:17.863 INFO [main] org.apache.catalina.startup.Catalina.load Server initialization in [378] milliseconds
birt        | 2025-04-10 09:04:17.886 | 10-Apr-2025 12:04:17.885 INFO [main] org.apache.catalina.core.StandardService.startInternal Starting service [Catalina]
birt        | 2025-04-10 09:04:17.886 | 10-Apr-2025 12:04:17.886 INFO [main] org.apache.catalina.core.StandardEngine.startInternal Starting Servlet engine: [Apache Tomcat/9.0.102]
birt        | 2025-04-10 09:04:17.899 | 10-Apr-2025 12:04:17.898 INFO [main] org.apache.catalina.startup.HostConfig.deployWAR Deploying web application archive [/usr/local/tomcat/webapps/birt.war]
birt        | 2025-04-10 09:04:18.437 | 10-Apr-2025 12:04:18.436 INFO [main] org.apache.jasper.servlet.TldScanner.scanJars At least one JAR was scanned for TLDs yet contained no TLDs. Enable debug logging for this logger for a complete list of JARs that were scanned but no TLDs were found in them. Skipping unneeded JARs during scanning can improve startup time and JSP compilation time.
birt        | 2025-04-10 09:04:18.458 | 10-Apr-2025 12:04:18.457 INFO [main] org.apache.catalina.startup.HostConfig.deployWAR Deployment of web application archive [/usr/local/tomcat/webapps/birt.war] has finished in [559] ms
birt        | 2025-04-10 09:04:18.460 | 10-Apr-2025 12:04:18.460 INFO [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["http-nio-8080"]
birt        | 2025-04-10 09:04:18.465 | 10-Apr-2025 12:04:18.465 INFO [main] org.apache.catalina.startup.Catalina.start Server startup in [600] milliseconds
birt        | 2025-04-10 09:06:50.046 | 10-Apr-2025 12:06:50.045 INFO [Thread-1] org.apache.coyote.AbstractProtocol.pause Pausing ProtocolHandler ["http-nio-8080"]
birt        | 2025-04-10 09:06:50.049 | 10-Apr-2025 12:06:50.048 INFO [Thread-1] org.apache.catalina.core.StandardService.stopInternal Stopping service [Catalina]
birt        | 2025-04-10 09:06:50.055 | 10-Apr-2025 12:06:50.055 INFO [Thread-1] org.apache.coyote.AbstractProtocol.stop Stopping ProtocolHandler ["http-nio-8080"]
birt        | 2025-04-10 09:06:50.058 | 10-Apr-2025 12:06:50.058 INFO [Thread-1] org.apache.coyote.AbstractProtocol.destroy Destroying ProtocolHandler ["http-nio-8080"]
birt        | 2025-04-10 09:07:09.143 | NOTE: Picked up JDK_JAVA_OPTIONS:  --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.rmi/sun.rmi.transport=ALL-UNNAMED
birt        | 2025-04-10 09:07:09.511 | 10-Apr-2025 12:07:09.508 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Server version name:   Apache Tomcat/9.0.102
birt        | 2025-04-10 09:07:09.512 | 10-Apr-2025 12:07:09.511 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Server built:          Mar 3 2025 19:33:14 UTC
birt        | 2025-04-10 09:07:09.512 | 10-Apr-2025 12:07:09.512 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Server version number: 9.0.102.0
birt        | 2025-04-10 09:07:09.512 | 10-Apr-2025 12:07:09.512 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log OS Name:               Linux
birt        | 2025-04-10 09:07:09.512 | 10-Apr-2025 12:07:09.512 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log OS Version:            5.15.167.4-microsoft-standard-WSL2
birt        | 2025-04-10 09:07:09.513 | 10-Apr-2025 12:07:09.512 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Architecture:          amd64
birt        | 2025-04-10 09:07:09.513 | 10-Apr-2025 12:07:09.513 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Java Home:             /opt/java/openjdk
birt        | 2025-04-10 09:07:09.513 | 10-Apr-2025 12:07:09.513 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log JVM Version:           21.0.6+7-LTS
birt        | 2025-04-10 09:07:09.513 | 10-Apr-2025 12:07:09.513 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log JVM Vendor:            Eclipse Adoptium
birt        | 2025-04-10 09:07:09.513 | 10-Apr-2025 12:07:09.513 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log CATALINA_BASE:         /usr/local/tomcat
birt        | 2025-04-10 09:07:09.513 | 10-Apr-2025 12:07:09.513 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log CATALINA_HOME:         /usr/local/tomcat
birt        | 2025-04-10 09:07:09.519 | 10-Apr-2025 12:07:09.518 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.lang=ALL-UNNAMED
birt        | 2025-04-10 09:07:09.519 | 10-Apr-2025 12:07:09.518 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.lang.invoke=ALL-UNNAMED
birt        | 2025-04-10 09:07:09.520 | 10-Apr-2025 12:07:09.519 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.lang.reflect=ALL-UNNAMED
birt        | 2025-04-10 09:07:09.520 | 10-Apr-2025 12:07:09.520 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.io=ALL-UNNAMED
birt        | 2025-04-10 09:07:09.520 | 10-Apr-2025 12:07:09.520 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.util=ALL-UNNAMED
birt        | 2025-04-10 09:07:09.520 | 10-Apr-2025 12:07:09.520 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.util.concurrent=ALL-UNNAMED
birt        | 2025-04-10 09:07:09.520 | 10-Apr-2025 12:07:09.520 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.rmi/sun.rmi.transport=ALL-UNNAMED
birt        | 2025-04-10 09:07:09.520 | 10-Apr-2025 12:07:09.520 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.util.logging.config.file=/usr/local/tomcat/conf/logging.properties
birt        | 2025-04-10 09:07:09.520 | 10-Apr-2025 12:07:09.520 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager
birt        | 2025-04-10 09:07:09.521 | 10-Apr-2025 12:07:09.520 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.awt.headless=true
birt        | 2025-04-10 09:07:09.521 | 10-Apr-2025 12:07:09.521 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djdk.tls.ephemeralDHKeySize=2048
birt        | 2025-04-10 09:07:09.521 | 10-Apr-2025 12:07:09.521 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.protocol.handler.pkgs=org.apache.catalina.webresources
birt        | 2025-04-10 09:07:09.521 | 10-Apr-2025 12:07:09.521 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dsun.io.useCanonCaches=false
birt        | 2025-04-10 09:07:09.521 | 10-Apr-2025 12:07:09.521 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dorg.apache.catalina.security.SecurityListener.UMASK=0027
birt        | 2025-04-10 09:07:09.521 | 10-Apr-2025 12:07:09.521 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dignore.endorsed.dirs=
birt        | 2025-04-10 09:07:09.521 | 10-Apr-2025 12:07:09.521 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dcatalina.base=/usr/local/tomcat
birt        | 2025-04-10 09:07:09.521 | 10-Apr-2025 12:07:09.521 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dcatalina.home=/usr/local/tomcat
birt        | 2025-04-10 09:07:09.521 | 10-Apr-2025 12:07:09.521 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.io.tmpdir=/usr/local/tomcat/temp
birt        | 2025-04-10 09:07:09.524 | 10-Apr-2025 12:07:09.523 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent Loaded Apache Tomcat Native library [1.3.1] using APR version [1.7.2].
birt        | 2025-04-10 09:07:09.524 | 10-Apr-2025 12:07:09.524 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent APR capabilities: IPv6 [true], sendfile [true], accept filters [false], random [true], UDS [true].
birt        | 2025-04-10 09:07:09.524 | 10-Apr-2025 12:07:09.524 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent APR/OpenSSL configuration: useAprConnector [false], useOpenSSL [true]
birt        | 2025-04-10 09:07:09.526 | 10-Apr-2025 12:07:09.526 INFO [main] org.apache.catalina.core.AprLifecycleListener.initializeSSL OpenSSL successfully initialized [OpenSSL 3.0.13 30 Jan 2024]
birt        | 2025-04-10 09:07:09.735 | 10-Apr-2025 12:07:09.735 INFO [main] org.apache.coyote.AbstractProtocol.init Initializing ProtocolHandler ["http-nio-8080"]
birt        | 2025-04-10 09:07:09.748 | 10-Apr-2025 12:07:09.747 INFO [main] org.apache.catalina.startup.Catalina.load Server initialization in [396] milliseconds
birt        | 2025-04-10 09:07:09.777 | 10-Apr-2025 12:07:09.776 INFO [main] org.apache.catalina.core.StandardService.startInternal Starting service [Catalina]
birt        | 2025-04-10 09:07:09.777 | 10-Apr-2025 12:07:09.777 INFO [main] org.apache.catalina.core.StandardEngine.startInternal Starting Servlet engine: [Apache Tomcat/9.0.102]
birt        | 2025-04-10 09:07:09.789 | 10-Apr-2025 12:07:09.788 INFO [main] org.apache.catalina.startup.HostConfig.deployWAR Deploying web application archive [/usr/local/tomcat/webapps/birt.war]
birt        | 2025-04-10 09:07:10.309 | 10-Apr-2025 12:07:10.309 INFO [main] org.apache.jasper.servlet.TldScanner.scanJars At least one JAR was scanned for TLDs yet contained no TLDs. Enable debug logging for this logger for a complete list of JARs that were scanned but no TLDs were found in them. Skipping unneeded JARs during scanning can improve startup time and JSP compilation time.
birt        | 2025-04-10 09:07:10.337 | 10-Apr-2025 12:07:10.336 INFO [main] org.apache.catalina.startup.HostConfig.deployWAR Deployment of web application archive [/usr/local/tomcat/webapps/birt.war] has finished in [548] ms
birt        | 2025-04-10 09:07:10.339 | 10-Apr-2025 12:07:10.339 INFO [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["http-nio-8080"]
birt        | 2025-04-10 09:07:10.347 | 10-Apr-2025 12:07:10.347 INFO [main] org.apache.catalina.startup.Catalina.start Server startup in [598] milliseconds
birt        | 2025-04-10 09:08:38.478 | 10-Apr-2025 12:08:38.478 INFO [Thread-1] org.apache.coyote.AbstractProtocol.pause Pausing ProtocolHandler ["http-nio-8080"]
birt        | 2025-04-10 09:08:38.480 | 10-Apr-2025 12:08:38.480 INFO [Thread-1] org.apache.catalina.core.StandardService.stopInternal Stopping service [Catalina]
birt        | 2025-04-10 09:08:38.488 | 10-Apr-2025 12:08:38.487 INFO [Thread-1] org.apache.coyote.AbstractProtocol.stop Stopping ProtocolHandler ["http-nio-8080"]
birt        | 2025-04-10 09:08:38.490 | 10-Apr-2025 12:08:38.490 INFO [Thread-1] org.apache.coyote.AbstractProtocol.destroy Destroying ProtocolHandler ["http-nio-8080"]
birt        | 2025-04-10 09:08:43.686 | NOTE: Picked up JDK_JAVA_OPTIONS:  --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.rmi/sun.rmi.transport=ALL-UNNAMED
birt        | 2025-04-10 09:08:43.940 | 10-Apr-2025 12:08:43.938 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Server version name:   Apache Tomcat/9.0.102
birt        | 2025-04-10 09:08:43.940 | 10-Apr-2025 12:08:43.940 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Server built:          Mar 3 2025 19:33:14 UTC
birt        | 2025-04-10 09:08:43.940 | 10-Apr-2025 12:08:43.940 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Server version number: 9.0.102.0
birt        | 2025-04-10 09:08:43.940 | 10-Apr-2025 12:08:43.940 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log OS Name:               Linux
birt        | 2025-04-10 09:08:43.940 | 10-Apr-2025 12:08:43.940 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log OS Version:            5.15.167.4-microsoft-standard-WSL2
birt        | 2025-04-10 09:08:43.940 | 10-Apr-2025 12:08:43.940 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Architecture:          amd64
birt        | 2025-04-10 09:08:43.940 | 10-Apr-2025 12:08:43.940 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Java Home:             /opt/java/openjdk
birt        | 2025-04-10 09:08:43.940 | 10-Apr-2025 12:08:43.940 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log JVM Version:           21.0.6+7-LTS
birt        | 2025-04-10 09:08:43.940 | 10-Apr-2025 12:08:43.940 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log JVM Vendor:            Eclipse Adoptium
birt        | 2025-04-10 09:08:43.941 | 10-Apr-2025 12:08:43.940 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log CATALINA_BASE:         /usr/local/tomcat
birt        | 2025-04-10 09:08:43.941 | 10-Apr-2025 12:08:43.941 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log CATALINA_HOME:         /usr/local/tomcat
birt        | 2025-04-10 09:08:43.947 | 10-Apr-2025 12:08:43.947 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.lang=ALL-UNNAMED
birt        | 2025-04-10 09:08:43.947 | 10-Apr-2025 12:08:43.947 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.lang.invoke=ALL-UNNAMED
birt        | 2025-04-10 09:08:43.947 | 10-Apr-2025 12:08:43.947 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.lang.reflect=ALL-UNNAMED
birt        | 2025-04-10 09:08:43.947 | 10-Apr-2025 12:08:43.947 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.io=ALL-UNNAMED
birt        | 2025-04-10 09:08:43.947 | 10-Apr-2025 12:08:43.947 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.util=ALL-UNNAMED
birt        | 2025-04-10 09:08:43.947 | 10-Apr-2025 12:08:43.947 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.util.concurrent=ALL-UNNAMED
birt        | 2025-04-10 09:08:43.947 | 10-Apr-2025 12:08:43.947 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.rmi/sun.rmi.transport=ALL-UNNAMED
birt        | 2025-04-10 09:08:43.947 | 10-Apr-2025 12:08:43.947 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.util.logging.config.file=/usr/local/tomcat/conf/logging.properties
birt        | 2025-04-10 09:08:43.947 | 10-Apr-2025 12:08:43.947 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager
birt        | 2025-04-10 09:08:43.948 | 10-Apr-2025 12:08:43.947 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.awt.headless=true
birt        | 2025-04-10 09:08:43.948 | 10-Apr-2025 12:08:43.948 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djdk.tls.ephemeralDHKeySize=2048
birt        | 2025-04-10 09:08:43.948 | 10-Apr-2025 12:08:43.948 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.protocol.handler.pkgs=org.apache.catalina.webresources
birt        | 2025-04-10 09:08:43.948 | 10-Apr-2025 12:08:43.948 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dsun.io.useCanonCaches=false
birt        | 2025-04-10 09:08:43.948 | 10-Apr-2025 12:08:43.948 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dorg.apache.catalina.security.SecurityListener.UMASK=0027
birt        | 2025-04-10 09:08:43.948 | 10-Apr-2025 12:08:43.948 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dignore.endorsed.dirs=
birt        | 2025-04-10 09:08:43.948 | 10-Apr-2025 12:08:43.948 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dcatalina.base=/usr/local/tomcat
birt        | 2025-04-10 09:08:43.948 | 10-Apr-2025 12:08:43.948 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dcatalina.home=/usr/local/tomcat
birt        | 2025-04-10 09:08:43.948 | 10-Apr-2025 12:08:43.948 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.io.tmpdir=/usr/local/tomcat/temp
birt        | 2025-04-10 09:08:43.950 | 10-Apr-2025 12:08:43.950 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent Loaded Apache Tomcat Native library [1.3.1] using APR version [1.7.2].
birt        | 2025-04-10 09:08:43.950 | 10-Apr-2025 12:08:43.950 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent APR capabilities: IPv6 [true], sendfile [true], accept filters [false], random [true], UDS [true].
birt        | 2025-04-10 09:08:43.950 | 10-Apr-2025 12:08:43.950 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent APR/OpenSSL configuration: useAprConnector [false], useOpenSSL [true]
birt        | 2025-04-10 09:08:43.953 | 10-Apr-2025 12:08:43.952 INFO [main] org.apache.catalina.core.AprLifecycleListener.initializeSSL OpenSSL successfully initialized [OpenSSL 3.0.13 30 Jan 2024]
birt        | 2025-04-10 09:08:44.199 | 10-Apr-2025 12:08:44.199 INFO [main] org.apache.coyote.AbstractProtocol.init Initializing ProtocolHandler ["http-nio-8080"]
birt        | 2025-04-10 09:08:44.212 | 10-Apr-2025 12:08:44.212 INFO [main] org.apache.catalina.startup.Catalina.load Server initialization in [396] milliseconds
birt        | 2025-04-10 09:08:44.236 | 10-Apr-2025 12:08:44.235 INFO [main] org.apache.catalina.core.StandardService.startInternal Starting service [Catalina]
birt        | 2025-04-10 09:08:44.236 | 10-Apr-2025 12:08:44.236 INFO [main] org.apache.catalina.core.StandardEngine.startInternal Starting Servlet engine: [Apache Tomcat/9.0.102]
birt        | 2025-04-10 09:08:44.247 | 10-Apr-2025 12:08:44.246 INFO [main] org.apache.catalina.startup.HostConfig.deployWAR Deploying web application archive [/usr/local/tomcat/webapps/birt.war]
birt        | 2025-04-10 09:08:44.839 | 10-Apr-2025 12:08:44.839 INFO [main] org.apache.jasper.servlet.TldScanner.scanJars At least one JAR was scanned for TLDs yet contained no TLDs. Enable debug logging for this logger for a complete list of JARs that were scanned but no TLDs were found in them. Skipping unneeded JARs during scanning can improve startup time and JSP compilation time.
birt        | 2025-04-10 09:08:44.866 | 10-Apr-2025 12:08:44.866 INFO [main] org.apache.catalina.startup.HostConfig.deployWAR Deployment of web application archive [/usr/local/tomcat/webapps/birt.war] has finished in [620] ms
birt        | 2025-04-10 09:08:44.869 | 10-Apr-2025 12:08:44.868 INFO [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["http-nio-8080"]
birt        | 2025-04-10 09:08:44.875 | 10-Apr-2025 12:08:44.874 INFO [main] org.apache.catalina.startup.Catalina.start Server startup in [661] milliseconds
birt        | 2025-04-10 09:09:10.841 | 10-Apr-2025 12:09:10.841 INFO [Thread-1] org.apache.coyote.AbstractProtocol.pause Pausing ProtocolHandler ["http-nio-8080"]
birt        | 2025-04-10 09:09:10.851 | 10-Apr-2025 12:09:10.843 INFO [Thread-1] org.apache.catalina.core.StandardService.stopInternal Stopping service [Catalina]
birt        | 2025-04-10 09:09:10.851 | 10-Apr-2025 12:09:10.850 INFO [Thread-1] org.apache.coyote.AbstractProtocol.stop Stopping ProtocolHandler ["http-nio-8080"]
birt        | 2025-04-10 09:09:10.855 | 10-Apr-2025 12:09:10.855 INFO [Thread-1] org.apache.coyote.AbstractProtocol.destroy Destroying ProtocolHandler ["http-nio-8080"]
birt        | 2025-04-10 09:09:16.407 | NOTE: Picked up JDK_JAVA_OPTIONS:  --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.rmi/sun.rmi.transport=ALL-UNNAMED
redis       | 2025-04-10 08:52:40.132 | 1:C 10 Apr 2025 11:52:40.131 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
redis       | 2025-04-10 08:52:40.132 | 1:C 10 Apr 2025 11:52:40.132 * Redis version=7.4.2, bits=64, commit=00000000, modified=0, pid=1, just started
redis       | 2025-04-10 08:52:40.132 | 1:C 10 Apr 2025 11:52:40.132 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
redis       | 2025-04-10 08:52:40.132 | 1:M 10 Apr 2025 11:52:40.132 * monotonic clock: POSIX clock_gettime
redis       | 2025-04-10 08:52:40.133 | 1:M 10 Apr 2025 11:52:40.133 * Running mode=standalone, port=6379.
redis       | 2025-04-10 08:52:40.133 | 1:M 10 Apr 2025 11:52:40.133 * Server initialized
redis       | 2025-04-10 08:52:40.133 | 1:M 10 Apr 2025 11:52:40.133 * Ready to accept connections tcp
redis       | 2025-04-10 09:04:11.630 | 1:signal-handler (1744286651) Received SIGTERM scheduling shutdown...
redis       | 2025-04-10 09:04:11.713 | 1:M 10 Apr 2025 12:04:11.713 * User requested shutdown...
redis       | 2025-04-10 09:04:11.713 | 1:M 10 Apr 2025 12:04:11.713 * Saving the final RDB snapshot before exiting.
redis       | 2025-04-10 09:04:11.716 | 1:M 10 Apr 2025 12:04:11.715 * DB saved on disk
redis       | 2025-04-10 09:04:11.716 | 1:M 10 Apr 2025 12:04:11.716 # Redis is now ready to exit, bye bye...
redis       | 2025-04-10 09:04:17.298 | 1:C 10 Apr 2025 12:04:17.298 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
redis       | 2025-04-10 09:04:17.298 | 1:C 10 Apr 2025 12:04:17.298 * Redis version=7.4.2, bits=64, commit=00000000, modified=0, pid=1, just started
redis       | 2025-04-10 09:04:17.298 | 1:C 10 Apr 2025 12:04:17.298 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
redis       | 2025-04-10 09:04:17.299 | 1:M 10 Apr 2025 12:04:17.299 * monotonic clock: POSIX clock_gettime
redis       | 2025-04-10 09:04:17.299 | 1:M 10 Apr 2025 12:04:17.299 * Running mode=standalone, port=6379.
redis       | 2025-04-10 09:04:17.300 | 1:M 10 Apr 2025 12:04:17.300 * Server initialized
redis       | 2025-04-10 09:04:17.300 | 1:M 10 Apr 2025 12:04:17.300 * Loading RDB produced by version 7.4.2
redis       | 2025-04-10 09:04:17.300 | 1:M 10 Apr 2025 12:04:17.300 * RDB age 6 seconds
redis       | 2025-04-10 09:04:17.300 | 1:M 10 Apr 2025 12:04:17.300 * RDB memory usage when created 1.38 Mb
redis       | 2025-04-10 09:04:17.300 | 1:M 10 Apr 2025 12:04:17.300 * Done loading RDB, keys loaded: 1, keys expired: 0.
redis       | 2025-04-10 09:04:17.300 | 1:M 10 Apr 2025 12:04:17.300 * DB loaded from disk: 0.000 seconds
redis       | 2025-04-10 09:04:17.300 | 1:M 10 Apr 2025 12:04:17.300 * Ready to accept connections tcp
redis       | 2025-04-10 09:06:52.369 | 1:signal-handler (1744286812) Received SIGTERM scheduling shutdown...
redis       | 2025-04-10 09:06:52.427 | 1:M 10 Apr 2025 12:06:52.426 * User requested shutdown...
redis       | 2025-04-10 09:06:52.427 | 1:M 10 Apr 2025 12:06:52.426 * Saving the final RDB snapshot before exiting.
redis       | 2025-04-10 09:06:52.429 | 1:M 10 Apr 2025 12:06:52.429 * DB saved on disk
redis       | 2025-04-10 09:06:52.429 | 1:M 10 Apr 2025 12:06:52.429 # Redis is now ready to exit, bye bye...
redis       | 2025-04-10 09:07:08.799 | 1:C 10 Apr 2025 12:07:08.799 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
redis       | 2025-04-10 09:07:08.799 | 1:C 10 Apr 2025 12:07:08.799 * Redis version=7.4.2, bits=64, commit=00000000, modified=0, pid=1, just started
redis       | 2025-04-10 09:07:08.799 | 1:C 10 Apr 2025 12:07:08.799 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
redis       | 2025-04-10 09:07:08.799 | 1:M 10 Apr 2025 12:07:08.799 * monotonic clock: POSIX clock_gettime
redis       | 2025-04-10 09:07:08.800 | 1:M 10 Apr 2025 12:07:08.800 * Running mode=standalone, port=6379.
redis       | 2025-04-10 09:07:08.800 | 1:M 10 Apr 2025 12:07:08.800 * Server initialized
redis       | 2025-04-10 09:07:08.800 | 1:M 10 Apr 2025 12:07:08.800 * Loading RDB produced by version 7.4.2
redis       | 2025-04-10 09:07:08.800 | 1:M 10 Apr 2025 12:07:08.800 * RDB age 16 seconds
redis       | 2025-04-10 09:07:08.800 | 1:M 10 Apr 2025 12:07:08.800 * RDB memory usage when created 1.45 Mb
redis       | 2025-04-10 09:07:08.800 | 1:M 10 Apr 2025 12:07:08.800 * Done loading RDB, keys loaded: 1, keys expired: 0.
redis       | 2025-04-10 09:07:08.800 | 1:M 10 Apr 2025 12:07:08.800 * DB loaded from disk: 0.000 seconds
redis       | 2025-04-10 09:07:08.800 | 1:M 10 Apr 2025 12:07:08.800 * Ready to accept connections tcp
redis       | 2025-04-10 09:08:38.476 | 1:signal-handler (1744286918) Received SIGTERM scheduling shutdown...
redis       | 2025-04-10 09:08:38.498 | 1:M 10 Apr 2025 12:08:38.498 * User requested shutdown...
redis       | 2025-04-10 09:08:38.498 | 1:M 10 Apr 2025 12:08:38.498 * Saving the final RDB snapshot before exiting.
redis       | 2025-04-10 09:08:38.502 | 1:M 10 Apr 2025 12:08:38.502 * DB saved on disk
redis       | 2025-04-10 09:08:38.503 | 1:M 10 Apr 2025 12:08:38.502 # Redis is now ready to exit, bye bye...
redis       | 2025-04-10 09:08:43.701 | 1:C 10 Apr 2025 12:08:43.699 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
redis       | 2025-04-10 09:08:43.701 | 1:C 10 Apr 2025 12:08:43.701 * Redis version=7.4.2, bits=64, commit=00000000, modified=0, pid=1, just started
redis       | 2025-04-10 09:08:43.704 | 1:C 10 Apr 2025 12:08:43.701 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
redis       | 2025-04-10 09:08:43.705 | 1:M 10 Apr 2025 12:08:43.705 * monotonic clock: POSIX clock_gettime
redis       | 2025-04-10 09:08:43.706 | 1:M 10 Apr 2025 12:08:43.706 * Running mode=standalone, port=6379.
redis       | 2025-04-10 09:08:43.707 | 1:M 10 Apr 2025 12:08:43.707 * Server initialized
redis       | 2025-04-10 09:08:43.707 | 1:M 10 Apr 2025 12:08:43.707 * Loading RDB produced by version 7.4.2
redis       | 2025-04-10 09:08:43.707 | 1:M 10 Apr 2025 12:08:43.707 * RDB age 5 seconds
redis       | 2025-04-10 09:08:43.707 | 1:M 10 Apr 2025 12:08:43.707 * RDB memory usage when created 1.37 Mb
redis       | 2025-04-10 09:08:43.707 | 1:M 10 Apr 2025 12:08:43.707 * Done loading RDB, keys loaded: 3, keys expired: 0.
redis       | 2025-04-10 09:08:43.707 | 1:M 10 Apr 2025 12:08:43.707 * DB loaded from disk: 0.000 seconds
redis       | 2025-04-10 09:08:43.707 | 1:M 10 Apr 2025 12:08:43.707 * Ready to accept connections tcp
redis       | 2025-04-10 09:09:10.876 | 1:signal-handler (1744286950) Received SIGTERM scheduling shutdown...
redis       | 2025-04-10 09:09:10.921 | 1:M 10 Apr 2025 12:09:10.921 * User requested shutdown...
redis       | 2025-04-10 09:09:10.922 | 1:M 10 Apr 2025 12:09:10.922 * Saving the final RDB snapshot before exiting.
redis       | 2025-04-10 09:09:10.925 | 1:M 10 Apr 2025 12:09:10.924 * DB saved on disk
redis       | 2025-04-10 09:09:10.925 | 1:M 10 Apr 2025 12:09:10.924 # Redis is now ready to exit, bye bye...
nginx       | 2025-04-10 08:52:40.686 | /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
nginx       | 2025-04-10 08:52:40.686 | /docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
nginx       | 2025-04-10 08:52:40.686 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
nginx       | 2025-04-10 08:52:40.692 | 10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
nginx       | 2025-04-10 08:52:40.699 | 10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
nginx       | 2025-04-10 08:52:40.700 | /docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
nginx       | 2025-04-10 08:52:40.700 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
nginx       | 2025-04-10 08:52:40.704 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
nginx       | 2025-04-10 08:52:40.706 | /docker-entrypoint.sh: Configuration complete; ready for start up
nginx       | 2025-04-10 08:59:10.301 | 172.18.0.1 - - [10/Apr/2025:11:59:10 +0000] "GET / HTTP/1.1" 200 14839 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
nginx       | 2025-04-10 08:59:10.321 | 172.18.0.1 - - [10/Apr/2025:11:59:10 +0000] "GET /static/css/styles.css HTTP/1.1" 200 7633 "http://192.168.10.11:5080/" "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
nginx       | 2025-04-10 08:59:10.406 | 172.18.0.1 - - [10/Apr/2025:11:59:10 +0000] "GET /static/images/login-background1.jpg HTTP/1.1" 200 6345054 "http://192.168.10.11:5080/static/css/styles.css" "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
nginx       | 2025-04-10 08:59:10.667 | 172.18.0.1 - - [10/Apr/2025:11:59:10 +0000] "GET /favicon.ico HTTP/1.1" 404 3637 "http://192.168.10.11:5080/" "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
nginx       | 2025-04-10 08:59:19.217 | 172.18.0.1 - - [10/Apr/2025:11:59:19 +0000] "POST /registrar/entrada/ HTTP/1.1" 200 97 "http://192.168.10.11:5080/" "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
nginx       | 2025-04-10 08:59:41.628 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /admin/ HTTP/1.1" 200 38776 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.646 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin/css/base.css HTTP/1.1" 200 22092 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.649 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin/css/dark_mode.css HTTP/1.1" 200 2804 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.650 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin/js/theme.js HTTP/1.1" 200 1653 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.654 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin/css/nav_sidebar.css HTTP/1.1" 200 2810 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.655 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/css/admin-interface.css?v=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 17679 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.655 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/css/changelist.css?v=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 1246 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.656 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/css/change-form.css?v=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 1125 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.656 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/css/file-upload.css?v=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 1169 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.656 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/css/fieldsets.css?v=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 499 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.657 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/css/header.css?v=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 1009 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.658 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/css/inlines.css?v=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 2715 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.658 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/css/jquery.ui.tabs.css?v=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 5558 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.658 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/css/language-chooser.css?v=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 1734 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.659 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/css/list-filter.css?v=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 614 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.659 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/css/list-filter-dropdown.css?v=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 691 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.660 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/css/login.css?v=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 1240 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.660 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/css/modules.css?v=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 404 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.660 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/css/nav-sidebar.css?v=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 2025 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.661 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/css/paginator.css?v=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 797 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.661 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/css/object-tools.css?v=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 319 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.662 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/css/rtl.css?v=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 1016 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.662 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/css/sticky-form-controls.css?v=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 2437 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.662 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/css/tabbed-changeform.css?v=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 1895 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.663 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/css/widgets.css?v=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 4752 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.663 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/css/third-party/ckeditor.css?v=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 2720 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.664 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/css/third-party/import-export.css?v=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 189 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.664 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/css/third-party/json-widget.css?v=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 993 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.664 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/css/third-party/modeltranslation.css?v=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 356 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.665 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/css/third-party/rangefilter.css?v=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 1238 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.666 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/css/third-party/sorl-thumbnail.css?v=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 1451 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.666 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/css/third-party/streamfield.css?v=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 6407 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.666 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/css/third-party/tinymce.css?v=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 78 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.667 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin/css/dashboard.css HTTP/1.1" 200 441 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.667 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin/css/responsive.css HTTP/1.1" 200 17972 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.667 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin/css/responsive.css?nocache=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 17972 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.667 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin/css/responsive_rtl.css?nocache=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 2544 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.668 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/foldable-apps/foldable-apps.css?nocache=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 1955 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.669 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/magnific-popup/magnific-popup.css?nocache=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 6951 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.669 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/related-modal/related-modal.css?v=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 2888 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.670 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/foldable-apps/foldable-apps.js?nocache=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 1750 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.670 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/magnific-popup/jquery.magnific-popup.js?nocache=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 60830 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.671 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin_interface/related-modal/related-modal.js?nocache=42345859042311fcac2b2a49c8b09d24faa4959d8a7aad5855e1c68c HTTP/1.1" 200 7032 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.672 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1" 404 555 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.726 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin/js/nav_sidebar.js HTTP/1.1" 200 3063 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.731 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin/img/icon-viewlink.svg HTTP/1.1" 200 581 "http://localhost:5080/static/admin/css/base.css" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.731 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin/img/icon-changelink.svg HTTP/1.1" 200 380 "http://localhost:5080/static/admin/css/base.css" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.731 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /static/admin/img/icon-addlink.svg HTTP/1.1" 200 331 "http://localhost:5080/static/admin/css/base.css" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:41.783 | 172.18.0.1 - - [10/Apr/2025:11:59:41 +0000] "GET /favicon.ico HTTP/1.1" 404 3633 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:44.685 | 172.18.0.1 - - [10/Apr/2025:11:59:44 +0000] "GET /admin/reloj_fichador/registrodiario/ HTTP/1.1" 200 49170 "http://localhost:5080/admin/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:44.702 | 172.18.0.1 - - [10/Apr/2025:11:59:44 +0000] "GET /static/admin/css/changelists.css HTTP/1.1" 200 6878 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:44.705 | 172.18.0.1 - - [10/Apr/2025:11:59:44 +0000] "GET /static/admin/js/vendor/jquery/jquery.js HTTP/1.1" 200 285314 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:44.705 | 172.18.0.1 - - [10/Apr/2025:11:59:44 +0000] "GET /static/admin/js/jquery.init.js HTTP/1.1" 200 347 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:44.705 | 172.18.0.1 - - [10/Apr/2025:11:59:44 +0000] "GET /static/admin/js/core.js HTTP/1.1" 200 6208 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:44.706 | 172.18.0.1 - - [10/Apr/2025:11:59:44 +0000] "GET /static/admin/js/actions.js HTTP/1.1" 200 8076 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:44.706 | 172.18.0.1 - - [10/Apr/2025:11:59:44 +0000] "GET /static/admin/js/admin/RelatedObjectLookups.js HTTP/1.1" 200 9097 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:44.707 | 172.18.0.1 - - [10/Apr/2025:11:59:44 +0000] "GET /static/admin/js/urlify.js HTTP/1.1" 200 7887 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:44.707 | 172.18.0.1 - - [10/Apr/2025:11:59:44 +0000] "GET /static/admin/js/prepopulate.js HTTP/1.1" 200 1531 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:44.709 | 172.18.0.1 - - [10/Apr/2025:11:59:44 +0000] "GET /static/admin/js/vendor/xregexp/xregexp.js HTTP/1.1" 200 325171 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:44.710 | 172.18.0.1 - - [10/Apr/2025:11:59:44 +0000] "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1" 404 555 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:44.715 | 172.18.0.1 - - [10/Apr/2025:11:59:44 +0000] "GET /admin/jsi18n/ HTTP/1.1" 200 8691 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:44.771 | 172.18.0.1 - - [10/Apr/2025:11:59:44 +0000] "GET /static/admin/css/widgets.css HTTP/1.1" 200 11564 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:44.777 | 172.18.0.1 - - [10/Apr/2025:11:59:44 +0000] "GET /static/admin/js/filters.js HTTP/1.1" 200 978 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:44.792 | 172.18.0.1 - - [10/Apr/2025:11:59:44 +0000] "GET /static/admin/img/tooltag-add.svg HTTP/1.1" 200 331 "http://localhost:5080/static/admin/css/base.css" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:44.811 | 172.18.0.1 - - [10/Apr/2025:11:59:44 +0000] "GET /static/admin/js/calendar.js HTTP/1.1" 200 9141 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:44.811 | 172.18.0.1 - - [10/Apr/2025:11:59:44 +0000] "GET /static/admin/js/admin/DateTimeShortcuts.js HTTP/1.1" 200 19319 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:44.846 | 172.18.0.1 - - [10/Apr/2025:11:59:44 +0000] "GET /static/admin/img/icon-calendar.svg HTTP/1.1" 200 1086 "http://localhost:5080/static/admin/css/widgets.css" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:53.914 | 172.18.0.1 - - [10/Apr/2025:11:59:53 +0000] "GET /admin/reloj_fichador/registrodiario/999/change/ HTTP/1.1" 200 56001 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:53.932 | 172.18.0.1 - - [10/Apr/2025:11:59:53 +0000] "GET /static/admin/css/forms.css HTTP/1.1" 200 8794 "http://localhost:5080/admin/reloj_fichador/registrodiario/999/change/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:53.933 | 172.18.0.1 - - [10/Apr/2025:11:59:53 +0000] "GET /static/admin/js/prepopulate_init.js HTTP/1.1" 200 586 "http://localhost:5080/admin/reloj_fichador/registrodiario/999/change/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:53.933 | 172.18.0.1 - - [10/Apr/2025:11:59:53 +0000] "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1" 404 555 "http://localhost:5080/admin/reloj_fichador/registrodiario/999/change/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:53.941 | 172.18.0.1 - - [10/Apr/2025:11:59:53 +0000] "GET /admin/jsi18n/ HTTP/1.1" 200 8691 "http://localhost:5080/admin/reloj_fichador/registrodiario/999/change/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:53.995 | 172.18.0.1 - - [10/Apr/2025:11:59:53 +0000] "GET /static/admin/js/change_form.js HTTP/1.1" 200 606 "http://localhost:5080/admin/reloj_fichador/registrodiario/999/change/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 08:59:54.052 | 172.18.0.1 - - [10/Apr/2025:11:59:54 +0000] "GET /static/admin/img/icon-clock.svg HTTP/1.1" 200 677 "http://localhost:5080/static/admin/css/widgets.css" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 09:00:04.645 | 172.18.0.1 - - [10/Apr/2025:12:00:04 +0000] "POST /admin/reloj_fichador/registrodiario/999/change/ HTTP/1.1" 302 0 "http://localhost:5080/admin/reloj_fichador/registrodiario/999/change/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 09:00:04.728 | 172.18.0.1 - - [10/Apr/2025:12:00:04 +0000] "GET /admin/reloj_fichador/registrodiario/ HTTP/1.1" 200 49452 "http://localhost:5080/admin/reloj_fichador/registrodiario/999/change/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 09:00:04.750 | 172.18.0.1 - - [10/Apr/2025:12:00:04 +0000] "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1" 404 555 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 09:00:04.757 | 172.18.0.1 - - [10/Apr/2025:12:00:04 +0000] "GET /admin/jsi18n/ HTTP/1.1" 200 8691 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 09:00:06.073 | 172.18.0.1 - - [10/Apr/2025:12:00:06 +0000] "GET /admin/reloj_fichador/registrodiario/add/ HTTP/1.1" 200 55641 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 09:00:06.096 | 172.18.0.1 - - [10/Apr/2025:12:00:06 +0000] "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1" 404 555 "http://localhost:5080/admin/reloj_fichador/registrodiario/add/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 09:00:06.103 | 172.18.0.1 - - [10/Apr/2025:12:00:06 +0000] "GET /admin/jsi18n/ HTTP/1.1" 200 8691 "http://localhost:5080/admin/reloj_fichador/registrodiario/add/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 09:00:11.093 | 172.18.0.1 - - [10/Apr/2025:12:00:11 +0000] "GET /static/images/login-background2.jpg HTTP/1.1" 200 3881665 "http://192.168.10.11:5080/" "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
nginx       | 2025-04-10 09:00:17.431 | 172.18.0.1 - - [10/Apr/2025:12:00:17 +0000] "POST /admin/reloj_fichador/registrodiario/add/ HTTP/1.1" 302 0 "http://localhost:5080/admin/reloj_fichador/registrodiario/add/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 09:00:17.513 | 172.18.0.1 - - [10/Apr/2025:12:00:17 +0000] "GET /admin/reloj_fichador/registrodiario/ HTTP/1.1" 200 50358 "http://localhost:5080/admin/reloj_fichador/registrodiario/add/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 09:00:17.534 | 172.18.0.1 - - [10/Apr/2025:12:00:17 +0000] "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1" 404 555 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 09:00:17.542 | 172.18.0.1 - - [10/Apr/2025:12:00:17 +0000] "GET /admin/jsi18n/ HTTP/1.1" 200 8691 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 09:00:23.432 | 172.18.0.1 - - [10/Apr/2025:12:00:23 +0000] "GET /admin/reloj_fichador/horas_totales/ HTTP/1.1" 200 36209 "http://localhost:5080/admin/reloj_fichador/registrodiario/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 09:00:23.448 | 172.18.0.1 - - [10/Apr/2025:12:00:23 +0000] "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1" 404 555 "http://localhost:5080/admin/reloj_fichador/horas_totales/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 09:00:23.456 | 172.18.0.1 - - [10/Apr/2025:12:00:23 +0000] "GET /admin/jsi18n/ HTTP/1.1" 200 8691 "http://localhost:5080/admin/reloj_fichador/horas_totales/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 09:00:27.268 | 172.18.0.1 - - [10/Apr/2025:12:00:27 +0000] "GET /admin/reloj_fichador/horas_feriado/ HTTP/1.1" 200 38089 "http://localhost:5080/admin/reloj_fichador/horas_totales/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 09:00:27.286 | 172.18.0.1 - - [10/Apr/2025:12:00:27 +0000] "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1" 404 555 "http://localhost:5080/admin/reloj_fichador/horas_feriado/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 09:00:27.293 | 172.18.0.1 - - [10/Apr/2025:12:00:27 +0000] "GET /admin/jsi18n/ HTTP/1.1" 200 8691 "http://localhost:5080/admin/reloj_fichador/horas_feriado/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 09:00:28.061 | 172.18.0.1 - - [10/Apr/2025:12:00:28 +0000] "GET /admin/reloj_fichador/horas_extras/ HTTP/1.1" 200 40062 "http://localhost:5080/admin/reloj_fichador/horas_feriado/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 09:00:28.080 | 172.18.0.1 - - [10/Apr/2025:12:00:28 +0000] "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1" 404 555 "http://localhost:5080/admin/reloj_fichador/horas_extras/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 09:00:28.087 | 172.18.0.1 - - [10/Apr/2025:12:00:28 +0000] "GET /admin/jsi18n/ HTTP/1.1" 200 8691 "http://localhost:5080/admin/reloj_fichador/horas_extras/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 09:00:30.907 | 172.18.0.1 - - [10/Apr/2025:12:00:30 +0000] "GET /admin/reloj_fichador/horas_trabajadas/ HTTP/1.1" 200 40939 "http://localhost:5080/admin/reloj_fichador/horas_extras/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 09:00:30.929 | 172.18.0.1 - - [10/Apr/2025:12:00:30 +0000] "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1" 404 555 "http://localhost:5080/admin/reloj_fichador/horas_trabajadas/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 09:00:30.936 | 172.18.0.1 - - [10/Apr/2025:12:00:30 +0000] "GET /admin/jsi18n/ HTTP/1.1" 200 8691 "http://localhost:5080/admin/reloj_fichador/horas_trabajadas/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
nginx       | 2025-04-10 09:01:11.759 | 172.18.0.1 - - [10/Apr/2025:12:01:11 +0000] "GET /static/images/login-background3.jpg HTTP/1.1" 200 4751255 "http://192.168.10.11:5080/" "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
nginx       | 2025-04-10 09:02:12.426 | 172.18.0.1 - - [10/Apr/2025:12:02:12 +0000] "GET /static/images/login-background4.jpg HTTP/1.1" 200 8356032 "http://192.168.10.11:5080/" "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
nginx       | 2025-04-10 09:03:13.087 | 172.18.0.1 - - [10/Apr/2025:12:03:13 +0000] "GET /static/images/login-background5.jpg HTTP/1.1" 200 3447518 "http://192.168.10.11:5080/" "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
nginx       | 2025-04-10 09:04:10.421 | 172.18.0.1 - - [10/Apr/2025:12:04:10 +0000] "GET /static/images/login-background6.jpg HTTP/1.1" 200 3365175 "http://192.168.10.11:5080/" "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
nginx       | 2025-04-10 09:04:17.271 | /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
nginx       | 2025-04-10 09:04:17.271 | /docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
nginx       | 2025-04-10 09:04:17.271 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
nginx       | 2025-04-10 09:04:17.273 | 10-listen-on-ipv6-by-default.sh: info: IPv6 listen already enabled
nginx       | 2025-04-10 09:04:17.273 | /docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
nginx       | 2025-04-10 09:04:17.273 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
nginx       | 2025-04-10 09:04:17.275 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
nginx       | 2025-04-10 09:04:17.282 | /docker-entrypoint.sh: Configuration complete; ready for start up
nginx       | 2025-04-10 09:05:11.183 | 172.18.0.1 - - [10/Apr/2025:12:05:11 +0000] "GET /static/images/login-background7.jpg HTTP/1.1" 200 12077575 "http://192.168.10.11:5080/" "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
nginx       | 2025-04-10 09:06:11.767 | 172.18.0.1 - - [10/Apr/2025:12:06:11 +0000] "GET /static/images/login-background8.jpg HTTP/1.1" 200 3836655 "http://192.168.10.11:5080/" "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
nginx       | 2025-04-10 09:07:09.371 | /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
nginx       | 2025-04-10 09:07:09.371 | /docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
nginx       | 2025-04-10 09:07:09.371 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
nginx       | 2025-04-10 09:07:09.373 | 10-listen-on-ipv6-by-default.sh: info: IPv6 listen already enabled
nginx       | 2025-04-10 09:07:09.373 | /docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
nginx       | 2025-04-10 09:07:09.373 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
nginx       | 2025-04-10 09:07:09.377 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
nginx       | 2025-04-10 09:07:09.379 | /docker-entrypoint.sh: Configuration complete; ready for start up
nginx       | 2025-04-10 09:08:44.121 | /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
nginx       | 2025-04-10 09:08:44.121 | /docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
nginx       | 2025-04-10 09:08:44.122 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
nginx       | 2025-04-10 09:08:44.125 | 10-listen-on-ipv6-by-default.sh: info: IPv6 listen already enabled
nginx       | 2025-04-10 09:08:44.125 | /docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
nginx       | 2025-04-10 09:08:44.125 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
nginx       | 2025-04-10 09:08:44.129 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
nginx       | 2025-04-10 09:08:44.131 | /docker-entrypoint.sh: Configuration complete; ready for start up
nginx       | 2025-04-10 09:09:16.420 | /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
nginx       | 2025-04-10 09:09:16.420 | /docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
nginx       | 2025-04-10 09:09:16.422 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
nginx       | 2025-04-10 09:09:16.436 | 10-listen-on-ipv6-by-default.sh: info: IPv6 listen already enabled
nginx       | 2025-04-10 09:09:16.436 | /docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
nginx       | 2025-04-10 09:09:16.436 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
nginx       | 2025-04-10 09:09:16.436 | /docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
nginx       | 2025-04-10 09:09:16.436 | /docker-entrypoint.sh: Configuration complete; ready for start up
nginx       | 2025-04-10 08:59:41.672 | 2025/04/10 11:59:41 [error] 29#29: *6 open() "/app/media/admin-interface/logo/logo_hores.png" failed (2: No such file or directory), client: 172.18.0.1, server: localhost, request: "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1", host: "localhost:5080", referrer: "http://localhost:5080/admin/"
nginx       | 2025-04-10 08:59:44.710 | 2025/04/10 11:59:44 [error] 29#29: *12 open() "/app/media/admin-interface/logo/logo_hores.png" failed (2: No such file or directory), client: 172.18.0.1, server: localhost, request: "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1", host: "localhost:5080", referrer: "http://localhost:5080/admin/reloj_fichador/registrodiario/"
nginx       | 2025-04-10 08:59:53.933 | 2025/04/10 11:59:53 [error] 29#29: *10 open() "/app/media/admin-interface/logo/logo_hores.png" failed (2: No such file or directory), client: 172.18.0.1, server: localhost, request: "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1", host: "localhost:5080", referrer: "http://localhost:5080/admin/reloj_fichador/registrodiario/999/change/"
nginx       | 2025-04-10 09:00:04.750 | 2025/04/10 12:00:04 [error] 29#29: *10 open() "/app/media/admin-interface/logo/logo_hores.png" failed (2: No such file or directory), client: 172.18.0.1, server: localhost, request: "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1", host: "localhost:5080", referrer: "http://localhost:5080/admin/reloj_fichador/registrodiario/"
nginx       | 2025-04-10 09:00:06.096 | 2025/04/10 12:00:06 [error] 29#29: *10 open() "/app/media/admin-interface/logo/logo_hores.png" failed (2: No such file or directory), client: 172.18.0.1, server: localhost, request: "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1", host: "localhost:5080", referrer: "http://localhost:5080/admin/reloj_fichador/registrodiario/add/"
nginx       | 2025-04-10 09:00:17.534 | 2025/04/10 12:00:17 [error] 29#29: *10 open() "/app/media/admin-interface/logo/logo_hores.png" failed (2: No such file or directory), client: 172.18.0.1, server: localhost, request: "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1", host: "localhost:5080", referrer: "http://localhost:5080/admin/reloj_fichador/registrodiario/"
nginx       | 2025-04-10 09:00:23.448 | 2025/04/10 12:00:23 [error] 29#29: *10 open() "/app/media/admin-interface/logo/logo_hores.png" failed (2: No such file or directory), client: 172.18.0.1, server: localhost, request: "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1", host: "localhost:5080", referrer: "http://localhost:5080/admin/reloj_fichador/horas_totales/"
nginx       | 2025-04-10 09:00:27.286 | 2025/04/10 12:00:27 [error] 29#29: *10 open() "/app/media/admin-interface/logo/logo_hores.png" failed (2: No such file or directory), client: 172.18.0.1, server: localhost, request: "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1", host: "localhost:5080", referrer: "http://localhost:5080/admin/reloj_fichador/horas_feriado/"
nginx       | 2025-04-10 09:00:28.080 | 2025/04/10 12:00:28 [error] 29#29: *10 open() "/app/media/admin-interface/logo/logo_hores.png" failed (2: No such file or directory), client: 172.18.0.1, server: localhost, request: "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1", host: "localhost:5080", referrer: "http://localhost:5080/admin/reloj_fichador/horas_extras/"
nginx       | 2025-04-10 09:00:30.929 | 2025/04/10 12:00:30 [error] 29#29: *10 open() "/app/media/admin-interface/logo/logo_hores.png" failed (2: No such file or directory), client: 172.18.0.1, server: localhost, request: "GET /media/admin-interface/logo/logo_hores.png HTTP/1.1", host: "localhost:5080", referrer: "http://localhost:5080/admin/reloj_fichador/horas_trabajadas/"
redis       | 2025-04-10 09:09:16.447 | 1:C 10 Apr 2025 12:09:16.447 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
redis       | 2025-04-10 09:09:16.447 | 1:C 10 Apr 2025 12:09:16.447 * Redis version=7.4.2, bits=64, commit=00000000, modified=0, pid=1, just started
redis       | 2025-04-10 09:09:16.447 | 1:C 10 Apr 2025 12:09:16.447 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
redis       | 2025-04-10 09:09:16.447 | 1:M 10 Apr 2025 12:09:16.447 * monotonic clock: POSIX clock_gettime
redis       | 2025-04-10 09:09:16.447 | 1:M 10 Apr 2025 12:09:16.447 * Running mode=standalone, port=6379.
redis       | 2025-04-10 09:09:16.448 | 1:M 10 Apr 2025 12:09:16.448 * Server initialized
redis       | 2025-04-10 09:09:16.448 | 1:M 10 Apr 2025 12:09:16.448 * Loading RDB produced by version 7.4.2
redis       | 2025-04-10 09:09:16.448 | 1:M 10 Apr 2025 12:09:16.448 * RDB age 6 seconds
redis       | 2025-04-10 09:09:16.448 | 1:M 10 Apr 2025 12:09:16.448 * RDB memory usage when created 1.39 Mb
redis       | 2025-04-10 09:09:16.448 | 1:M 10 Apr 2025 12:09:16.448 * Done loading RDB, keys loaded: 3, keys expired: 0.
redis       | 2025-04-10 09:09:16.448 | 1:M 10 Apr 2025 12:09:16.448 * DB loaded from disk: 0.000 seconds
redis       | 2025-04-10 09:09:16.448 | 1:M 10 Apr 2025 12:09:16.448 * Ready to accept connections tcp
web         | 2025-04-10 08:52:40.353 | wait-for-it.sh: waiting 15 seconds for db:3306
web         | 2025-04-10 08:52:43.361 | wait-for-it.sh: db:3306 is available after 3 seconds
web         | 2025-04-10 08:52:46.074 | [2025-04-10 11:52:46 +0000] [1] [INFO] Starting gunicorn 23.0.0
web         | 2025-04-10 08:52:46.074 | [2025-04-10 11:52:46 +0000] [1] [INFO] Listening at: http://0.0.0.0:58000 (1)
web         | 2025-04-10 08:52:46.074 | [2025-04-10 11:52:46 +0000] [1] [INFO] Using worker: sync
web         | 2025-04-10 08:52:46.075 | [2025-04-10 11:52:46 +0000] [86] [INFO] Booting worker with pid: 86
web         | 2025-04-10 08:52:46.163 | [2025-04-10 11:52:46 +0000] [87] [INFO] Booting worker with pid: 87
web         | 2025-04-10 08:52:46.259 | [2025-04-10 11:52:46 +0000] [88] [INFO] Booting worker with pid: 88
web         | 2025-04-10 08:59:10.667 | Not Found: /favicon.ico
web         | 2025-04-10 08:59:19.198 | Registros desbalancados para el operario PIZARRO, LEANDRO E. - 39610329 en la fecha 2025-04-10.
web         | 2025-04-10 08:59:41.611 | /usr/local/lib/python3.11/site-packages/admin_interface/templatetags/admin_interface_tags.py:38: UserWarning: Language chooser requires Django's `set_language` view: `urlpatterns += [url(r'^i18n/', include('django.conf.urls.i18n'))]`.
web         | 2025-04-10 08:59:41.611 |   warnings.warn(
web         | 2025-04-10 08:59:41.783 | Not Found: /favicon.ico
web         | 2025-04-10 08:59:44.636 | /usr/local/lib/python3.11/site-packages/admin_interface/templatetags/admin_interface_tags.py:38: UserWarning: Language chooser requires Django's `set_language` view: `urlpatterns += [url(r'^i18n/', include('django.conf.urls.i18n'))]`.
web         | 2025-04-10 08:59:44.636 |   warnings.warn(
web         | 2025-04-10 08:59:53.872 | /usr/local/lib/python3.11/site-packages/admin_interface/templatetags/admin_interface_tags.py:38: UserWarning: Language chooser requires Django's `set_language` view: `urlpatterns += [url(r'^i18n/', include('django.conf.urls.i18n'))]`.
web         | 2025-04-10 08:59:53.872 |   warnings.warn(
web         | 2025-04-10 09:00:04.628 | Registros desbalancados para el operario PIZARRO, LEANDRO E. - 39610329 en la fecha 2025-04-10.
web         | 2025-04-10 09:04:11.609 | [2025-04-10 12:04:11 +0000] [1] [INFO] Handling signal: term
web         | 2025-04-10 09:04:11.609 | [2025-04-10 09:04:11 -0300] [86] [INFO] Worker exiting (pid: 86)
web         | 2025-04-10 09:04:11.609 | [2025-04-10 09:04:11 -0300] [87] [INFO] Worker exiting (pid: 87)
web         | 2025-04-10 09:04:11.621 | [2025-04-10 09:04:11 -0300] [88] [INFO] Worker exiting (pid: 88)
web         | 2025-04-10 09:04:11.909 | [2025-04-10 12:04:11 +0000] [1] [INFO] Shutting down: Master
web         | 2025-04-10 09:04:17.352 | wait-for-it.sh: waiting 15 seconds for db:3306
web         | 2025-04-10 09:04:21.360 | wait-for-it.sh: db:3306 is available after 4 seconds
web         | 2025-04-10 09:04:23.750 | [2025-04-10 12:04:23 +0000] [1] [INFO] Starting gunicorn 23.0.0
web         | 2025-04-10 09:04:23.751 | [2025-04-10 12:04:23 +0000] [1] [INFO] Listening at: http://0.0.0.0:58000 (1)
web         | 2025-04-10 09:04:23.751 | [2025-04-10 12:04:23 +0000] [1] [INFO] Using worker: sync
web         | 2025-04-10 09:04:23.752 | [2025-04-10 12:04:23 +0000] [88] [INFO] Booting worker with pid: 88
web         | 2025-04-10 09:04:23.818 | [2025-04-10 12:04:23 +0000] [89] [INFO] Booting worker with pid: 89
web         | 2025-04-10 09:04:23.902 | [2025-04-10 12:04:23 +0000] [90] [INFO] Booting worker with pid: 90
web         | 2025-04-10 09:06:51.074 | [2025-04-10 12:06:51 +0000] [1] [INFO] Handling signal: term
web         | 2025-04-10 09:06:51.078 | [2025-04-10 09:06:51 -0300] [89] [INFO] Worker exiting (pid: 89)
web         | 2025-04-10 09:06:51.078 | [2025-04-10 09:06:51 -0300] [90] [INFO] Worker exiting (pid: 90)
web         | 2025-04-10 09:06:51.078 | [2025-04-10 09:06:51 -0300] [88] [INFO] Worker exiting (pid: 88)
web         | 2025-04-10 09:06:51.375 | [2025-04-10 12:06:51 +0000] [1] [INFO] Shutting down: Master
web         | 2025-04-10 09:07:09.207 | wait-for-it.sh: waiting 15 seconds for db:3306
web         | 2025-04-10 09:07:11.214 | wait-for-it.sh: db:3306 is available after 2 seconds
web         | 2025-04-10 09:07:13.657 | [2025-04-10 12:07:13 +0000] [1] [INFO] Starting gunicorn 23.0.0
web         | 2025-04-10 09:07:13.657 | [2025-04-10 12:07:13 +0000] [1] [INFO] Listening at: http://0.0.0.0:58000 (1)
web         | 2025-04-10 09:07:13.657 | [2025-04-10 12:07:13 +0000] [1] [INFO] Using worker: sync
web         | 2025-04-10 09:07:13.658 | [2025-04-10 12:07:13 +0000] [84] [INFO] Booting worker with pid: 84
web         | 2025-04-10 09:07:13.697 | [2025-04-10 12:07:13 +0000] [85] [INFO] Booting worker with pid: 85
web         | 2025-04-10 09:07:13.724 | [2025-04-10 12:07:13 +0000] [86] [INFO] Booting worker with pid: 86
web         | 2025-04-10 09:08:38.499 | [2025-04-10 12:08:38 +0000] [1] [INFO] Handling signal: term
web         | 2025-04-10 09:08:38.499 | [2025-04-10 09:08:38 -0300] [85] [INFO] Worker exiting (pid: 85)
web         | 2025-04-10 09:08:38.499 | [2025-04-10 09:08:38 -0300] [84] [INFO] Worker exiting (pid: 84)
web         | 2025-04-10 09:08:38.509 | [2025-04-10 09:08:38 -0300] [86] [INFO] Worker exiting (pid: 86)
web         | 2025-04-10 09:08:38.552 | [2025-04-10 12:08:38 +0000] [1] [INFO] Shutting down: Master
web         | 2025-04-10 09:08:44.139 | wait-for-it.sh: waiting 15 seconds for db:3306
web         | 2025-04-10 09:08:48.136 | wait-for-it.sh: db:3306 is available after 4 seconds
web         | 2025-04-10 09:08:50.305 | [2025-04-10 12:08:50 +0000] [1] [INFO] Starting gunicorn 23.0.0
web         | 2025-04-10 09:08:50.305 | [2025-04-10 12:08:50 +0000] [1] [INFO] Listening at: http://0.0.0.0:58000 (1)
web         | 2025-04-10 09:08:50.305 | [2025-04-10 12:08:50 +0000] [1] [INFO] Using worker: sync
web         | 2025-04-10 09:08:50.306 | [2025-04-10 12:08:50 +0000] [82] [INFO] Booting worker with pid: 82
web         | 2025-04-10 09:08:50.386 | [2025-04-10 12:08:50 +0000] [83] [INFO] Booting worker with pid: 83
web         | 2025-04-10 09:08:50.390 | [2025-04-10 12:08:50 +0000] [84] [INFO] Booting worker with pid: 84
web         | 2025-04-10 09:09:10.839 | [2025-04-10 12:09:10 +0000] [1] [INFO] Handling signal: term
web         | 2025-04-10 09:09:10.851 | [2025-04-10 09:09:10 -0300] [82] [INFO] Worker exiting (pid: 82)
web         | 2025-04-10 09:09:10.851 | [2025-04-10 09:09:10 -0300] [83] [INFO] Worker exiting (pid: 83)
web         | 2025-04-10 09:09:10.852 | [2025-04-10 09:09:10 -0300] [84] [INFO] Worker exiting (pid: 84)
web         | 2025-04-10 09:09:11.142 | [2025-04-10 12:09:11 +0000] [1] [INFO] Shutting down: Master
web         | 2025-04-10 08:52:44.739 | Operations to perform:
web         | 2025-04-10 08:52:44.739 |   Apply all migrations: admin, admin_interface, auth, contenttypes, django_celery_beat, django_celery_results, reloj_fichador, sessions
web         | 2025-04-10 08:52:44.739 | Running migrations:
web         | 2025-04-10 08:52:44.739 |   No migrations to apply.
web         | 2025-04-10 08:52:45.836 | Found another file with the destination path 'admin/js/cancel.js'. It will be ignored since only the first encountered file is collected. If this is not what you want, make sure every static file has a unique path.
web         | 2025-04-10 08:52:45.836 | Found another file with the destination path 'admin/js/popup_response.js'. It will be ignored since only the first encountered file is collected. If this is not what you want, make sure every static file has a unique path.
web         | 2025-04-10 08:52:45.836 | 
web         | 2025-04-10 08:52:45.836 | 0 static files copied to '/app/staticfiles', 225 unmodified.
web         | 2025-04-10 09:04:22.503 | Operations to perform:
web         | 2025-04-10 09:04:22.503 |   Apply all migrations: admin, admin_interface, auth, contenttypes, django_celery_beat, django_celery_results, reloj_fichador, sessions
web         | 2025-04-10 09:04:22.503 | Running migrations:
web         | 2025-04-10 09:04:22.503 |   No migrations to apply.
web         | 2025-04-10 09:04:23.553 | Found another file with the destination path 'admin/js/cancel.js'. It will be ignored since only the first encountered file is collected. If this is not what you want, make sure every static file has a unique path.
web         | 2025-04-10 09:04:23.553 | Found another file with the destination path 'admin/js/popup_response.js'. It will be ignored since only the first encountered file is collected. If this is not what you want, make sure every static file has a unique path.
web         | 2025-04-10 09:04:23.553 | 
web         | 2025-04-10 09:04:23.553 | 0 static files copied to '/app/staticfiles', 225 unmodified.
web         | 2025-04-10 09:07:12.447 | Operations to perform:
web         | 2025-04-10 09:07:12.447 |   Apply all migrations: admin, admin_interface, auth, contenttypes, django_celery_beat, django_celery_results, reloj_fichador, sessions
web         | 2025-04-10 09:07:12.447 | Running migrations:
web         | 2025-04-10 09:07:12.447 |   No migrations to apply.
web         | 2025-04-10 09:07:13.463 | Found another file with the destination path 'admin/js/cancel.js'. It will be ignored since only the first encountered file is collected. If this is not what you want, make sure every static file has a unique path.
web         | 2025-04-10 09:07:13.464 | Found another file with the destination path 'admin/js/popup_response.js'. It will be ignored since only the first encountered file is collected. If this is not what you want, make sure every static file has a unique path.
web         | 2025-04-10 09:07:13.464 | 
web         | 2025-04-10 09:07:13.464 | 0 static files copied to '/app/staticfiles', 225 unmodified.
web         | 2025-04-10 09:08:49.151 | Operations to perform:
web         | 2025-04-10 09:08:49.151 |   Apply all migrations: admin, admin_interface, auth, contenttypes, django_celery_beat, django_celery_results, reloj_fichador, sessions
web         | 2025-04-10 09:08:49.151 | Running migrations:
web         | 2025-04-10 09:08:49.151 |   No migrations to apply.
web         | 2025-04-10 09:08:50.124 | Found another file with the destination path 'admin/js/cancel.js'. It will be ignored since only the first encountered file is collected. If this is not what you want, make sure every static file has a unique path.
web         | 2025-04-10 09:08:50.124 | Found another file with the destination path 'admin/js/popup_response.js'. It will be ignored since only the first encountered file is collected. If this is not what you want, make sure every static file has a unique path.
web         | 2025-04-10 09:08:50.124 | 
web         | 2025-04-10 09:08:50.124 | 0 static files copied to '/app/staticfiles', 225 unmodified.
db          | 2025-04-10 09:09:16.578 | 2025-04-10 12:09:16+00:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 8.4.0-1.el9 started.
web         | 2025-04-10 09:09:16.583 | wait-for-it.sh: waiting 15 seconds for db:3306
celery      | 2025-04-10 09:09:16.705 | wait-for-it.sh: waiting 15 seconds for db:3306
birt        | 2025-04-10 09:09:16.749 | 10-Apr-2025 12:09:16.744 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Server version name:   Apache Tomcat/9.0.102
birt        | 2025-04-10 09:09:16.749 | 10-Apr-2025 12:09:16.749 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Server built:          Mar 3 2025 19:33:14 UTC
birt        | 2025-04-10 09:09:16.749 | 10-Apr-2025 12:09:16.749 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Server version number: 9.0.102.0
birt        | 2025-04-10 09:09:16.749 | 10-Apr-2025 12:09:16.749 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log OS Name:               Linux
birt        | 2025-04-10 09:09:16.749 | 10-Apr-2025 12:09:16.749 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log OS Version:            5.15.167.4-microsoft-standard-WSL2
birt        | 2025-04-10 09:09:16.749 | 10-Apr-2025 12:09:16.749 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Architecture:          amd64
birt        | 2025-04-10 09:09:16.749 | 10-Apr-2025 12:09:16.749 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Java Home:             /opt/java/openjdk
birt        | 2025-04-10 09:09:16.749 | 10-Apr-2025 12:09:16.749 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log JVM Version:           21.0.6+7-LTS
birt        | 2025-04-10 09:09:16.749 | 10-Apr-2025 12:09:16.749 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log JVM Vendor:            Eclipse Adoptium
birt        | 2025-04-10 09:09:16.750 | 10-Apr-2025 12:09:16.749 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log CATALINA_BASE:         /usr/local/tomcat
birt        | 2025-04-10 09:09:16.750 | 10-Apr-2025 12:09:16.750 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log CATALINA_HOME:         /usr/local/tomcat
birt        | 2025-04-10 09:09:16.756 | 10-Apr-2025 12:09:16.756 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.lang=ALL-UNNAMED
birt        | 2025-04-10 09:09:16.756 | 10-Apr-2025 12:09:16.756 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.lang.invoke=ALL-UNNAMED
birt        | 2025-04-10 09:09:16.756 | 10-Apr-2025 12:09:16.756 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.lang.reflect=ALL-UNNAMED
birt        | 2025-04-10 09:09:16.756 | 10-Apr-2025 12:09:16.756 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.io=ALL-UNNAMED
birt        | 2025-04-10 09:09:16.756 | 10-Apr-2025 12:09:16.756 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.util=ALL-UNNAMED
birt        | 2025-04-10 09:09:16.756 | 10-Apr-2025 12:09:16.756 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.base/java.util.concurrent=ALL-UNNAMED
birt        | 2025-04-10 09:09:16.756 | 10-Apr-2025 12:09:16.756 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: --add-opens=java.rmi/sun.rmi.transport=ALL-UNNAMED
birt        | 2025-04-10 09:09:16.757 | 10-Apr-2025 12:09:16.756 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.util.logging.config.file=/usr/local/tomcat/conf/logging.properties
birt        | 2025-04-10 09:09:16.757 | 10-Apr-2025 12:09:16.757 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager
birt        | 2025-04-10 09:09:16.757 | 10-Apr-2025 12:09:16.757 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.awt.headless=true
birt        | 2025-04-10 09:09:16.757 | 10-Apr-2025 12:09:16.757 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djdk.tls.ephemeralDHKeySize=2048
birt        | 2025-04-10 09:09:16.757 | 10-Apr-2025 12:09:16.757 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.protocol.handler.pkgs=org.apache.catalina.webresources
birt        | 2025-04-10 09:09:16.757 | 10-Apr-2025 12:09:16.757 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dsun.io.useCanonCaches=false
birt        | 2025-04-10 09:09:16.758 | 10-Apr-2025 12:09:16.757 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dorg.apache.catalina.security.SecurityListener.UMASK=0027
birt        | 2025-04-10 09:09:16.758 | 10-Apr-2025 12:09:16.758 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dignore.endorsed.dirs=
birt        | 2025-04-10 09:09:16.758 | 10-Apr-2025 12:09:16.758 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dcatalina.base=/usr/local/tomcat
birt        | 2025-04-10 09:09:16.758 | 10-Apr-2025 12:09:16.758 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dcatalina.home=/usr/local/tomcat
birt        | 2025-04-10 09:09:16.758 | 10-Apr-2025 12:09:16.758 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.io.tmpdir=/usr/local/tomcat/temp
birt        | 2025-04-10 09:09:16.760 | 10-Apr-2025 12:09:16.760 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent Loaded Apache Tomcat Native library [1.3.1] using APR version [1.7.2].
birt        | 2025-04-10 09:09:16.761 | 10-Apr-2025 12:09:16.761 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent APR capabilities: IPv6 [true], sendfile [true], accept filters [false], random [true], UDS [true].
birt        | 2025-04-10 09:09:16.761 | 10-Apr-2025 12:09:16.761 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent APR/OpenSSL configuration: useAprConnector [false], useOpenSSL [true]
birt        | 2025-04-10 09:09:16.764 | 10-Apr-2025 12:09:16.763 INFO [main] org.apache.catalina.core.AprLifecycleListener.initializeSSL OpenSSL successfully initialized [OpenSSL 3.0.13 30 Jan 2024]
db          | 2025-04-10 09:09:16.995 | 2025-04-10 12:09:16+00:00 [Note] [Entrypoint]: Switching to dedicated user 'mysql'
birt        | 2025-04-10 09:09:17.004 | 10-Apr-2025 12:09:17.004 INFO [main] org.apache.coyote.AbstractProtocol.init Initializing ProtocolHandler ["http-nio-8080"]
db          | 2025-04-10 09:09:17.004 | 2025-04-10 12:09:17+00:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 8.4.0-1.el9 started.
birt        | 2025-04-10 09:09:17.017 | 10-Apr-2025 12:09:17.016 INFO [main] org.apache.catalina.startup.Catalina.load Server initialization in [446] milliseconds
birt        | 2025-04-10 09:09:17.044 | 10-Apr-2025 12:09:17.044 INFO [main] org.apache.catalina.core.StandardService.startInternal Starting service [Catalina]
birt        | 2025-04-10 09:09:17.044 | 10-Apr-2025 12:09:17.044 INFO [main] org.apache.catalina.core.StandardEngine.startInternal Starting Servlet engine: [Apache Tomcat/9.0.102]
birt        | 2025-04-10 09:09:17.058 | 10-Apr-2025 12:09:17.058 INFO [main] org.apache.catalina.startup.HostConfig.deployWAR Deploying web application archive [/usr/local/tomcat/webapps/birt.war]
db          | 2025-04-10 09:09:17.187 | '/var/lib/mysql/mysql.sock' -> '/var/run/mysqld/mysqld.sock'
db          | 2025-04-10 09:09:17.377 | 2025-04-10T12:09:17.196777Z 0 [System] [MY-015015] [Server] MySQL Server - start.
db          | 2025-04-10 09:09:17.377 | 2025-04-10T12:09:17.374433Z 0 [System] [MY-010116] [Server] /usr/sbin/mysqld (mysqld 8.4.0) starting as process 1
db          | 2025-04-10 09:09:17.377 | 2025-04-10T12:09:17.377061Z 0 [Warning] [MY-010159] [Server] Setting lower_case_table_names=2 because file system for /var/lib/mysql/ is case insensitive
db          | 2025-04-10 09:09:17.385 | 2025-04-10T12:09:17.385525Z 1 [System] [MY-013576] [InnoDB] InnoDB initialization has started.
birt        | 2025-04-10 09:09:17.639 | 10-Apr-2025 12:09:17.638 INFO [main] org.apache.jasper.servlet.TldScanner.scanJars At least one JAR was scanned for TLDs yet contained no TLDs. Enable debug logging for this logger for a complete list of JARs that were scanned but no TLDs were found in them. Skipping unneeded JARs during scanning can improve startup time and JSP compilation time.
birt        | 2025-04-10 09:09:17.668 | 10-Apr-2025 12:09:17.668 INFO [main] org.apache.catalina.startup.HostConfig.deployWAR Deployment of web application archive [/usr/local/tomcat/webapps/birt.war] has finished in [609] ms
birt        | 2025-04-10 09:09:17.670 | 10-Apr-2025 12:09:17.670 INFO [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["http-nio-8080"]
birt        | 2025-04-10 09:09:17.679 | 10-Apr-2025 12:09:17.679 INFO [main] org.apache.catalina.startup.Catalina.start Server startup in [660] milliseconds
db          | 2025-04-10 09:09:18.136 | 2025-04-10T12:09:18.136134Z 1 [System] [MY-013577] [InnoDB] InnoDB initialization has ended.
db          | 2025-04-10 09:09:18.554 | 2025-04-10T12:09:18.554806Z 0 [Warning] [MY-010068] [Server] CA certificate ca.pem is self signed.
db          | 2025-04-10 09:09:18.555 | 2025-04-10T12:09:18.555282Z 0 [System] [MY-013602] [Server] Channel mysql_main configured to support TLS. Encrypted connections are now supported for this channel.
db          | 2025-04-10 09:09:18.565 | 2025-04-10T12:09:18.565300Z 0 [Warning] [MY-011810] [Server] Insecure configuration for --pid-file: Location '/var/run/mysqld' in the path is accessible to all OS users. Consider choosing a different directory.
web         | 2025-04-10 09:09:18.590 | wait-for-it.sh: db:3306 is available after 2 seconds
db          | 2025-04-10 09:09:18.609 | 2025-04-10T12:09:18.609611Z 0 [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections. Version: '8.4.0'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server - GPL.
celery      | 2025-04-10 09:09:18.711 | wait-for-it.sh: db:3306 is available after 2 seconds
db          | 2025-04-10 09:09:18.865 | 2025-04-10T12:09:18.864890Z 0 [System] [MY-011323] [Server] X Plugin ready for connections. Bind-address: '::' port: 33060, socket: /var/run/mysqld/mysqlx.sock
web         | 2025-04-10 09:09:19.624 | Operations to perform:
web         | 2025-04-10 09:09:19.624 |   Apply all migrations: admin, admin_interface, auth, contenttypes, django_celery_beat, django_celery_results, reloj_fichador, sessions
web         | 2025-04-10 09:09:19.624 | Running migrations:
web         | 2025-04-10 09:09:19.624 |   No migrations to apply.
celery      | 2025-04-10 09:09:19.691 |  
celery      | 2025-04-10 09:09:19.691 |  -------------- celery@336749e752ac v5.4.0 (opalescent)
celery      | 2025-04-10 09:09:19.691 | --- ***** ----- 
celery      | 2025-04-10 09:09:19.691 | -- ******* ---- Linux-5.15.167.4-microsoft-standard-WSL2-x86_64-with-glibc2.36 2025-04-10 09:09:19
celery      | 2025-04-10 09:09:19.691 | - *** --- * --- 
celery      | 2025-04-10 09:09:19.691 | - ** ---------- [config]
celery      | 2025-04-10 09:09:19.691 | - ** ---------- .> app:         mantenedor:0x7f1d7518e310
celery      | 2025-04-10 09:09:19.691 | - ** ---------- .> transport:   redis://redis:6379/5
celery      | 2025-04-10 09:09:19.691 | - ** ---------- .> results:     disabled://
celery      | 2025-04-10 09:09:19.691 | - *** --- * --- .> concurrency: 6 (prefork)
celery      | 2025-04-10 09:09:19.691 | -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
celery      | 2025-04-10 09:09:19.691 | --- ***** ----- 
celery      | 2025-04-10 09:09:19.691 |  -------------- [queues]
celery      | 2025-04-10 09:09:19.691 |                 .> celery           exchange=celery(direct) key=celery
celery      | 2025-04-10 09:09:19.691 |                 
celery      | 2025-04-10 09:09:19.691 | 
celery      | 2025-04-10 09:09:19.691 | [tasks]
celery      | 2025-04-10 09:09:19.691 |   . apps.reloj_fichador.tasks.crear_asistencia_prueba
celery      | 2025-04-10 09:09:19.691 |   . apps.reloj_fichador.tasks.generar_registros_asistencia
celery      | 2025-04-10 09:09:19.691 |   . apps.reloj_fichador.tasks.prueba_tarea
celery      | 2025-04-10 09:09:19.691 |   . mantenedor.celery.debug_task
celery      | 2025-04-10 09:09:19.691 | 
celery      | 2025-04-10 09:09:19.996 | [2025-04-10 09:09:19,995: INFO/MainProcess] Connected to redis://redis:6379/5
celery      | 2025-04-10 09:09:19.998 | [2025-04-10 09:09:19,998: INFO/MainProcess] mingle: searching for neighbors
celery-beat | 2025-04-10 09:09:20.126 | wait-for-it.sh: db:3306 is available after 4 seconds
web         | 2025-04-10 09:09:20.651 | Found another file with the destination path 'admin/js/cancel.js'. It will be ignored since only the first encountered file is collected. If this is not what you want, make sure every static file has a unique path.
web         | 2025-04-10 09:09:20.651 | Found another file with the destination path 'admin/js/popup_response.js'. It will be ignored since only the first encountered file is collected. If this is not what you want, make sure every static file has a unique path.
web         | 2025-04-10 09:09:20.651 | 
web         | 2025-04-10 09:09:20.651 | 0 static files copied to '/app/staticfiles', 225 unmodified.
web         | 2025-04-10 09:09:20.846 | [2025-04-10 12:09:20 +0000] [1] [INFO] Starting gunicorn 23.0.0
web         | 2025-04-10 09:09:20.846 | [2025-04-10 12:09:20 +0000] [1] [INFO] Listening at: http://0.0.0.0:58000 (1)
web         | 2025-04-10 09:09:20.846 | [2025-04-10 12:09:20 +0000] [1] [INFO] Using worker: sync
web         | 2025-04-10 09:09:20.847 | [2025-04-10 12:09:20 +0000] [84] [INFO] Booting worker with pid: 84
web         | 2025-04-10 09:09:20.939 | [2025-04-10 12:09:20 +0000] [85] [INFO] Booting worker with pid: 85
celery      | 2025-04-10 09:09:21.004 | [2025-04-10 09:09:21,004: INFO/MainProcess] mingle: all alone
celery      | 2025-04-10 09:09:21.013 | [2025-04-10 09:09:21,013: INFO/MainProcess] celery@336749e752ac ready.
web         | 2025-04-10 09:09:21.020 | [2025-04-10 12:09:21 +0000] [86] [INFO] Booting worker with pid: 86
celery-beat | 2025-04-10 09:09:21.216 | Operations to perform:
celery-beat | 2025-04-10 09:09:21.216 |   Apply all migrations: admin, admin_interface, auth, contenttypes, django_celery_beat, django_celery_results, reloj_fichador, sessions
celery-beat | 2025-04-10 09:09:21.216 | Running migrations:
celery-beat | 2025-04-10 09:09:21.216 |   No migrations to apply.
celery-beat | 2025-04-10 09:09:22.297 | [2025-04-10 09:09:22,297: INFO/MainProcess] beat: Starting...
celery-beat | 2025-04-10 09:09:22.335 | [2025-04-10 09:09:22,335: INFO/MainProcess] DatabaseScheduler: Schedule changed.
backup      | 2025-04-10 09:09:24.615 | wait-for-it.sh: waiting 15 seconds for db:3306
backup      | 2025-04-10 09:09:24.618 | wait-for-it.sh: db:3306 is available after 0 seconds
backup      | 2025-04-10 09:09:24.622 | mysqldump: [Warning] Using a password on the command line interface can be insecure.
celery-beat | 2025-04-10 09:10:00.003 | [2025-04-10 09:10:00,002: INFO/MainProcess] Scheduler: Sending due task generar-registros-asistencia-5am (apps.reloj_fichador.tasks.generar_registros_asistencia)
celery      | 2025-04-10 09:10:00.010 | [2025-04-10 09:10:00,010: INFO/MainProcess] Task apps.reloj_fichador.tasks.generar_registros_asistencia[be670336-4805-44b4-a85e-7d6d52a86f21] received
celery      | 2025-04-10 09:10:00.020 | [2025-04-10 09:10:00,020: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para BALDAZAR, RAUL - 14281172 en 2025-04-10.
celery      | 2025-04-10 09:10:00.024 | [2025-04-10 09:10:00,024: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para BAINOTTI, JORGE - 35669855 en 2025-04-10.
celery      | 2025-04-10 09:10:00.028 | [2025-04-10 09:10:00,027: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para CALDERON, CARLOS - 25040357 en 2025-04-10.
celery      | 2025-04-10 09:10:00.032 | [2025-04-10 09:10:00,032: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para GAUNA, LUCIANO - 29161251 en 2025-04-10.
celery      | 2025-04-10 09:10:00.035 | [2025-04-10 09:10:00,035: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para JARA, RAMIRO - 34965695 en 2025-04-10.
celery      | 2025-04-10 09:10:00.038 | [2025-04-10 09:10:00,038: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para LIOI, VICTOR - 22384294 en 2025-04-10.
celery      | 2025-04-10 09:10:00.041 | [2025-04-10 09:10:00,041: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para PEREZ, NICOLAS - 28757702 en 2025-04-10.
celery      | 2025-04-10 09:10:00.043 | [2025-04-10 09:10:00,043: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para PIAZZA, JORGE - 29884270 en 2025-04-10.
celery      | 2025-04-10 09:10:00.046 | [2025-04-10 09:10:00,045: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para DIAZ, LUCAS - 33920821 en 2025-04-10.
celery      | 2025-04-10 09:10:00.048 | [2025-04-10 09:10:00,048: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para LOPEZ, DANILO - 33349984 en 2025-04-10.
celery      | 2025-04-10 09:10:00.050 | [2025-04-10 09:10:00,050: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para SANTUCHO, MAXIMILIANO - 31731146 en 2025-04-10.
celery      | 2025-04-10 09:10:00.053 | [2025-04-10 09:10:00,052: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para MARTINEZ, CARLOS - 13108031 en 2025-04-10.
celery      | 2025-04-10 09:10:00.055 | [2025-04-10 09:10:00,055: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para VIOLA, HERNÁN MANUEL - 38279671 en 2025-04-10.
celery      | 2025-04-10 09:10:00.057 | [2025-04-10 09:10:00,057: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para DECO, RAFAEL EZEQUIEL - 39022473 en 2025-04-10.
celery      | 2025-04-10 09:10:00.060 | [2025-04-10 09:10:00,060: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para CANTARUTTI, FERNANDO - 37627948 en 2025-04-10.
celery      | 2025-04-10 09:10:00.063 | [2025-04-10 09:10:00,062: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para MATEUCI, SILVINA BELEN - 34965669 en 2025-04-10.
celery      | 2025-04-10 09:10:00.065 | [2025-04-10 09:10:00,065: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para VIDELA, MAURICIO - 27673387 en 2025-04-10.
celery      | 2025-04-10 09:10:00.067 | [2025-04-10 09:10:00,067: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para GOLINELLI, MARTIN - 29519506 en 2025-04-10.
celery      | 2025-04-10 09:10:00.069 | [2025-04-10 09:10:00,069: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para ZABALA, CARLOS F. - 37233007 en 2025-04-10.
celery      | 2025-04-10 09:10:00.072 | [2025-04-10 09:10:00,072: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para PIZARRO, LEANDRO E. - 39610329 en 2025-04-10.
celery      | 2025-04-10 09:10:00.075 | [2025-04-10 09:10:00,074: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para MONTI, CHRISTIAN - 36707055 en 2025-04-10.
celery      | 2025-04-10 09:10:00.077 | [2025-04-10 09:10:00,077: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para MORALES, LUCIANO N. - 36707429 en 2025-04-10.
celery      | 2025-04-10 09:10:00.079 | [2025-04-10 09:10:00,079: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para ROJAS, OSCAR - 62778461 en 2025-04-10.
celery      | 2025-04-10 09:10:00.081 | [2025-04-10 09:10:00,081: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para ALMENARA, LIHUEN ANDRES - 41484063 en 2025-04-10.
celery      | 2025-04-10 09:10:00.084 | [2025-04-10 09:10:00,084: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para FERREYRA, TOMAS - 40026784 en 2025-04-10.
celery      | 2025-04-10 09:10:00.086 | [2025-04-10 09:10:00,086: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para MARIA, GONZALO - 38159134 en 2025-04-10.
celery      | 2025-04-10 09:10:00.088 | [2025-04-10 09:10:00,088: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para AVENDAÑO, DAREL - 40678696 en 2025-04-10.
celery      | 2025-04-10 09:10:00.091 | [2025-04-10 09:10:00,090: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para RODRIGUEZ, GASTON - 37165416 en 2025-04-10.
celery      | 2025-04-10 09:10:00.093 | [2025-04-10 09:10:00,093: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para MATULICH, JOSE - 37850500 en 2025-04-10.
celery      | 2025-04-10 09:10:00.096 | [2025-04-10 09:10:00,095: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para MARUCCO, NOELIA - 32599619 en 2025-04-10.
celery      | 2025-04-10 09:10:00.099 | [2025-04-10 09:10:00,098: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para MOLINERO, JOAQUIN - 41280170 en 2025-04-10.
celery      | 2025-04-10 09:10:00.101 | [2025-04-10 09:10:00,101: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para GOMEZ, FRANCISCO - 41994218 en 2025-04-10.
celery      | 2025-04-10 09:10:00.103 | [2025-04-10 09:10:00,103: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para ALLASIA, DAMIAN - 39824996 en 2025-04-10.
celery      | 2025-04-10 09:10:00.106 | [2025-04-10 09:10:00,106: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para ACEVEDO, JULIETA - 40314005 en 2025-04-10.
celery      | 2025-04-10 09:10:00.108 | [2025-04-10 09:10:00,108: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para MANIAS, LUCAS GABRIEL - 40026647 en 2025-04-10.
celery      | 2025-04-10 09:10:00.111 | [2025-04-10 09:10:00,111: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para LOPEZ, RAYMUNDO - 37232850 en 2025-04-10.
celery      | 2025-04-10 09:10:00.113 | [2025-04-10 09:10:00,113: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para MASSAFARA, BRAIAN - 41888232 en 2025-04-10.
celery      | 2025-04-10 09:10:00.115 | [2025-04-10 09:10:00,115: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para CORONEL, ROMINA - 39176825 en 2025-04-10.
celery      | 2025-04-10 09:10:00.118 | [2025-04-10 09:10:00,118: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para LOMELLO, GONZALO - 30287386 en 2025-04-10.
celery      | 2025-04-10 09:10:00.120 | [2025-04-10 09:10:00,120: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para FERRERI, MILTON - 40299956 en 2025-04-10.
celery      | 2025-04-10 09:10:00.122 | [2025-04-10 09:10:00,122: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para QUINTEROS, BRUNO AGUSTIN - 42696371 en 2025-04-10.
celery      | 2025-04-10 09:10:00.125 | [2025-04-10 09:10:00,125: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para ARNAUD, JERONIMO - 43134653 en 2025-04-10.
celery      | 2025-04-10 09:10:00.127 | [2025-04-10 09:10:00,127: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para BELTRAN, GABRIEL - 38279571 en 2025-04-10.
celery      | 2025-04-10 09:10:00.130 | [2025-04-10 09:10:00,130: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para MARIZZA, JORGE - 40678625 en 2025-04-10.
celery      | 2025-04-10 09:10:00.132 | [2025-04-10 09:10:00,132: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para GIUSTI, JULIO - 41484043 en 2025-04-10.
celery      | 2025-04-10 09:10:00.134 | [2025-04-10 09:10:00,134: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para CABRAL, FACUNDO JULIAN - 43607689 en 2025-04-10.
celery      | 2025-04-10 09:10:00.136 | [2025-04-10 09:10:00,136: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para TESTA, ENZO NICOLAS - 43230436 en 2025-04-10.
celery      | 2025-04-10 09:10:00.139 | [2025-04-10 09:10:00,138: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para FIOL, JORGE LISANDRO - 38279683 en 2025-04-10.
celery      | 2025-04-10 09:10:00.141 | [2025-04-10 09:10:00,141: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para CEBALLOS, FERNANDO - 39610460 en 2025-04-10.
celery      | 2025-04-10 09:10:00.143 | [2025-04-10 09:10:00,143: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para ALBA, GERARDO - 43675993 en 2025-04-10.
celery      | 2025-04-10 09:10:00.145 | [2025-04-10 09:10:00,145: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para DI CROCE, JESSICA - 43015155 en 2025-04-10.
celery      | 2025-04-10 09:10:00.147 | [2025-04-10 09:10:00,147: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para JARA, DIEGO - 28816742 en 2025-04-10.
celery      | 2025-04-10 09:10:00.152 | [2025-04-10 09:10:00,151: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para SAAB, AGUSTIN GABRIEL - 37627901 en 2025-04-10.
celery      | 2025-04-10 09:10:00.155 | [2025-04-10 09:10:00,155: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para ARGUELLO, HUGO FABRICIO - 38279585 en 2025-04-10.
celery      | 2025-04-10 09:10:00.158 | [2025-04-10 09:10:00,158: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para VILLEGAS, EMMANUEL - 36707330 en 2025-04-10.
celery      | 2025-04-10 09:10:00.160 | [2025-04-10 09:10:00,160: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para WYSS, TOBIAS - 45836909 en 2025-04-10.
celery      | 2025-04-10 09:10:00.162 | [2025-04-10 09:10:00,162: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para LAZO, MATIAS - 45352705 en 2025-04-10.
celery      | 2025-04-10 09:10:00.164 | [2025-04-10 09:10:00,164: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para TURRIN, AXEL ARIEL - 38158188 en 2025-04-10.
celery      | 2025-04-10 09:10:00.167 | [2025-04-10 09:10:00,167: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para VILLALBA, RICARDO ALFREDO - 35669686 en 2025-04-10.
celery      | 2025-04-10 09:10:00.169 | [2025-04-10 09:10:00,169: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para RODRIGUEZ, TICIANO - 45836980 en 2025-04-10.
celery      | 2025-04-10 09:10:00.171 | [2025-04-10 09:10:00,171: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para BELTRAN, GERMAN - 39326346 en 2025-04-10.
celery      | 2025-04-10 09:10:00.174 | [2025-04-10 09:10:00,173: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para BAIOCCHI, SANTIAGO NICOLAS - 37232760 en 2025-04-10.
celery      | 2025-04-10 09:10:00.175 | [2025-04-10 09:10:00,175: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para DOMINGUEZ, FERNANDO ARIEL - 24726499 en 2025-04-10.
celery      | 2025-04-10 09:10:00.177 | [2025-04-10 09:10:00,177: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para JARA, DANIEL ELIAS - 38164470 en 2025-04-10.
celery      | 2025-04-10 09:10:00.179 | [2025-04-10 09:10:00,179: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para BURGOS, FACUNDO SEBASTIAN - 41280065 en 2025-04-10.
celery      | 2025-04-10 09:10:00.182 | [2025-04-10 09:10:00,182: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para FUENTES, FRANCISCO LUIS - 44296925 en 2025-04-10.
celery      | 2025-04-10 09:10:00.186 | [2025-04-10 09:10:00,185: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para GIMENEZ, BENJAMIN JOSUE - 45937356 en 2025-04-10.
celery      | 2025-04-10 09:10:00.188 | [2025-04-10 09:10:00,188: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para CROGNALI, LEONARLO DAVID - 44898882 en 2025-04-10.
celery      | 2025-04-10 09:10:00.190 | [2025-04-10 09:10:00,190: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para FUSI, LUCAS ALEJANDRO - 43675844 en 2025-04-10.
celery      | 2025-04-10 09:10:00.192 | [2025-04-10 09:10:00,192: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para GOLINELLI, BLAS - 37232833 en 2025-04-10.
celery      | 2025-04-10 09:10:00.194 | [2025-04-10 09:10:00,194: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para PIERMARINI, FACUNDO FABIAN - 41484145 en 2025-04-10.
celery      | 2025-04-10 09:10:00.197 | [2025-04-10 09:10:00,196: WARNING/ForkPoolWorker-4] Registro de asistencia ya existente para MORANGE, AGUSTIN - 46512137 en 2025-04-10.
celery      | 2025-04-10 09:10:00.198 | [2025-04-10 09:10:00,198: INFO/ForkPoolWorker-4] Task apps.reloj_fichador.tasks.generar_registros_asistencia[be670336-4805-44b4-a85e-7d6d52a86f21] succeeded in 0.18792196099821012s: None

[2025-04-10 09:12:51,791: WARNING/MainProcess] ^


[2025-04-10 09:12:51,791: WARNING/MainProcess] ^


[2025-04-10 09:12:51,791: WARNING/MainProcess] ^


[2025-04-10 09:12:51,791: WARNING/MainProcess] ^


[2025-04-10 09:12:51,791: WARNING/MainProcess] ^


[2025-04-10 09:12:51,791: WARNING/MainProcess] ^


[2025-04-10 09:12:51,791: WARNING/MainProcess] ^


[2025-04-10 09:12:51,791: WARNING/MainProcess] ^


[2025-04-10 09:12:51,791: WARNING/MainProcess] ^


[2025-04-10 09:12:51,791: WARNING/MainProcess] ^


[2025-04-10 09:12:51,791: WARNING/MainProcess] ^


[2025-04-10 09:12:51,791: WARNING/MainProcess] ^


[2025-04-10 09:12:51,791: WARNING/MainProcess] ^


[2025-04-10 09:12:51,791: WARNING/MainProcess] ^


[2025-04-10 09:12:51,791: WARNING/MainProcess] ^


[2025-04-10 09:12:51,791: WARNING/MainProcess] ^


[2025-04-10 09:12:51,791: WARNING/MainProcess] ^


[2025-04-10 09:12:51,791: WARNING/MainProcess] ^


[2025-04-10 09:12:51,791: WARNING/MainProcess] ^


[2025-04-10 09:12:51,791: WARNING/MainProcess] ^


[2025-04-10 09:12:51,791: WARNING/MainProcess] ^


[2025-04-10 09:12:51,791: WARNING/MainProcess] ^


[2025-04-10 09:12:51,791: WARNING/MainProcess] ^


[2025-04-10 09:12:51,791: WARNING/MainProcess] ^


[2025-04-10 09:12:51,791: WARNING/MainProcess] File "/usr/local/lib/python3.11/site-packages/django/db/backends/mysql/operations.py", line 267, in adapt_datetimefield_value


[2025-04-10 09:12:51,791: WARNING/MainProcess]


[2025-04-10 09:12:51,791: WARNING/MainProcess] raise ValueError(


[2025-04-10 09:12:51,791: WARNING/MainProcess] ValueError


[2025-04-10 09:12:51,791: WARNING/MainProcess] :


[2025-04-10 09:12:51,791: WARNING/MainProcess] MySQL backend does not support timezone-aware datetimes when USE_TZ is False.


celery beat v5.4.0 (opalescent) is starting.


__ - ... __ - _


LocalTime -> 2025-04-10 09:09:22


Configuration ->


. broker -> redis://redis:6379/5


. loader -> celery.loaders.app.AppLoader


. scheduler -> django_celery_beat.schedulers.DatabaseScheduler




. logfile -> [stderr]@%INFO


. maxinterval -> 5.00 seconds (5s)


wait-for-it.sh: waiting 15 seconds for db:3306


wait-for-it.sh: db:3306 is available after 0 seconds


Operations to perform:


Apply all migrations: admin, admin_interface, auth, contenttypes, django_celery_beat, django_celery_results, reloj_fichador, sessions


Running migrations:


No migrations to apply.


[2025-04-10 09:12:54,281: INFO/MainProcess] beat: Starting...


[2025-04-10 09:12:54,313: INFO/MainProcess] DatabaseScheduler: Schedule changed.



