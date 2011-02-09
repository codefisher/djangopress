./manage.py syncdb
./manage.py reset --noinput blog links pages menus sites
./manage.py loaddata ../fixtures/*.json

