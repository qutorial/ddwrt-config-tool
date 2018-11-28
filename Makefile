SHELL := /bin/bash

install:
	sudo -H ./install.sh

test: test-static-leases test-settings-coding

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

# When adding tests - Do Not Forget to extend the all-tests target
# Keep these lines last in the file, please, and add new tests right before.
