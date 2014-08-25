python ../manage.py sqlclear blog links pages menus sites downloads forum auth donate ipn
rm -f ../*.db
echo "no" | python ../manage.py syncdb
python ../manage.py loaddata ../fixtures/*.json

