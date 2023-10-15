.PHONY: build
build:
	./$@.sh

.PHONY: deploy
deploy:
	./$@.sh

.PHONY: rsync-push rsync-pull
rsync-push:
	./rsync.sh push

rsync-pull:
	./rsync.sh pull

.PHONY: open-vscode
open-vscode:
	bash -c 'cd .. && code --disable-extension=ms-vscode-remote.remote-containers --folder-uri=vscode-remote://ssh-remote+mariadb-operator//workspace/mariadb-operator'
