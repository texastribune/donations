APP=checkout
NS=texastribune

DOCKER_ENV_FILE?=env-docker
LOG_LEVEL?=INFO

dev:
	docker-compose run --service-ports donations --build

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
		--publish=5678:5678 \
		--link=rabbitmq:rabbitmq \
		--link=redis:redis \
		--name=${APP} ${NS}/${APP}:dev bash

shell: build
	-docker rm -f ${APP}-shell
	docker run \
		--volume=$$(pwd):/app \
		--rm --interactive --tty \
		--env-file=${DOCKER_ENV_FILE} \
		--name=${APP}-shell ${NS}/${APP}:dev bash

build:
	docker build -f Dockerfile --tag=${NS}/${APP}:dev .

clean:
	-docker stop ${APP} && docker rm ${APP}
	-docker stop redis && docker rm redis
	-docker stop rabbitmq && docker rm rabbitmq
	rm -rf .mypy_cache

backing:
	-docker rm -f rabbitmq redis
	docker run --detach --name rabbitmq --publish=15672:15672 rabbitmq:management
	docker run --detach --name redis redis

test: build
	DEBUG=False docker run -it --env-file=env-docker --rm --volume=$$(pwd):/app --entrypoint=/app/test-entrypoint.sh ${NS}/${APP}:dev
# 	docker run \
# 		--workdir=/app \
# 		--rm \
# 		--entrypoint=python \
# 		texastribune/checkout:dev /app/test-entrypoint.sh
# #		texastribune/checkout:dev /usr/local/bin/py.test -x /app/test_all.py --cov=/app

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
