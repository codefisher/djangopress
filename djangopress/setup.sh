rm -f ../sqlite.db

echo "no" | ./manage.py syncdb

./manage.py migrate blog
./manage.py migrate accounts
./manage.py migrate menus
./manage.py migrate util
./manage.py migrate

./manage.py loaddata ../fixtures/*

./manage.py createsuperuser --username=michael --email=m@xrl.in
