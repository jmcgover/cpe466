CC= 	g++
FLAGS= 	-g -Wall -ansi -pedantic -O3 
LIBS=
PROGS= 	parse
OBJS= 	parse.o

# PARSER
parse: parse.o
	$(CC) $(FLAGS) $(LIBS) $^ -o $@

parse.o: parse.c parse.h
	$(CC) $(FLAGS) $(LIBS) $^ -c
