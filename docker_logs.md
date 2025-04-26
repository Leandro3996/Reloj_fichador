2025-04-22T15:26:59.833140187Z wait-for-it.sh: waiting 120 seconds for db:3306
2025-04-22T15:26:59.834465073Z wait-for-it.sh: db:3306 is available after 0 seconds
2025-04-22T15:27:00.477811780Z Operations to perform:
2025-04-22T15:27:00.477841506Z   Apply all migrations: admin, admin_interface, auth, contenttypes, django_celery_beat, django_celery_results, reloj_fichador, sessions
2025-04-22T15:27:00.477844454Z Running migrations:
2025-04-22T15:27:00.477846284Z   No migrations to apply.
2025-04-22T15:27:01.120361164Z Found another file with the destination path 'admin/js/cancel.js'. It will be ignored since only the first encountered file is collected. If this is not what you want, make sure every static file has a unique path.
2025-04-22T15:27:01.120379709Z Found another file with the destination path 'admin/js/popup_response.js'. It will be ignored since only the first encountered file is collected. If this is not what you want, make sure every static file has a unique path.
2025-04-22T15:27:01.120382054Z 
2025-04-22T15:27:01.120383534Z 0 static files copied to '/app/staticfiles', 225 unmodified.
2025-04-22T15:27:01.259065344Z [2025-04-22 15:27:01 +0000] [1] [INFO] Starting gunicorn 23.0.0
2025-04-22T15:27:01.259140199Z [2025-04-22 15:27:01 +0000] [1] [INFO] Listening at: http://0.0.0.0:58000 (1)
2025-04-22T15:27:01.259153142Z [2025-04-22 15:27:01 +0000] [1] [INFO] Using worker: sync
2025-04-22T15:27:01.260043663Z [2025-04-22 15:27:01 +0000] [103] [INFO] Booting worker with pid: 103
2025-04-22T15:27:01.302870968Z [2025-04-22 15:27:01 +0000] [104] [INFO] Booting worker with pid: 104
2025-04-22T15:27:01.394103632Z [2025-04-22 15:27:01 +0000] [109] [INFO] Booting worker with pid: 109
2025-04-22T15:51:09.933571327Z WARNING 2025-04-22 12:51:09,933 base Session data corrupted

22T15:51:11.870022560Z /usr/local/lib/python3.11/site-packages/admin_interface/templatetags/admin_interface_tags.py:38: UserWarning: Language chooser requires Django's `set_language` view: `urlpatterns += [url(r'^i18n/', include('django.conf.urls.i18n'))]`.
2025-04-22T15:51:11.870141410Z   warnings.warn(

22T15:51:26.521190755Z /usr/local/lib/python3.11/site-packages/admin_interface/templatetags/admin_interface_tags.py:38: UserWarning: Language chooser requires Django's `set_language` view: `urlpatterns += [url(r'^i18n/', include('django.conf.urls.i18n'))]`.
2025-04-22T15:51:26.521207258Z   warnings.warn(
2025-04-22T15:51:28.652004301Z WARNING 2025-04-22 12:51:28,651 log Not Found: /favicon.ico

22T15:51:59.709899887Z /usr/local/lib/python3.11/site-packages/admin_interface/templatetags/admin_interface_tags.py:38: UserWarning: Language chooser requires Django's `set_language` view: `urlpatterns += [url(r'^i18n/', include('django.conf.urls.i18n'))]`.
2025-04-22T15:51:59.709923930Z   warnings.warn(
2025-04-22T15:52:08.796279890Z WARNING 2025-04-22 12:52:08,796 log Not Found: /favicon.ico
2025-04-22T15:52:49.293681644Z WARNING 2025-04-22 12:52:49,293 log Not Found: /favicon.ico
2025-04-22T15:53:09.408101746Z WARNING 2025-04-22 12:53:09,407 log Not Found: /favicon.ico
2025-04-22T15:53:33.831489462Z WARNING 2025-04-22 12:53:33,831 log Not Found: /favicon.ico
2025-04-22T15:54:59.865274939Z WARNING 2025-04-22 12:54:59,865 log Not Found: /favicon.ico
2025-04-22T16:10:32.327419068Z ERROR 2025-04-22 13:10:32,326 exception Invalid HTTP_HOST header: 'relojfichador.com:5080'. You may need to add 'relojfichador.com' to ALLOWED_HOSTS.
2025-04-22T16:10:32.327438080Z Traceback (most recent call last):
2025-04-22T16:10:32.327441063Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 55, in inner
2025-04-22T16:10:32.327443469Z     response = get_response(request)
2025-04-22T16:10:32.327445451Z                ^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.327447501Z   File "/usr/local/lib/python3.11/site-packages/django/utils/deprecation.py", line 128, in __call__
2025-04-22T16:10:32.327449583Z     response = self.process_request(request)
2025-04-22T16:10:32.327451552Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.327453512Z   File "/usr/local/lib/python3.11/site-packages/django/middleware/common.py", line 48, in process_request
2025-04-22T16:10:32.327456879Z     host = request.get_host()
2025-04-22T16:10:32.327458921Z            ^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.327460888Z   File "/usr/local/lib/python3.11/site-packages/django/http/request.py", line 151, in get_host
2025-04-22T16:10:32.327463041Z     raise DisallowedHost(msg)
2025-04-22T16:10:32.327464982Z django.core.exceptions.DisallowedHost: Invalid HTTP_HOST header: 'relojfichador.com:5080'. You may need to add 'relojfichador.com' to ALLOWED_HOSTS.
2025-04-22T16:10:32.328407289Z [2025-04-22 13:10:32 -0300] [103] [ERROR] Error handling request /
2025-04-22T16:10:32.328421358Z Traceback (most recent call last):
2025-04-22T16:10:32.328423980Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 55, in inner
2025-04-22T16:10:32.328426231Z     response = get_response(request)
2025-04-22T16:10:32.328428086Z                ^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.328429936Z   File "/usr/local/lib/python3.11/site-packages/django/utils/deprecation.py", line 128, in __call__
2025-04-22T16:10:32.328431833Z     response = self.process_request(request)
2025-04-22T16:10:32.328433879Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.328435728Z   File "/usr/local/lib/python3.11/site-packages/django/middleware/common.py", line 48, in process_request
2025-04-22T16:10:32.328437674Z     host = request.get_host()
2025-04-22T16:10:32.328439385Z            ^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.328441119Z   File "/usr/local/lib/python3.11/site-packages/django/http/request.py", line 151, in get_host
2025-04-22T16:10:32.328443041Z     raise DisallowedHost(msg)
2025-04-22T16:10:32.328444837Z django.core.exceptions.DisallowedHost: Invalid HTTP_HOST header: 'relojfichador.com:5080'. You may need to add 'relojfichador.com' to ALLOWED_HOSTS.
2025-04-22T16:10:32.328453773Z 
2025-04-22T16:10:32.328455991Z During handling of the above exception, another exception occurred:
2025-04-22T16:10:32.328457885Z 
2025-04-22T16:10:32.328459599Z Traceback (most recent call last):
2025-04-22T16:10:32.328461329Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 164, in get_exception_response
2025-04-22T16:10:32.328463211Z     response = callback(request, exception=exception)
2025-04-22T16:10:32.328464982Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.328466723Z   File "/app/apps/reloj_fichador/views.py", line 148, in error_400
2025-04-22T16:10:32.328468550Z     'user': request.user,
2025-04-22T16:10:32.328470294Z             ^^^^^^^^^^^^
2025-04-22T16:10:32.328471993Z AttributeError: 'WSGIRequest' object has no attribute 'user'
2025-04-22T16:10:32.328473722Z 
2025-04-22T16:10:32.328475369Z During handling of the above exception, another exception occurred:
2025-04-22T16:10:32.328477084Z 
2025-04-22T16:10:32.328478705Z Traceback (most recent call last):
2025-04-22T16:10:32.328480404Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 55, in inner
2025-04-22T16:10:32.328482237Z     response = get_response(request)
2025-04-22T16:10:32.328484003Z                ^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.328485760Z   File "/usr/local/lib/python3.11/site-packages/django/utils/deprecation.py", line 129, in __call__
2025-04-22T16:10:32.328487582Z     response = response or self.get_response(request)
2025-04-22T16:10:32.328489284Z                            ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.328490996Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 57, in inner
2025-04-22T16:10:32.328493530Z     response = response_for_exception(request, exc)
2025-04-22T16:10:32.328495353Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.328497149Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 134, in response_for_exception
2025-04-22T16:10:32.328499020Z     response = get_exception_response(
2025-04-22T16:10:32.328500728Z                ^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.328502428Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 167, in get_exception_response
2025-04-22T16:10:32.328504292Z     response = handle_uncaught_exception(request, resolver, sys.exc_info())
2025-04-22T16:10:32.328506083Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.328507882Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 185, in handle_uncaught_exception
2025-04-22T16:10:32.328509739Z     return callback(request)
2025-04-22T16:10:32.328513936Z            ^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.328515916Z   File "/app/apps/reloj_fichador/views.py", line 178, in error_500
2025-04-22T16:10:32.328517798Z     'user': request.user,
2025-04-22T16:10:32.328519505Z             ^^^^^^^^^^^^
2025-04-22T16:10:32.328521215Z AttributeError: 'WSGIRequest' object has no attribute 'user'
2025-04-22T16:10:32.328523164Z 
2025-04-22T16:10:32.328524841Z During handling of the above exception, another exception occurred:
2025-04-22T16:10:32.328526548Z 
2025-04-22T16:10:32.328528168Z Traceback (most recent call last):
2025-04-22T16:10:32.328529918Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 55, in inner
2025-04-22T16:10:32.328531752Z     response = get_response(request)
2025-04-22T16:10:32.328533428Z                ^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.328535102Z   File "/usr/local/lib/python3.11/site-packages/django/utils/deprecation.py", line 129, in __call__
2025-04-22T16:10:32.328536865Z     response = response or self.get_response(request)
2025-04-22T16:10:32.328538514Z                            ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.328540175Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 57, in inner
2025-04-22T16:10:32.328541925Z     response = response_for_exception(request, exc)
2025-04-22T16:10:32.328543601Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.328545339Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 140, in response_for_exception
2025-04-22T16:10:32.328547144Z     response = handle_uncaught_exception(
2025-04-22T16:10:32.328548862Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.328550566Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 185, in handle_uncaught_exception
2025-04-22T16:10:32.328552438Z     return callback(request)
2025-04-22T16:10:32.328554374Z            ^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.328556158Z   File "/app/apps/reloj_fichador/views.py", line 178, in error_500
2025-04-22T16:10:32.328558356Z     'user': request.user,
2025-04-22T16:10:32.328560274Z             ^^^^^^^^^^^^
2025-04-22T16:10:32.328561981Z AttributeError: 'WSGIRequest' object has no attribute 'user'
2025-04-22T16:10:32.328564045Z 
2025-04-22T16:10:32.328565785Z During handling of the above exception, another exception occurred:
2025-04-22T16:10:32.328568665Z 
2025-04-22T16:10:32.328570946Z Traceback (most recent call last):
2025-04-22T16:10:32.328572758Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 55, in inner
2025-04-22T16:10:32.328574628Z     response = get_response(request)
2025-04-22T16:10:32.328578767Z                ^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.328580771Z   File "/usr/local/lib/python3.11/site-packages/django/utils/deprecation.py", line 129, in __call__
2025-04-22T16:10:32.328582748Z     response = response or self.get_response(request)
2025-04-22T16:10:32.328584508Z                            ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.328586269Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 57, in inner
2025-04-22T16:10:32.328588084Z     response = response_for_exception(request, exc)
2025-04-22T16:10:32.328589811Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.328591575Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 140, in response_for_exception
2025-04-22T16:10:32.328593393Z     response = handle_uncaught_exception(
2025-04-22T16:10:32.328595096Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.328596817Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 185, in handle_uncaught_exception
2025-04-22T16:10:32.328598639Z     return callback(request)
2025-04-22T16:10:32.328600342Z            ^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.328602035Z   File "/app/apps/reloj_fichador/views.py", line 178, in error_500
2025-04-22T16:10:32.328604012Z     'user': request.user,
2025-04-22T16:10:32.328605900Z             ^^^^^^^^^^^^
2025-04-22T16:10:32.328607798Z AttributeError: 'WSGIRequest' object has no attribute 'user'
2025-04-22T16:10:32.328609708Z 
2025-04-22T16:10:32.328611528Z During handling of the above exception, another exception occurred:
2025-04-22T16:10:32.328613425Z 
2025-04-22T16:10:32.328615247Z Traceback (most recent call last):
2025-04-22T16:10:32.328617131Z   File "/usr/local/lib/python3.11/site-packages/gunicorn/workers/sync.py", line 134, in handle
2025-04-22T16:10:32.328619133Z     self.handle_request(listener, req, client, addr)
2025-04-22T16:10:32.328621056Z   File "/usr/local/lib/python3.11/site-packages/gunicorn/workers/sync.py", line 177, in handle_request
2025-04-22T16:10:32.328623083Z     respiter = self.wsgi(environ, resp.start_response)
2025-04-22T16:10:32.328624988Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.328626895Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/wsgi.py", line 124, in __call__
2025-04-22T16:10:32.328628888Z     response = self.get_response(request)
2025-04-22T16:10:32.328630768Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.328633042Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/base.py", line 140, in get_response
2025-04-22T16:10:32.328635239Z     response = self._middleware_chain(request)
2025-04-22T16:10:32.328639006Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.328641049Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 57, in inner
2025-04-22T16:10:32.328643038Z     response = response_for_exception(request, exc)
2025-04-22T16:10:32.328644965Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.328646856Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 140, in response_for_exception
2025-04-22T16:10:32.328648866Z     response = handle_uncaught_exception(
2025-04-22T16:10:32.328650733Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.328652626Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 185, in handle_uncaught_exception
2025-04-22T16:10:32.328654673Z     return callback(request)
2025-04-22T16:10:32.328656540Z            ^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.328658403Z   File "/app/apps/reloj_fichador/views.py", line 178, in error_500
2025-04-22T16:10:32.328660369Z     'user': request.user,
2025-04-22T16:10:32.328662202Z             ^^^^^^^^^^^^
2025-04-22T16:10:32.328664061Z AttributeError: 'WSGIRequest' object has no attribute 'user'
2025-04-22T16:10:32.361046564Z ERROR 2025-04-22 13:10:32,360 exception Invalid HTTP_HOST header: 'relojfichador.com:5080'. You may need to add 'relojfichador.com' to ALLOWED_HOSTS.
2025-04-22T16:10:32.361057275Z Traceback (most recent call last):
2025-04-22T16:10:32.361059915Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 55, in inner
2025-04-22T16:10:32.361062199Z     response = get_response(request)
2025-04-22T16:10:32.361064053Z                ^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.361065809Z   File "/usr/local/lib/python3.11/site-packages/django/utils/deprecation.py", line 128, in __call__
2025-04-22T16:10:32.361067721Z     response = self.process_request(request)
2025-04-22T16:10:32.361069455Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.361071205Z   File "/usr/local/lib/python3.11/site-packages/django/middleware/common.py", line 48, in process_request
2025-04-22T16:10:32.361073289Z     host = request.get_host()
2025-04-22T16:10:32.361075218Z            ^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.361077106Z   File "/usr/local/lib/python3.11/site-packages/django/http/request.py", line 151, in get_host
2025-04-22T16:10:32.361079118Z     raise DisallowedHost(msg)
2025-04-22T16:10:32.361080993Z django.core.exceptions.DisallowedHost: Invalid HTTP_HOST header: 'relojfichador.com:5080'. You may need to add 'relojfichador.com' to ALLOWED_HOSTS.
2025-04-22T16:10:32.361755847Z [2025-04-22 13:10:32 -0300] [103] [ERROR] Error handling request /favicon.ico
2025-04-22T16:10:32.361765984Z Traceback (most recent call last):
2025-04-22T16:10:32.361768898Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 55, in inner
2025-04-22T16:10:32.361779112Z     response = get_response(request)
2025-04-22T16:10:32.361781495Z                ^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.361783513Z   File "/usr/local/lib/python3.11/site-packages/django/utils/deprecation.py", line 128, in __call__
2025-04-22T16:10:32.361785613Z     response = self.process_request(request)
2025-04-22T16:10:32.361787505Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.361789501Z   File "/usr/local/lib/python3.11/site-packages/django/middleware/common.py", line 48, in process_request
2025-04-22T16:10:32.361791526Z     host = request.get_host()
2025-04-22T16:10:32.361793428Z            ^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.361795330Z   File "/usr/local/lib/python3.11/site-packages/django/http/request.py", line 151, in get_host
2025-04-22T16:10:32.361797516Z     raise DisallowedHost(msg)
2025-04-22T16:10:32.361799492Z django.core.exceptions.DisallowedHost: Invalid HTTP_HOST header: 'relojfichador.com:5080'. You may need to add 'relojfichador.com' to ALLOWED_HOSTS.
2025-04-22T16:10:32.361801712Z 
2025-04-22T16:10:32.361803579Z During handling of the above exception, another exception occurred:
2025-04-22T16:10:32.361805530Z 
2025-04-22T16:10:32.361807386Z Traceback (most recent call last):
2025-04-22T16:10:32.361809286Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 164, in get_exception_response
2025-04-22T16:10:32.361811340Z     response = callback(request, exception=exception)
2025-04-22T16:10:32.361813278Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.361815180Z   File "/app/apps/reloj_fichador/views.py", line 148, in error_400
2025-04-22T16:10:32.361817183Z     'user': request.user,
2025-04-22T16:10:32.361819039Z             ^^^^^^^^^^^^
2025-04-22T16:10:32.361820913Z AttributeError: 'WSGIRequest' object has no attribute 'user'
2025-04-22T16:10:32.361822815Z 
2025-04-22T16:10:32.361824675Z During handling of the above exception, another exception occurred:
2025-04-22T16:10:32.361826631Z 
2025-04-22T16:10:32.361828440Z Traceback (most recent call last):
2025-04-22T16:10:32.361830329Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 55, in inner
2025-04-22T16:10:32.361832324Z     response = get_response(request)
2025-04-22T16:10:32.361834185Z                ^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.361836092Z   File "/usr/local/lib/python3.11/site-packages/django/utils/deprecation.py", line 129, in __call__
2025-04-22T16:10:32.361838098Z     response = response or self.get_response(request)
2025-04-22T16:10:32.361840039Z                            ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.361841950Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 57, in inner
2025-04-22T16:10:32.361847719Z     response = response_for_exception(request, exc)
2025-04-22T16:10:32.361849945Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.361853117Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 134, in response_for_exception
2025-04-22T16:10:32.361855263Z     response = get_exception_response(
2025-04-22T16:10:32.361857177Z                ^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.361859071Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 167, in get_exception_response
2025-04-22T16:10:32.361861140Z     response = handle_uncaught_exception(request, resolver, sys.exc_info())
2025-04-22T16:10:32.361863143Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.361865097Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 185, in handle_uncaught_exception
2025-04-22T16:10:32.361867144Z     return callback(request)
2025-04-22T16:10:32.361869036Z            ^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.361870885Z   File "/app/apps/reloj_fichador/views.py", line 178, in error_500
2025-04-22T16:10:32.361872849Z     'user': request.user,
2025-04-22T16:10:32.361874687Z             ^^^^^^^^^^^^
2025-04-22T16:10:32.361876555Z AttributeError: 'WSGIRequest' object has no attribute 'user'
2025-04-22T16:10:32.361878464Z 
2025-04-22T16:10:32.361880269Z During handling of the above exception, another exception occurred:
2025-04-22T16:10:32.361882190Z 
2025-04-22T16:10:32.361884009Z Traceback (most recent call last):
2025-04-22T16:10:32.361885865Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 55, in inner
2025-04-22T16:10:32.361887857Z     response = get_response(request)
2025-04-22T16:10:32.361889737Z                ^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.361891652Z   File "/usr/local/lib/python3.11/site-packages/django/utils/deprecation.py", line 129, in __call__
2025-04-22T16:10:32.361893639Z     response = response or self.get_response(request)
2025-04-22T16:10:32.361895525Z                            ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.361897435Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 57, in inner
2025-04-22T16:10:32.361899415Z     response = response_for_exception(request, exc)
2025-04-22T16:10:32.361901306Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.361903213Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 140, in response_for_exception
2025-04-22T16:10:32.361905207Z     response = handle_uncaught_exception(
2025-04-22T16:10:32.361907090Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.361911430Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 185, in handle_uncaught_exception
2025-04-22T16:10:32.361913633Z     return callback(request)
2025-04-22T16:10:32.361915516Z            ^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.361917670Z   File "/app/apps/reloj_fichador/views.py", line 178, in error_500
2025-04-22T16:10:32.361919721Z     'user': request.user,
2025-04-22T16:10:32.361921622Z             ^^^^^^^^^^^^
2025-04-22T16:10:32.361923526Z AttributeError: 'WSGIRequest' object has no attribute 'user'
2025-04-22T16:10:32.361925542Z 
2025-04-22T16:10:32.361927371Z During handling of the above exception, another exception occurred:
2025-04-22T16:10:32.361929336Z 
2025-04-22T16:10:32.361931143Z Traceback (most recent call last):
2025-04-22T16:10:32.361933060Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 55, in inner
2025-04-22T16:10:32.361935032Z     response = get_response(request)
2025-04-22T16:10:32.361936922Z                ^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.361938781Z   File "/usr/local/lib/python3.11/site-packages/django/utils/deprecation.py", line 129, in __call__
2025-04-22T16:10:32.361941059Z     response = response or self.get_response(request)
2025-04-22T16:10:32.361943113Z                            ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.361945069Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 57, in inner
2025-04-22T16:10:32.361947123Z     response = response_for_exception(request, exc)
2025-04-22T16:10:32.361949023Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.361950914Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 140, in response_for_exception
2025-04-22T16:10:32.361952929Z     response = handle_uncaught_exception(
2025-04-22T16:10:32.361954874Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.361956778Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 185, in handle_uncaught_exception
2025-04-22T16:10:32.361958875Z     return callback(request)
2025-04-22T16:10:32.361960750Z            ^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.361962611Z   File "/app/apps/reloj_fichador/views.py", line 178, in error_500
2025-04-22T16:10:32.361964657Z     'user': request.user,
2025-04-22T16:10:32.361966546Z             ^^^^^^^^^^^^
2025-04-22T16:10:32.361968517Z AttributeError: 'WSGIRequest' object has no attribute 'user'
2025-04-22T16:10:32.361970455Z 
2025-04-22T16:10:32.361972331Z During handling of the above exception, another exception occurred:
2025-04-22T16:10:32.361974235Z 
2025-04-22T16:10:32.361975995Z Traceback (most recent call last):
2025-04-22T16:10:32.362035151Z   File "/usr/local/lib/python3.11/site-packages/gunicorn/workers/sync.py", line 134, in handle
2025-04-22T16:10:32.362037643Z     self.handle_request(listener, req, client, addr)
2025-04-22T16:10:32.362039628Z   File "/usr/local/lib/python3.11/site-packages/gunicorn/workers/sync.py", line 177, in handle_request
2025-04-22T16:10:32.362041687Z     respiter = self.wsgi(environ, resp.start_response)
2025-04-22T16:10:32.362044108Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.362046074Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/wsgi.py", line 124, in __call__
2025-04-22T16:10:32.362048085Z     response = self.get_response(request)
2025-04-22T16:10:32.362050002Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.362052277Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/base.py", line 140, in get_response
2025-04-22T16:10:32.362054373Z     response = self._middleware_chain(request)
2025-04-22T16:10:32.362056238Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.362058165Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 57, in inner
2025-04-22T16:10:32.362060160Z     response = response_for_exception(request, exc)
2025-04-22T16:10:32.362062132Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.362064034Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 140, in response_for_exception
2025-04-22T16:10:32.362066058Z     response = handle_uncaught_exception(
2025-04-22T16:10:32.362067910Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.362069808Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 185, in handle_uncaught_exception
2025-04-22T16:10:32.362071820Z     return callback(request)
2025-04-22T16:10:32.362073667Z            ^^^^^^^^^^^^^^^^^
2025-04-22T16:10:32.362075518Z   File "/app/apps/reloj_fichador/views.py", line 178, in error_500
2025-04-22T16:10:32.362077499Z     'user': request.user,
2025-04-22T16:10:32.362079374Z             ^^^^^^^^^^^^
2025-04-22T16:10:32.362081241Z AttributeError: 'WSGIRequest' object has no attribute 'user'
2025-04-22T16:25:35.270268712Z ERROR 2025-04-22 13:25:35,269 exception Invalid HTTP_HOST header: 'relojfichador.com:5080'. You may need to add 'relojfichador.com' to ALLOWED_HOSTS.
2025-04-22T16:25:35.270282595Z Traceback (most recent call last):
2025-04-22T16:25:35.270283911Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 55, in inner
2025-04-22T16:25:35.270285029Z     response = get_response(request)
2025-04-22T16:25:35.270286036Z                ^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.270286934Z   File "/usr/local/lib/python3.11/site-packages/django/utils/deprecation.py", line 128, in __call__
2025-04-22T16:25:35.270295461Z     response = self.process_request(request)
2025-04-22T16:25:35.270296381Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.270297255Z   File "/usr/local/lib/python3.11/site-packages/django/middleware/common.py", line 48, in process_request
2025-04-22T16:25:35.270298213Z     host = request.get_host()
2025-04-22T16:25:35.270300171Z            ^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.270301076Z   File "/usr/local/lib/python3.11/site-packages/django/http/request.py", line 151, in get_host
2025-04-22T16:25:35.270302109Z     raise DisallowedHost(msg)
2025-04-22T16:25:35.270303054Z django.core.exceptions.DisallowedHost: Invalid HTTP_HOST header: 'relojfichador.com:5080'. You may need to add 'relojfichador.com' to ALLOWED_HOSTS.
2025-04-22T16:25:35.271105143Z [2025-04-22 13:25:35 -0300] [103] [ERROR] Error handling request /
2025-04-22T16:25:35.271114144Z Traceback (most recent call last):
2025-04-22T16:25:35.271116980Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 55, in inner
2025-04-22T16:25:35.271119273Z     response = get_response(request)
2025-04-22T16:25:35.271121079Z                ^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.271122891Z   File "/usr/local/lib/python3.11/site-packages/django/utils/deprecation.py", line 128, in __call__
2025-04-22T16:25:35.271124839Z     response = self.process_request(request)
2025-04-22T16:25:35.271126648Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.271128402Z   File "/usr/local/lib/python3.11/site-packages/django/middleware/common.py", line 48, in process_request
2025-04-22T16:25:35.271130302Z     host = request.get_host()
2025-04-22T16:25:35.271132006Z            ^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.271133702Z   File "/usr/local/lib/python3.11/site-packages/django/http/request.py", line 151, in get_host
2025-04-22T16:25:35.271135548Z     raise DisallowedHost(msg)
2025-04-22T16:25:35.271137468Z django.core.exceptions.DisallowedHost: Invalid HTTP_HOST header: 'relojfichador.com:5080'. You may need to add 'relojfichador.com' to ALLOWED_HOSTS.
2025-04-22T16:25:35.271139568Z 
2025-04-22T16:25:35.271152876Z During handling of the above exception, another exception occurred:
2025-04-22T16:25:35.271154627Z 
2025-04-22T16:25:35.271156290Z Traceback (most recent call last):
2025-04-22T16:25:35.271158048Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 164, in get_exception_response
2025-04-22T16:25:35.271159941Z     response = callback(request, exception=exception)
2025-04-22T16:25:35.271161625Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.271163372Z   File "/app/apps/reloj_fichador/views.py", line 148, in error_400
2025-04-22T16:25:35.271165137Z     'user': request.user,
2025-04-22T16:25:35.271171619Z             ^^^^^^^^^^^^
2025-04-22T16:25:35.271173777Z AttributeError: 'WSGIRequest' object has no attribute 'user'
2025-04-22T16:25:35.271175567Z 
2025-04-22T16:25:35.271177210Z During handling of the above exception, another exception occurred:
2025-04-22T16:25:35.271178998Z 
2025-04-22T16:25:35.271180597Z Traceback (most recent call last):
2025-04-22T16:25:35.271182318Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 55, in inner
2025-04-22T16:25:35.271184213Z     response = get_response(request)
2025-04-22T16:25:35.271185932Z                ^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.271187629Z   File "/usr/local/lib/python3.11/site-packages/django/utils/deprecation.py", line 129, in __call__
2025-04-22T16:25:35.271189447Z     response = response or self.get_response(request)
2025-04-22T16:25:35.271191127Z                            ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.271192825Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 57, in inner
2025-04-22T16:25:35.271194995Z     response = response_for_exception(request, exc)
2025-04-22T16:25:35.271196884Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.271198615Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 134, in response_for_exception
2025-04-22T16:25:35.271200469Z     response = get_exception_response(
2025-04-22T16:25:35.271202144Z                ^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.271203853Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 167, in get_exception_response
2025-04-22T16:25:35.271205702Z     response = handle_uncaught_exception(request, resolver, sys.exc_info())
2025-04-22T16:25:35.271207523Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.271209307Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 185, in handle_uncaught_exception
2025-04-22T16:25:35.271211215Z     return callback(request)
2025-04-22T16:25:35.271212898Z            ^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.271214593Z   File "/app/apps/reloj_fichador/views.py", line 178, in error_500
2025-04-22T16:25:35.271216378Z     'user': request.user,
2025-04-22T16:25:35.271218088Z             ^^^^^^^^^^^^
2025-04-22T16:25:35.271219780Z AttributeError: 'WSGIRequest' object has no attribute 'user'
2025-04-22T16:25:35.271221519Z 
2025-04-22T16:25:35.271223178Z During handling of the above exception, another exception occurred:
2025-04-22T16:25:35.271225005Z 
2025-04-22T16:25:35.271226664Z Traceback (most recent call last):
2025-04-22T16:25:35.271228376Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 55, in inner
2025-04-22T16:25:35.271232714Z     response = get_response(request)
2025-04-22T16:25:35.271234676Z                ^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.271236429Z   File "/usr/local/lib/python3.11/site-packages/django/utils/deprecation.py", line 129, in __call__
2025-04-22T16:25:35.271238247Z     response = response or self.get_response(request)
2025-04-22T16:25:35.271239973Z                            ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.271241783Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 57, in inner
2025-04-22T16:25:35.271243587Z     response = response_for_exception(request, exc)
2025-04-22T16:25:35.271245317Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.271247056Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 140, in response_for_exception
2025-04-22T16:25:35.271248902Z     response = handle_uncaught_exception(
2025-04-22T16:25:35.271250604Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.271252354Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 185, in handle_uncaught_exception
2025-04-22T16:25:35.271254200Z     return callback(request)
2025-04-22T16:25:35.271255986Z            ^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.271257737Z   File "/app/apps/reloj_fichador/views.py", line 178, in error_500
2025-04-22T16:25:35.271259776Z     'user': request.user,
2025-04-22T16:25:35.271261596Z             ^^^^^^^^^^^^
2025-04-22T16:25:35.271263386Z AttributeError: 'WSGIRequest' object has no attribute 'user'
2025-04-22T16:25:35.271265225Z 
2025-04-22T16:25:35.271266988Z During handling of the above exception, another exception occurred:
2025-04-22T16:25:35.271268829Z 
2025-04-22T16:25:35.271270467Z Traceback (most recent call last):
2025-04-22T16:25:35.271272177Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 55, in inner
2025-04-22T16:25:35.271274024Z     response = get_response(request)
2025-04-22T16:25:35.271275729Z                ^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.271277482Z   File "/usr/local/lib/python3.11/site-packages/django/utils/deprecation.py", line 129, in __call__
2025-04-22T16:25:35.271279305Z     response = response or self.get_response(request)
2025-04-22T16:25:35.271281046Z                            ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.271282768Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 57, in inner
2025-04-22T16:25:35.271284619Z     response = response_for_exception(request, exc)
2025-04-22T16:25:35.271286353Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.271288110Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 140, in response_for_exception
2025-04-22T16:25:35.271291945Z     response = handle_uncaught_exception(
2025-04-22T16:25:35.271293811Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.271295552Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 185, in handle_uncaught_exception
2025-04-22T16:25:35.271297487Z     return callback(request)
2025-04-22T16:25:35.271299810Z            ^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.271301746Z   File "/app/apps/reloj_fichador/views.py", line 178, in error_500
2025-04-22T16:25:35.271303607Z     'user': request.user,
2025-04-22T16:25:35.271305372Z             ^^^^^^^^^^^^
2025-04-22T16:25:35.271307108Z AttributeError: 'WSGIRequest' object has no attribute 'user'
2025-04-22T16:25:35.271308882Z 
2025-04-22T16:25:35.271310557Z During handling of the above exception, another exception occurred:
2025-04-22T16:25:35.271312289Z 
2025-04-22T16:25:35.271313876Z Traceback (most recent call last):
2025-04-22T16:25:35.271315586Z   File "/usr/local/lib/python3.11/site-packages/gunicorn/workers/sync.py", line 134, in handle
2025-04-22T16:25:35.271317404Z     self.handle_request(listener, req, client, addr)
2025-04-22T16:25:35.271319258Z   File "/usr/local/lib/python3.11/site-packages/gunicorn/workers/sync.py", line 177, in handle_request
2025-04-22T16:25:35.271321107Z     respiter = self.wsgi(environ, resp.start_response)
2025-04-22T16:25:35.271322852Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.271324599Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/wsgi.py", line 124, in __call__
2025-04-22T16:25:35.271326485Z     response = self.get_response(request)
2025-04-22T16:25:35.271328177Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.271330239Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/base.py", line 140, in get_response
2025-04-22T16:25:35.271332220Z     response = self._middleware_chain(request)
2025-04-22T16:25:35.271333971Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.271335716Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 57, in inner
2025-04-22T16:25:35.271337571Z     response = response_for_exception(request, exc)
2025-04-22T16:25:35.271339453Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.271341269Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 140, in response_for_exception
2025-04-22T16:25:35.271343162Z     response = handle_uncaught_exception(
2025-04-22T16:25:35.271344967Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.271346713Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 185, in handle_uncaught_exception
2025-04-22T16:25:35.271350522Z     return callback(request)
2025-04-22T16:25:35.271352535Z            ^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.271354462Z   File "/app/apps/reloj_fichador/views.py", line 178, in error_500
2025-04-22T16:25:35.271356431Z     'user': request.user,
2025-04-22T16:25:35.271358350Z             ^^^^^^^^^^^^
2025-04-22T16:25:35.271360200Z AttributeError: 'WSGIRequest' object has no attribute 'user'
2025-04-22T16:25:35.566540338Z ERROR 2025-04-22 13:25:35,566 exception Invalid HTTP_HOST header: 'relojfichador.com:5080'. You may need to add 'relojfichador.com' to ALLOWED_HOSTS.
2025-04-22T16:25:35.566552157Z Traceback (most recent call last):
2025-04-22T16:25:35.566553451Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 55, in inner
2025-04-22T16:25:35.566554669Z     response = get_response(request)
2025-04-22T16:25:35.566555710Z                ^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.566556949Z   File "/usr/local/lib/python3.11/site-packages/django/utils/deprecation.py", line 128, in __call__
2025-04-22T16:25:35.566558000Z     response = self.process_request(request)
2025-04-22T16:25:35.566559205Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.566560166Z   File "/usr/local/lib/python3.11/site-packages/django/middleware/common.py", line 48, in process_request
2025-04-22T16:25:35.566561186Z     host = request.get_host()
2025-04-22T16:25:35.566562117Z            ^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.566563092Z   File "/usr/local/lib/python3.11/site-packages/django/http/request.py", line 151, in get_host
2025-04-22T16:25:35.566564123Z     raise DisallowedHost(msg)
2025-04-22T16:25:35.566565053Z django.core.exceptions.DisallowedHost: Invalid HTTP_HOST header: 'relojfichador.com:5080'. You may need to add 'relojfichador.com' to ALLOWED_HOSTS.
2025-04-22T16:25:35.567679469Z [2025-04-22 13:25:35 -0300] [104] [ERROR] Error handling request /favicon.ico
2025-04-22T16:25:35.567681367Z Traceback (most recent call last):
2025-04-22T16:25:35.567682294Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 55, in inner
2025-04-22T16:25:35.567683329Z     response = get_response(request)
2025-04-22T16:25:35.567684293Z                ^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.567685257Z   File "/usr/local/lib/python3.11/site-packages/django/utils/deprecation.py", line 128, in __call__
2025-04-22T16:25:35.567686288Z     response = self.process_request(request)
2025-04-22T16:25:35.567687303Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.567688296Z   File "/usr/local/lib/python3.11/site-packages/django/middleware/common.py", line 48, in process_request
2025-04-22T16:25:35.567689328Z     host = request.get_host()
2025-04-22T16:25:35.567690247Z            ^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.567691173Z   File "/usr/local/lib/python3.11/site-packages/django/http/request.py", line 151, in get_host
2025-04-22T16:25:35.567697329Z     raise DisallowedHost(msg)
2025-04-22T16:25:35.567698305Z django.core.exceptions.DisallowedHost: Invalid HTTP_HOST header: 'relojfichador.com:5080'. You may need to add 'relojfichador.com' to ALLOWED_HOSTS.
2025-04-22T16:25:35.567699349Z 
2025-04-22T16:25:35.567700251Z During handling of the above exception, another exception occurred:
2025-04-22T16:25:35.567701307Z 
2025-04-22T16:25:35.567702174Z Traceback (most recent call last):
2025-04-22T16:25:35.567703100Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 164, in get_exception_response
2025-04-22T16:25:35.567704169Z     response = callback(request, exception=exception)
2025-04-22T16:25:35.567705283Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.567706239Z   File "/app/apps/reloj_fichador/views.py", line 148, in error_400
2025-04-22T16:25:35.567707283Z     'user': request.user,
2025-04-22T16:25:35.567708333Z             ^^^^^^^^^^^^
2025-04-22T16:25:35.567709343Z AttributeError: 'WSGIRequest' object has no attribute 'user'
2025-04-22T16:25:35.567710375Z 
2025-04-22T16:25:35.567711243Z During handling of the above exception, another exception occurred:
2025-04-22T16:25:35.567712270Z 
2025-04-22T16:25:35.567713158Z Traceback (most recent call last):
2025-04-22T16:25:35.567714114Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 55, in inner
2025-04-22T16:25:35.567715145Z     response = get_response(request)
2025-04-22T16:25:35.567716081Z                ^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.567716997Z   File "/usr/local/lib/python3.11/site-packages/django/utils/deprecation.py", line 129, in __call__
2025-04-22T16:25:35.567718004Z     response = response or self.get_response(request)
2025-04-22T16:25:35.567718959Z                            ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.567719900Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 57, in inner
2025-04-22T16:25:35.567721069Z     response = response_for_exception(request, exc)
2025-04-22T16:25:35.567722021Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.567722968Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 134, in response_for_exception
2025-04-22T16:25:35.567724016Z     response = get_exception_response(
2025-04-22T16:25:35.567724965Z                ^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.567725922Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 167, in get_exception_response
2025-04-22T16:25:35.567726956Z     response = handle_uncaught_exception(request, resolver, sys.exc_info())
2025-04-22T16:25:35.567729033Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.567730033Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 185, in handle_uncaught_exception
2025-04-22T16:25:35.567731056Z     return callback(request)
2025-04-22T16:25:35.567731972Z            ^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.567732875Z   File "/app/apps/reloj_fichador/views.py", line 178, in error_500
2025-04-22T16:25:35.567738244Z     'user': request.user,
2025-04-22T16:25:35.567739137Z             ^^^^^^^^^^^^
2025-04-22T16:25:35.567740435Z AttributeError: 'WSGIRequest' object has no attribute 'user'
2025-04-22T16:25:35.567742073Z 
2025-04-22T16:25:35.567744468Z During handling of the above exception, another exception occurred:
2025-04-22T16:25:35.567745477Z 
2025-04-22T16:25:35.567746347Z Traceback (most recent call last):
2025-04-22T16:25:35.567747258Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 55, in inner
2025-04-22T16:25:35.567748275Z     response = get_response(request)
2025-04-22T16:25:35.567749198Z                ^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.567750130Z   File "/usr/local/lib/python3.11/site-packages/django/utils/deprecation.py", line 129, in __call__
2025-04-22T16:25:35.567751158Z     response = response or self.get_response(request)
2025-04-22T16:25:35.567752094Z                            ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.567753117Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 57, in inner
2025-04-22T16:25:35.567754163Z     response = response_for_exception(request, exc)
2025-04-22T16:25:35.567755103Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.567756042Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 140, in response_for_exception
2025-04-22T16:25:35.567757072Z     response = handle_uncaught_exception(
2025-04-22T16:25:35.567758007Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.567758964Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 185, in handle_uncaught_exception
2025-04-22T16:25:35.567759991Z     return callback(request)
2025-04-22T16:25:35.567760911Z            ^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.567761938Z   File "/app/apps/reloj_fichador/views.py", line 178, in error_500
2025-04-22T16:25:35.567762933Z     'user': request.user,
2025-04-22T16:25:35.567763867Z             ^^^^^^^^^^^^
2025-04-22T16:25:35.567764772Z AttributeError: 'WSGIRequest' object has no attribute 'user'
2025-04-22T16:25:35.567765713Z 
2025-04-22T16:25:35.567766591Z During handling of the above exception, another exception occurred:
2025-04-22T16:25:35.567768623Z 
2025-04-22T16:25:35.567769483Z Traceback (most recent call last):
2025-04-22T16:25:35.567770405Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 55, in inner
2025-04-22T16:25:35.567771431Z     response = get_response(request)
2025-04-22T16:25:35.567772356Z                ^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.567773286Z   File "/usr/local/lib/python3.11/site-packages/django/utils/deprecation.py", line 129, in __call__
2025-04-22T16:25:35.567774274Z     response = response or self.get_response(request)
2025-04-22T16:25:35.567775190Z                            ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.567776147Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 57, in inner
2025-04-22T16:25:35.567777140Z     response = response_for_exception(request, exc)
2025-04-22T16:25:35.567778074Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.567779018Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 140, in response_for_exception
2025-04-22T16:25:35.567780064Z     response = handle_uncaught_exception(
2025-04-22T16:25:35.567780963Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.567781880Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 185, in handle_uncaught_exception
2025-04-22T16:25:35.567782920Z     return callback(request)
2025-04-22T16:25:35.567783820Z            ^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.567784738Z   File "/app/apps/reloj_fichador/views.py", line 178, in error_500
2025-04-22T16:25:35.567785718Z     'user': request.user,
2025-04-22T16:25:35.567786603Z             ^^^^^^^^^^^^
2025-04-22T16:25:35.567787535Z AttributeError: 'WSGIRequest' object has no attribute 'user'
2025-04-22T16:25:35.567788469Z 
2025-04-22T16:25:35.567789343Z During handling of the above exception, another exception occurred:
2025-04-22T16:25:35.567790353Z 
2025-04-22T16:25:35.567791225Z Traceback (most recent call last):
2025-04-22T16:25:35.567792160Z   File "/usr/local/lib/python3.11/site-packages/gunicorn/workers/sync.py", line 134, in handle
2025-04-22T16:25:35.567793170Z     self.handle_request(listener, req, client, addr)
2025-04-22T16:25:35.567794123Z   File "/usr/local/lib/python3.11/site-packages/gunicorn/workers/sync.py", line 177, in handle_request
2025-04-22T16:25:35.567795156Z     respiter = self.wsgi(environ, resp.start_response)
2025-04-22T16:25:35.567796073Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.567796993Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/wsgi.py", line 124, in __call__
2025-04-22T16:25:35.567797993Z     response = self.get_response(request)
2025-04-22T16:25:35.567798925Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.567800754Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/base.py", line 140, in get_response
2025-04-22T16:25:35.567801820Z     response = self._middleware_chain(request)
2025-04-22T16:25:35.567802760Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.567803718Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 57, in inner
2025-04-22T16:25:35.567804725Z     response = response_for_exception(request, exc)
2025-04-22T16:25:35.567805647Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.567806595Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 140, in response_for_exception
2025-04-22T16:25:35.567807630Z     response = handle_uncaught_exception(
2025-04-22T16:25:35.567808575Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.567809502Z   File "/usr/local/lib/python3.11/site-packages/django/core/handlers/exception.py", line 185, in handle_uncaught_exception
2025-04-22T16:25:35.567810529Z     return callback(request)
2025-04-22T16:25:35.567811530Z            ^^^^^^^^^^^^^^^^^
2025-04-22T16:25:35.567813078Z   File "/app/apps/reloj_fichador/views.py", line 178, in error_500
2025-04-22T16:25:35.567814814Z     'user': request.user,
2025-04-22T16:25:35.567815749Z             ^^^^^^^^^^^^
2025-04-22T16:25:35.567816650Z AttributeError: 'WSGIRequest' object has no attribute 'user'
2025-04-23T11:49:08.159842754Z WARNING 2025-04-23 08:49:08,159 base Session data corrupted
2025-04-23T11:49:08.959086824Z WARNING 2025-04-23 08:49:08,958 log Not Found: /favicon.ico
2025-04-23T11:49:16.452876512Z WARNING 2025-04-23 08:49:16,452 models Registros desbalancados para el operario PIZARRO, LEANDRO E. - 39610329 en la fecha 2025-04-23.
2025-04-23T11:49:19.318546871Z WARNING 2025-04-23 08:49:19,318 models Registros desbalancados para el operario PIZARRO, LEANDRO E. - 39610329 en la fecha 2025-04-23.
2025-04-23T11:49:21.718600926Z WARNING 2025-04-23 08:49:21,718 models Registros desbalancados para el operario PIZARRO, LEANDRO E. - 39610329 en la fecha 2025-04-23.
2025-04-23T11:49:28.126960063Z WARNING 2025-04-23 08:49:28,126 models Registros desbalancados para el operario PIZARRO, LEANDRO E. - 39610329 en la fecha 2025-04-23.
2025-04-23T11:49:30.808987001Z Inconsistencia detectada en registro: No se pueden registrar movimientos transitorios después de la salida.
2025-04-23T11:49:30.819672533Z WARNING 2025-04-23 08:49:30,819 log Bad Request: /registrar/salida_transitoria/
2025-04-23T11:49:46.853157453Z WARNING 2025-04-23 08:49:46,853 models Registros desbalancados para el operario PIZARRO, LEANDRO E. - 39610329 en la fecha 2025-04-23.
2025-04-23T17:04:28.790225368Z WARNING 2025-04-23 14:04:28,790 log Not Found: /favicon.ico
2025-04-23T17:05:52.346318262Z WARNING 2025-04-23 14:05:52,346 models Registros desbalancados para el operario MASSAFARA, BRAIAN - 41888232 en la fecha 2025-04-23.
2025-04-23T17:36:40.915019794Z [2025-04-23 17:36:40 +0000] [1] [INFO] Handling signal: term
2025-04-23T17:36:40.915576915Z [2025-04-23 14:36:40 -0300] [109] [INFO] Worker exiting (pid: 109)
2025-04-23T17:36:40.915602509Z [2025-04-23 14:36:40 -0300] [104] [INFO] Worker exiting (pid: 104)
2025-04-23T17:36:40.916546214Z [2025-04-23 14:36:40 -0300] [103] [INFO] Worker exiting (pid: 103)
2025-04-23T17:36:41.115430350Z [2025-04-23 17:36:41 +0000] [1] [INFO] Shutting down: Master
2025-04-23T17:36:42.032076137Z wait-for-it.sh: waiting 120 seconds for db:3306
2025-04-23T17:36:46.037451093Z wait-for-it.sh: db:3306 is available after 4 seconds
2025-04-23T17:36:46.660378906Z Operations to perform:
2025-04-23T17:36:46.660401064Z   Apply all migrations: admin, admin_interface, auth, contenttypes, django_celery_beat, django_celery_results, reloj_fichador, sessions
2025-04-23T17:36:46.660403968Z Running migrations:
2025-04-23T17:36:46.660406092Z   No migrations to apply.
2025-04-23T17:36:47.307273468Z Found another file with the destination path 'admin/js/cancel.js'. It will be ignored since only the first encountered file is collected. If this is not what you want, make sure every static file has a unique path.
2025-04-23T17:36:47.307298574Z Found another file with the destination path 'admin/js/popup_response.js'. It will be ignored since only the first encountered file is collected. If this is not what you want, make sure every static file has a unique path.
2025-04-23T17:36:47.307302044Z 
2025-04-23T17:36:47.307304221Z 0 static files copied to '/app/staticfiles', 225 unmodified.
2025-04-23T17:36:47.454130167Z [2025-04-23 17:36:47 +0000] [1] [INFO] Starting gunicorn 23.0.0
2025-04-23T17:36:47.454234003Z [2025-04-23 17:36:47 +0000] [1] [INFO] Listening at: http://0.0.0.0:58000 (1)
2025-04-23T17:36:47.454245541Z [2025-04-23 17:36:47 +0000] [1] [INFO] Using worker: sync
2025-04-23T17:36:47.455274336Z [2025-04-23 17:36:47 +0000] [111] [INFO] Booting worker with pid: 111
2025-04-23T17:36:47.551983645Z [2025-04-23 17:36:47 +0000] [112] [INFO] Booting worker with pid: 112
2025-04-23T17:36:47.603645970Z [2025-04-23 17:36:47 +0000] [135] [INFO] Booting worker with pid: 135

23T17:37:52.360613881Z /usr/local/lib/python3.11/site-packages/admin_interface/templatetags/admin_interface_tags.py:38: UserWarning: Language chooser requires Django's `set_language` view: `urlpatterns += [url(r'^i18n/', include('django.conf.urls.i18n'))]`.
2025-04-23T17:37:52.360637856Z   warnings.warn(

23T17:37:55.324822485Z /usr/local/lib/python3.11/site-packages/admin_interface/templatetags/admin_interface_tags.py:38: UserWarning: Language chooser requires Django's `set_language` view: `urlpatterns += [url(r'^i18n/', include('django.conf.urls.i18n'))]`.
2025-04-23T17:37:55.324854263Z   warnings.warn(