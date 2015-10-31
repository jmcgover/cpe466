SHELL := /bin/bash

lib_argparse := src/lib/argparse
parse_test := src/app/parse_test/

libraries := $(lib_argparse)
apps := $(parse_test)
dirs := $(libraries) $(apps)

.PHONY: all $(apps) $(libraries)

all: $(apps)

$(apps): $(libraries)
	$(MAKE) -C $@

$(libraries):
	$(MAKE) -C $@
	mkdir -p ./lib
	cp $@/*.a ./lib

clean: 
	$(RM) bin/* lib/*
	for DIR in ${dirs}; do make -C $${DIR} clean; done
