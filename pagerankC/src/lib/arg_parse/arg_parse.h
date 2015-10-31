#ifndef ARG_PARSE_H
#define ARG_PARSE_H

#include <stdio.h>
#include "../../include/graph_types.h"

typedef struct args args_t;
struct args {
    char *graph_filename;
    graph_filetype_e type;
    int help_printed;
};

int parse_args(int argc, char **argv, args_t *args);
int print_usage(FILE *stream, int argc, char **argv, char *msg);
int print_help(FILE *stream, int argc, char **argv);

#endif /* ARG_PARSE_H */
