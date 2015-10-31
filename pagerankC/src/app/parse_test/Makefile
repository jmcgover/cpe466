BIN := parse_test
OBJS:= main.o

PAGERANK_LIBS := arg_parse/libarg_parse.a\
		 graph_parse/libgraph_parse.a

include ../../app.mk

libs:
	$(MAKE) -C ../../../

cleanall:
	$(MAKE) -C ../../../ clean
