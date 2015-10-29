#ifndef PARSE_H
#define PARSE_H

#include <stdio.h>

typedef struct args args_t;
struct args {
    char *graph_filename;
};
int parse_args(int argc, char **argv, args_t *args);
int print_usage(FILE *stream, int argc, char **argv, char *msg);
int print_help(FILE *stream, int argc, char **argv);


#endif /* PARSE_H */
