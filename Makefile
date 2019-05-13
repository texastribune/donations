APP=checkout
NS=texastribune

DOCKER_ENV_FILE?=env-docker
LOG_LEVEL?=INFO

interactive: build backing
	-docker rm -f ${APP}
	-docker volume rm ${APP}_node_modules-vol
	-docker volume create --name ${APP}_node_modules-vol
	docker run \
		--volume=${APP}_node_modules-vol:/app/node_modules \
		--volume=$$(pwd):/app \
		--rm --interactive --tty \
		--env-file=${DOCKER_ENV_FILE} \
		--publish=80:5000 \
		--link=rabbitmq:rabbitmq \
		--link=redis:redis \
		--name=${APP} ${NS}/${APP}:dev bash

build:
	docker build -f Dockerfile --tag=${NS}/${APP}:dev .

clean:
	-docker stop ${APP} && docker rm ${APP}
	-docker stop redis && docker rm redis
	-docker stop rabbitmq && docker rm rabbitmq

backing:
	-docker rm -f rabbitmq redis
	docker run --detach --name rabbitmq --publish=15672:15672 rabbitmq:management
	docker run --detach --name redis redis

test: build
	docker run \
		--workdir=/app \
		--rm \
		--entrypoint=python \
		texastribune/checkout:dev /usr/local/bin/py.test /app/tests.py --cov=/app

reconcile-email:
	docker build --tag=sf-py2 -f Dockerfile.py2 .
	docker run --env-file=${DOCKER_ENV_FILE} --rm --interactive --tty --name=py2 sf-py2

restart:
	-pkill celery
	-pkill python
	C_FORCE_ROOT=True celery -A app.celery worker --without-heartbeat --without-gossip --without-mingle --loglevel=${LOG_LEVEL} &
	python3 app.py & yarn run dev

celery-restart:
	-pkill celery
	C_FORCE_ROOT=True celery -A app.celery worker --without-heartbeat --without-gossip --without-mingle --loglevel=${LOG_LEVEL} &
