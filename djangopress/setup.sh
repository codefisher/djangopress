rm -f ../sqlite.db

echo "no" | ./manage.py syncdb

#./manage.py schemamigration blog --initial
#./manage.py schemamigration accounts --initial
#./manage.py schemamigration menus --initial
#./manage.py schemamigration core --initial
#./manage.py schemamigration core.links --initial
#./manage.py schemamigration pages --initial
#./manage.py migrate accounts
#./manage.py migrate

./manage.py createsuperuser --username=michael --email=m@xrl.in
./manage.py loaddata ../fixtures/*.json

#./manage.py importnews
