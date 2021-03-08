#!/usr/bin/make -f

DOCKER_COMPOSE_CMD = docker-compose

-include Makefile.variable

ifdef DOCKER_HOST
	DOCKER_COMPOSE_CMD += --host ${DOCKER_HOST}
endif

LC_ALL := C
.DEFAULT_GOAL := all
.PHONY: all

all:
	${DOCKER_COMPOSE_CMD} build
	${DOCKER_COMPOSE_CMD} up --detach
