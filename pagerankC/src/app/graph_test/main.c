#include "../../lib/graph/graph.h"

#include "../../include/graph_types.h"

#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ERRNO errno ? errno : EXIT_FAILURE
#define STRERR errno ? strerror(errno) : "errno is useless"
#define GRAPH_TEST_ASSERT(SUCCESS_COND, TODO) {\
    if (!(SUCCESS_COND)) {\
        fprintf(stderr, "%s:%d:%s:(%d)%s\n", \
            __FILE__, __LINE__, __func__, errno, STRERR);\
        TODO;\
    }\
}


int main(int argc, char **argv) {
    graph_t *graph = NULL;
    long long a, b;
    /* Initialize graph */
    graph = graph_init(0);
    GRAPH_TEST_ASSERT(graph, return ERRNO);

    /* Add some links */
    a = 1;
    b = 2;
    fprintf(stderr, "Adding from %lld to %lld...\n", a, b);
    add_in_link(graph, a, b);

    a = 17;
    b = 1000;
    fprintf(stderr, "Adding from %lld to %lld...\n", a, b);
    add_in_link(graph, a, b);

    /* Destroy graph */
    graph_destroy(graph);
    fprintf(stderr, "SUCCESS!\n");
    return EXIT_SUCCESS;
}
