PWD=$(shell pwd)

build:
	docker build -t easy-wordclouds . --compress

start:
	@make build
	docker run --rm -v ${PWD}/dist:/comments_mapping/dist python-mapping