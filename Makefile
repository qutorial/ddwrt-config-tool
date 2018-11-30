SHELL := /bin/bash


default: prior test

test: test-static-leases test-settings-coding test-nvram-coding

prior:
	@echo "Default target is running all tests!"

install:
	sudo -H ./install.sh

test-static-leases:
	( \
	  source ./activate.sh; \
	  /usr/bin/env 	python3 -m unittest test_staticleases.TestStaticLeases; \
	)

test-settings-coding:
	( \
	  source ./activate.sh; \
	  /usr/bin/env 	python3 -m unittest test_settingscoding.TestSettingsDecoding; \
	)

test-nvram-coding:
	( \
	  source ./activate.sh; \
	  /usr/bin/env 	python3 -m unittest test_ddwrtnvram.TestNvramCoding; \
	)

# When adding tests - Do Not Forget to extend the all-tests target
# Keep these lines last in the file, please, and add new tests right before.
