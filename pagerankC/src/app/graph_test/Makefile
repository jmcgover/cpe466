BIN := graph_test
OBJS:= main.o

PAGERANK_LIBS := graph/libgraph.a

include ../../app.mk

libs:
	$(MAKE) -C ../../../

cleanall:
	$(MAKE) -C ../../../ clean
