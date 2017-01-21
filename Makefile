init:
	pip-3.2 install -r requirements.txt

test:
	nosetests test_cat_cannon.py
