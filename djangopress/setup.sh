python ../manage.py sqlclear blog links pages menus sites downloads forum auth donate ipn
python ../manage.py migrate
python ../manage.py loaddata ../fixtures/*.json

