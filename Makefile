APP=checkout
NS=texastribune

build:
	docker build --tag=${NS}/${APP} .

debug:
	docker run --volumes-from=${APP} --interactive=true --tty=true ${NS}/${APP} bash

build-dev: build
	docker build -f Dockerfile.dev --tag=${NS}/${APP}:dev .

run:
	docker run --name=${APP} --detach=true --publish=5000:80 ${NS}/${APP}

clean:
	-docker stop ${APP} && docker rm ${APP}
	-docker stop redis && docker rm redis
	-docker stop rabbitmq && docker rm rabbitmq

backing:
	docker run --detach --name rabbitmq rabbitmq
	docker run --detach --name redis redis

interactive: build-dev
	docker run \
		--workdir=/flask \
		--volume=$$(pwd):/flask \
		--env-file=env \
		--rm --interactive --tty \
		--publish=80:5000 \
		--publish=5555:5555 \
		--link=rabbitmq:rabbitmq \
		--link=redis:redis \
		--name=${APP} ${NS}/${APP}:dev bash

test: build-dev
	docker run \
		--env-file=env \
		--workdir=/app \
		--rm \
		--entrypoint=python3 \
		texastribune/checkout:dev /usr/local/bin/py.test tests.py --cov=.

push:
	docker push ${NS}/${APP}
