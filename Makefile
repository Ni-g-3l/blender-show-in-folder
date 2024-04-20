PACKAGE_VERSION = $(shell grep -oP 'version": \((.*?)\)' $(CURDIR)/show_in_folder_addon/__init__.py | cut -d'(' -f2 | cut -d')' -f1 | sed 's/, /./g')

install_dev:
	rm -rf /tmp/blender/show_in_folder_env
	mkdir /tmp/blender/show_in_folder_env/scripts/addons -p
	ln $(CURDIR)/show_in_folder_addon /tmp/blender/show_in_folder_env/scripts/addons/show_in_folder_addon -s

run:
	export BLENDER_USER_SCRIPTS=/tmp/blender/show_in_folder_env/scripts; \
	blender --addons show_in_folder_addon

deploy:release

release:build clean
	@echo "------------------- RELEASE PACKAGE ------------------- "
	@echo Releasing ${PACKAGE_VERSION} version
	@git tag ${PACKAGE_VERSION} || echo "Tag already exists."
	@echo "------------------------------------------------------- "

build: clean
	@echo "-------------------- BUILD PACKAGE -------------------- "
	mkdir -p dist
	zip -r dist/show_in_folder_addon-${PACKAGE_VERSION}.zip show_in_folder_addon
	@echo "------------------------------------------------------- "

clean:
	@echo "-------------------- CLEAN PACKAGE -------------------- "
	find . -name \*.pyc -delete
	find . -name __pycache__ -delete
	@echo "------------------------------------------------------- "