#ifndef GRAPH_PARSE_H
#define GRAPH_PARSE_H

#include <stdio.h>
#include "../../include/graph_types.h"

/* Parse functions */
int parse_graph_file(FILE *stream, graph_filetype_e type, graph_record_handler_f handler, void *data);
char *parse_graph_num_line(char *beg_line, graph_record_handler_f handler, void *data);
char *parse_graph_span_line(char *beg_line, graph_record_handler_f handler, void *data);

/* Print functions */
int fprintf_graph(FILE *stream, graph_num_record_t *record);
int printf_graph(graph_num_record_t *record);

#endif /* GRAPH_PARSE_H */
