SHELL := /bin/bash

install:
	sudo -H ./install.sh

all-tests: test-static-leases test-settings-decoding

test-static-leases:
	( \
	  source ./activate.sh; \
	  /usr/bin/env 	python3 -m unittest test_staticleases.TestStaticLeases; \
	)

test-settings-decoding:
	( \
	  source ./activate.sh; \
	  /usr/bin/env 	python3 -m unittest test_staticleases.TestSettingsDecoding; \
	)

# When adding tests - Do Not Forget to extend the all-tests target
# Keep these lines last in the file, please, and add new tests right before.


