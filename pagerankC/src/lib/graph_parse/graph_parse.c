#include "graph_parse.h"

#include <stdlib.h>
#include <string.h>
#define MAX_LINE_LEN 256
#define LINE_LEN MAX_LINE_LEN
static char line[LINE_LEN];

int parse_graph_file(FILE *stream, graph_filetype_e type) {
    int line_no = 0;

    memset(line, 0, LINE_LEN);
    while (fgets(line, LINE_LEN, stream)) {
        switch (type) {
            case NONE:
                printf("%d: %s", ++line_no, line);
                break;
            case NUM:
                break;
            case LABEL:
                break;
            case SNAP:
                break;
            case QUIET:
                break;
        }
        memset(line, 0, LINE_LEN);
    }
    return EXIT_SUCCESS;
}

char *parse_graph_num_line(char *beg_line, graph_num_record_t *record) {
    char *cur = NULL;
    if (beg_line == NULL) {
        return beg_line;
    }
    return cur;
}
