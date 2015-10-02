APP=checkout
NS=texastribune

build:
	docker build --tag=${NS}/${APP} .

debug:
	docker run --volumes-from=${APP} --interactive=true --tty=true ${NS}/${APP} bash

run:
	docker run --name=${APP} --detach=true --publish=5000:80 ${NS}/${APP}

clean:
	docker stop ${APP} && docker rm ${APP}

interactive: build
	docker run --workdir=/flask --volume=$$(pwd):/flask --env-file=env --rm --interactive --tty --publish=80:5000 --name=${APP} ${NS}/${APP} bash

push:
	docker push ${NS}/${APP}
