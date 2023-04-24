#!/usr/bin/env sh
env/bin/celery -A solotodo_core multi restart store_update general reports storescraper --pidfile=solotodo_core/pids/celery/%n.pid --logfile=solotodo_core/logs/celery/%n.log -l info