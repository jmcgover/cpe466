#include "graph_parse.h"

#include <stdlib.h>
#include <string.h>

#define MAX_LINE_LEN 256
#define LINE_LEN MAX_LINE_LEN
static char line[LINE_LEN];

#define COMMENT_CHAR '#'

char *parse_graph_snap_line(char *beg_line, graph_record_handler_f handler, void *data);

/* ----------Primary parsing---------- */
/*
 */
int parse_graph_file(FILE *stream, graph_filetype_e type, graph_record_handler_f handler, void *data) {
    int line_no = 0;

    memset(line, 0, LINE_LEN);
    while (fgets(line, LINE_LEN, stream)) {
        ++line_no;
        if (*line == COMMENT_CHAR) {
            continue;
        }
        switch (type) {
            case NONE:
                printf("%d: %s", line_no, line);
                break;
            case NUM:
                parse_graph_num_line(line, handler, data);
                break;
            case LABEL:
                break;
            case SNAP:
                parse_graph_snap_line(line, handler, data);
                break;
            case HANDLE:
                handler(line, data);
                break;
            case QUIET:
                break;
            default:
                break;
        }
        memset(line, 0, LINE_LEN);
    }
    return EXIT_SUCCESS;
}

/* ----------Parse functions---------- */
/*
 */
#define NUM_DELIM ","
#define BASE10 10
char *parse_graph_num_line(char *beg_line, graph_record_handler_f handler, void *data) {
    char *cur = NULL;
    char *tok = NULL;
    graph_num_record_t record;

    /* Error handling */
    if (beg_line == NULL) {
        return NULL;
    }
    cur = beg_line;

    /* Tokenize and Parse */
    tok = strtok(cur, NUM_DELIM);
    record.node_a_label = strtoll(tok, &cur, BASE10);
    tok = strtok(NULL, NUM_DELIM);
    record.node_a_val = strtoll(tok, &cur, BASE10);
    tok = strtok(NULL, NUM_DELIM);
    record.node_b_label = strtoll(tok, &cur, BASE10);
    tok = strtok(NULL, NUM_DELIM);
    record.node_b_val = strtoll(tok, &cur, BASE10);

    handler(&record, data);

    /* return where the parser ended up */
    return cur;
}

/*
 */
#define NUM_DELIM ","
#define BASE10 10
char *parse_graph_snap_line(char *beg_line, graph_record_handler_f handler, void *data) {
    char *cur = NULL;
    graph_snap_record_t record;

    /* Error handling */
    if (beg_line == NULL) {
        return NULL;
    }
    cur = beg_line;

    /* Parse */
    record.from_node_label = strtoll(cur, &cur, BASE10);
    record.to_node_label = strtoll(cur, &cur, BASE10);
    record.sign = atoi(cur);

    handler(&record, data);

    /* return where the parser ended up */
    return cur;
}

/* ----------Print functions---------- */
/*
 */
int fprintf_graph(FILE *stream, graph_num_record_t *record) {
    int rtn = 0;
    rtn |= fprintf(stream, "GRAPH NUM RECORD:");
    rtn |= fprintf(stream, "\tline_no       : %lld\n", record->line_no);
    rtn |= fprintf(stream, "\tnode_a_label  : %lld\n", record->node_a_label);
    rtn |= fprintf(stream, "\tnode_a_val    : %lld\n", record->node_a_val);
    rtn |= fprintf(stream, "\tnode_b_label  : %lld\n", record->node_b_label);
    rtn |= fprintf(stream, "\tnode_b_val    : %lld\n", record->node_b_val);
    return rtn < 0;
}
/*
 */
int printf_graph(graph_num_record_t *record) {
    return fprintf_graph(stdout, record);
}
