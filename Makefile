PWD=$(shell pwd)

build:
	docker build -t easy-wordclouds . --compress

start:
	@make build
	docker run --rm -v ${PWD}/dist:/basic_linguistic_indicators/dist easy-wordclouds
#	docker cp easy-wordclouds:/dist/wordcloud.png $(PWD)/dist/wordcloud.png
#	docker stop easy-wordclouds

test:
	pytest $(find **/*.py) --cov=. --cov-fail-under=90 --cov-report term-missing

lint:
	pylint ./**/*.py

dep:
	pip install pylint
	pip install -r requirements.txt

dep3:
	pip3 install pylint
	pip3 install -r requirements.txt