.PHONY: all

all: daemon

daemon: python/daemon.py
	pyinstaller $< --onefile \
		--workpath ./compile/build \
		--specpath ./compile \
		--hiddenimport packaging.specifiers \
		--hiddenimport packaging.requirements

clean:
	rm -rf ./compile

clear: clean
	rm -rf ./dist
