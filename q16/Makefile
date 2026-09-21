.PHONY: check build clean

check:
	python -m build >0
	pip install --force-reinstall dist/greetlab_25020007122-0.1.1-py3-none-any.whl 
	./check.sh
	pip uninstall -y greetlab_25020007122
	rm -rf dist

build:
	python -m build 

clean:
	rm -rf dist build *.egg-info
