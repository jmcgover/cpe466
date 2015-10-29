#CC= 	g++
CC= 	gcc
FLAGS= 	-g -Wall -ansi -pedantic -O3 
LIBS=
PROGS= 	parse
OBJS= 	parse.o

# PARSER
parse: parse.o main.c
	$(CC) $(FLAGS) $(LIBS) $^ -o $@

parse.o: parse.c parse.h
	$(CC) $(FLAGS) $(LIBS) $^ -c

clean: 
	rm -fv $(OBJS)

cleanall: clean
	rm -fv $(PROGS) *.gch
