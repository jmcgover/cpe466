#include "../../lib/arg_parse/arg_parse.h"
#include "../../lib/graph_parse/graph_parse.h"
#include "../../include/graph_types.h"

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define PARSE_TEST_ASSERT(SUCCESS_COND, TODO) {\
    if (!(SUCCESS_COND)) {\
        fprintf(stderr, "%s:%d:%s:(%d)%s\n", \
            __FILE__, __LINE__, __func__, errno, errno ? strerror(errno) : "errno is useless");\
        TODO;\
    }\
}
#define ERRNO errno ? errno : EXIT_FAILURE

/*
 * Tests the parsing tools for arguments and graphs to make sure they're
 * correct.
 */
int main(int argc, char **argv) {
    int rtn;
    args_t args = {0};
    FILE *graph_stream = NULL;

    rtn = parse_args(argc, argv, &args);
    if (rtn || args.help_printed) {
        return rtn;
    }

    /* Open file */
    printf("Opening Graph: %s\n", args.graph_filename);
    graph_stream = fopen(args.graph_filename, "r");
    PARSE_TEST_ASSERT(NULL != graph_stream, return ERRNO;);

    /* Parse file */
    parse_graph_file(graph_stream, args.type);

    /* Close file */
    rtn = fclose(graph_stream);
    PARSE_TEST_ASSERT(!errno, return ERRNO;);

    fprintf(stdout, "Hello, World!\n");
    return 0;
}
