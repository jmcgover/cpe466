SHELL := /bin/bash

CC := gcc
CFLAGS := -g -O3 -MMD -Wall -Wno-unused-parameter $(EXTRA_CFLAGS)
LDFLAGS := -pthread
INCLUDES := -I../../lib
OUTFILE := $(BIN)$(LIB)

.PHONY: default clean

default: $(OUTFILE)

clean:
	$(RM) -fv *.o *.gch *~ $(OUTFILE)

-include *.d

%.o: %.c
	$(CC) $(CFLAGS) -o $@ -c $< $(INCLUDES)
