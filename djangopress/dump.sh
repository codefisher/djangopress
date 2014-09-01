python ../manage.py dumpdata --indent 2 blog > ../fixtures/blog.json
python ../manage.py dumpdata --indent 2 forum > ../fixtures/forum.json
python ../manage.py dumpdata --indent 2 menus > ../fixtures/links.json
python ../manage.py dumpdata --indent 2 sites > ../fixtures/sites.json
python ../manage.py dumpdata --indent 2 accounts auth > ../fixtures/auth.json
python ../manage.py dumpdata --indent 2 pages feed_block > ../fixtures/pages.json
python ../manage.py dumpdata --indent 2 downloads extension_downloads > ../fixtures/downloads.json
python ../manage.py dumpdata --indent 2 donate ipn > ../fixtures/donate.json
