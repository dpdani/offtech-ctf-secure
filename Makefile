.PHONY: install upload prepare-dependencies upload-dependencies


user_name=`cat deter_username.txt`
folder_name="secure"
red_exp_name="secure-g3"
blue_exp_name="secure-g3"
venv="$(HOME)/.pyenv/versions/ctf-secure"


install:
	red_exp_name=$(red_exp_name) blue_exp_name=$(blue_exp_name) folder_name=$(folder_name) ./install.sh

upload:
	rsync -avz --exclude-from='.rsyncignore' . $(user_name)@users.isi.deterlab.net:~/$(folder_name)

prepare-dependencies:
	rm -rf site-packages
	ssh $(user_name)@users.isi.deterlab.net "rm -rf ~/$(folder_name)/site-packages"
	cp -r $(venv)/lib/python3.6/site-packages/ .

upload-dependencies: prepare-dependencies upload
