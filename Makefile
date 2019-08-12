init:
	pip install -r requirements.txt
test:
	mkdir -p .temp
	python -m unittest discover -v
