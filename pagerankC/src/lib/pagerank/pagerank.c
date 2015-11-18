#include "pagerank.h"

#include <stdlib.h>


#include <errno.h>
#include <stdio.h>
#include <string.h>
#define ERRNO errno ? errno : EXIT_FAILURE
#define STRERR errno ? strerror(errno) : "errno is useless"
#define PR_ASSERT(SUCCESS_COND, TODO) {\
    if (!(SUCCESS_COND)) {\
        fprintf(stderr, "%s:%d:%s:(%d)%s\n", \
            __FILE__, __LINE__, __func__, errno, STRERR);\
        TODO;\
    }\
}
#define PR_ASSERT_MSG(SUCCESS_COND, msg, TODO) {\
    if (!(SUCCESS_COND)) {\
        fprintf(stderr, "%s:%d:%s:(%d)%s: %s\n", \
            __FILE__, __LINE__, __func__, errno, STRERR, msg);\
        TODO;\
    }\
}

struct pagerank {
    double *pageranks;          /* Array of pagerank values */
    double max_delta;           /* Biggest difference (compared to epsilon) */
    double start_val;           /* Starting value (1/N) */
    long long num_nodes;        /* Number of nodes */
    long long highest_node_num; /* Last node we can index */
    graph_t *graph;
};

pagerank_t *pagerank_init(graph_t *graph) {
    pagerank_t *new_pagerank = NULL;
    long long i;
    double start_val = 0.0;
    long long highest_node_num;
    long long num_nodes;
    int *nodes_used;

    PR_ASSERT_MSG(NULL != graph, "graph cannot be null",
        return NULL;
    );
    highest_node_num = get_highest_node_num(graph);
    num_nodes = get_num_nodes(graph);
    nodes_used = get_node_nums_used(graph);

    /* Make pagerank data structure */
    new_pagerank = calloc(1, sizeof(pagerank_t));
    PR_ASSERT_MSG(NULL != new_pagerank, "new_pagerank calloc failed",
        return NULL;
    );

    /* Make pageranks array */
    new_pagerank->pageranks = calloc(highest_node_num + 1, sizeof(double));
    PR_ASSERT_MSG(NULL != new_pagerank->pageranks, "pagerank array calloc failed",
        free(new_pagerank);
        return NULL;
    );

    /* Fill with default value (1/N) */
    start_val = 1.0 / num_nodes;
    printf("highest: %lld NUm Nodes %lld Start Val : %.12f\n", highest_node_num, num_nodes, start_val);
    for (i = 0; i < highest_node_num + 1; i++) {
        if (nodes_used[i]) {
            new_pagerank->pageranks[i] = start_val;
        }
    }

    /* Assign non-pointer values */
    new_pagerank->highest_node_num = highest_node_num;
    new_pagerank->num_nodes = num_nodes;
    new_pagerank->start_val = start_val;

    return new_pagerank;
}

double *get_pageranks(pagerank_t *pr) {
    return pr->pageranks;
}

int calc_pagerank(pagerank_t *pr, double d, double eps) {
    long long highest_node_num = -1;
    long long *num_out_links = NULL;
    long long *num_in_links = NULL;
    long long **in_link_nodes = NULL;
    long long i, j, node_num_in_links;
    double *new_pageranks = NULL;

    /* Input Checking */
    if (d < 0.0 || d > 1.0) {
        return EXIT_FAILURE;
    }
    if (eps < 0.0) {
        return EXIT_FAILURE;
    }

    /* initialize */
    highest_node_num = get_highest_node_num(pr->graph);
    num_out_links = get_num_out_links(pr->graph);
    num_in_links = get_num_in_links(pr->graph);
    in_link_nodes = get_in_link_nodes(pr->graph);

    /* calculate */
    do {
        new_pageranks = calloc(highest_node_num + 1, sizeof(double));
        for (i = 0; i < highest_node_num + 1; i++) {
            node_num_in_links = num_in_links[i];
            for (j = 0; j < node_num_in_links; j++) {
            }
        }
        free(pr->pageranks);
        pr->pageranks = new_pageranks;
    } while (pr->max_delta > eps);
    return EXIT_SUCCESS;
}
