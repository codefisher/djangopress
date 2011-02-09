./manage.py dumpdata --indent 2 blog > ../fixtures/blog.json
./manage.py dumpdata --indent 2 links menus > ../fixtures/links.json
./manage.py dumpdata --indent 2 sites > ../fixtures/sites.json
./manage.py dumpdata --indent 2 accounts auth > ../fixtures/auth.json
./manage.py dumpdata --indent 2 pages > ../fixtures/pages.json