DC=docker compose
D=docker

CONTAINER?=app




%:
	@:

args = `arg="$(filter-out $@,$(MAKECMDGOALS))" && echo $${arg:-${1}}`

.PHONY: up rebuild exec action

up:
	$(DC) up

rebuild:
	$(DC) build --no-cache
	$(DC) up

shell:
	$(D) exec -it $(call args, $(CONTAINER)) /bin/bash

requirements:
	$(D) exec $(CONTAINER) pip-compile -o requirements.txt requirements.in;