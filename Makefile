SHELL := /bin/bash

all-tests: test-static-leases

test-static-leases:
	( \
	  source ./activate.sh; \
	  /usr/bin/env 	python3 -m unittest test_staticleases.TestStaticLeases; \
	)

# When adding tests - Do Not Forget to extend the all-tests target
# Keep these lines last in the file, please, and add new tests right before.


