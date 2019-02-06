SHELL := /bin/bash


default: prior test

test: test-static-leases test-settings-coding test-nvram-coding test-mnvram test-router test-lease test-leases-router test-add-static-lease test-read-leases test-read-sshd-config

prior:
	@echo "Default target is running all tests!"

install:
	sudo -H ./install.sh

install-dev:
	sudo -H ./install.sh dev

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

test-mnvram:
	( \
	  source ./activate.sh; \
	  /usr/bin/env 	python3 -m unittest test_mnvram.TestMnvram; \
	)

test-router:
	( \
	  source ./activate.sh; \
	  /usr/bin/env 	python3 -m unittest test_router.TestRouter; \
	)

test-lease:
	( \
	  source ./activate.sh; \
	  /usr/bin/env 	python3 -m unittest test_lease.TestLease; \
	)

test-leases-router:
	( \
	  source ./activate.sh; \
	  /usr/bin/env 	python3 -m unittest test_leases_router.TestLeasesRouter; \
	)

test-add-static-lease:
	( \
	  source ./activate.sh; \
	  /usr/bin/env 	python3 -m unittest test_add_static_lease.TestAddStaticLease; \
	)

test-read-leases:
	( \
	  source ./activate.sh; \
	  /usr/bin/env 	python3 -m unittest test_read_leases.TestReadLeases; \
	)

test-read-sshd-config:
	( \
	  source ./activate.sh; \
	  /usr/bin/env 	python3 -m unittest test_read_sshd_config.TestReadSshdConfig; \
	)


# When adding tests - Do Not Forget to extend the all-tests target
# Keep these lines last in the file, please, and add new tests right before.
