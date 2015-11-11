#include "../../lib/arg_parse/arg_parse.h"
#include "../../lib/graph/graph.h"
#include "../../lib/graph_parse/graph_parse.h"
#include "../../lib/pagerank/pagerank.h"

#include "../../include/graph_types.h"

#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ERRNO errno ? errno : EXIT_FAILURE
#define STRERR errno ? strerror(errno) : "errno is useless"
#define PARSE_TEST_ASSERT(SUCCESS_COND, TODO) {\
    if (!(SUCCESS_COND)) {\
        fprintf(stderr, "%s:%d:%s:(%d)%s\n", \
            __FILE__, __LINE__, __func__, errno, STRERR);\
        TODO;\
    }\
}

#define MAX(a, b) (a > b ? a : b)
#define MIN(a, b) (a < b ? a : b)

#define WIDTH 20

typedef struct graph_stats graph_stats_t;
struct graph_stats {
    long long num_edges;
    long long highest_node_num;
    long long lowest_node_num;
};
void count_things(void *record, void *data);
void count_things_num(void *record, void *data);
void count_things_snap(void *record, void *data);
void print_things_snap(void *record, void *data);

/*
 * Tests the parsing tools for arguments and graphs to make sure they're
 * correct.
 */
int main(int argc, char **argv) {
    int rtn;
    args_t args = {0};
    FILE *graph_stream = NULL;
    graph_stats_t stats = {0, LLONG_MIN, LLONG_MAX};
    graph_t *graph = NULL;
    pagerank_t *pr_test = NULL;
    double *pageranks = NULL;
    long long i, j;
    long long highest_node_num;
    long long num_in_links;
    long long *in_link_nodes;

    rtn = parse_args(argc, argv, &args);
    if (rtn || args.help_printed) {
        return rtn;
    }

    /* Open file */
    printf("Opening Graph: %s\n", args.graph_filename);
    graph_stream = fopen(args.graph_filename, "r");
    PARSE_TEST_ASSERT(NULL != graph_stream, return ERRNO;);

    /* Parse file */
    switch (args.type) {
        case NONE:
            printf("NONE Type. Doing nothing.\n");
            break;
        case NUM:
            printf("NUM Type. Counting edges and finding MAX/MIN node num....\n");
            parse_graph_file(graph_stream, args.type, count_things_num, &stats);
            printf("%-*s: %lld\n", WIDTH, "Num Edges", stats.num_edges);
            printf("%-*s: %lld\n", WIDTH, "Highest Node Num", stats.highest_node_num);
            printf("%-*s: %lld\n", WIDTH, "Lowest Node Num", stats.lowest_node_num);
            break;
        case LABEL:
            printf("LABEL Type. Counting edges....\n");
            parse_graph_file(graph_stream, args.type, count_things, &stats);
            printf("%-*s: %lld\n", WIDTH, "Num Edges", stats.num_edges);
            break;
        case SNAP:
            printf("SNAP Type. Building graph...\n");
            graph = graph_init(0);
            parse_graph_file(graph_stream, args.type, graph_snap_handler, graph);
            printf("DONE.\n");
            highest_node_num = get_highest_node_num(graph);
            printf("Highest node num: %lld\n", highest_node_num);
            for (i = 0; i < 10 + 1; i++) {
                in_link_nodes = get_in_links(graph, i);
                num_in_links = get_num_in_links(graph, i);
                printf("-------------------------\n");
                printf("Node %lld (%lld): ", i, num_in_links);
                for (j = 0; j < num_in_links; j++) {
                    printf("%lld, ", in_link_nodes[j]);
                }
                printf("\n");
                printf("-------------------------\n");
            }
            printf("Initializing pageranks...\n");
            pr_test = pagerank_init(graph);
            pageranks = get_pageranks(pr_test);
            for (i = 0; i < 10; i++) {
                printf("%lld: %.12f\n", i, pageranks[i]);
            }
            graph_destroy(graph);
            /*             parse_graph_file(graph_stream, args.type, print_things_snap, &stats); */
            break;
        case HANDLE:
            printf("HANDLE Type. Doing nothing.\n");
            break;
        case QUIET:
            printf("QUIET Type. Counting edges....\n");
            parse_graph_file(graph_stream, args.type, count_things, &stats);
            printf("%-*s: %lld\n", WIDTH, "Num Edges", stats.num_edges);
            break;
        default:
            break;
    }


    /* Close file */
    rtn = fclose(graph_stream);
    PARSE_TEST_ASSERT(!errno, return ERRNO;);

    fprintf(stdout, "Hello, World!\n");
    return 0;
}

void count_things(void *record, void *data) {
    graph_stats_t *stats = data;
    stats->num_edges++;
}

void count_things_num(void *record, void *data) {
    graph_stats_t *stats = data;
    graph_num_record_t *num_record = record;
    stats->num_edges++;
    stats->highest_node_num = MAX(num_record->node_a_label, stats->highest_node_num);
    stats->highest_node_num = MAX(num_record->node_b_label, stats->highest_node_num);
    stats->lowest_node_num = MIN(num_record->node_a_label, stats->lowest_node_num);
    stats->lowest_node_num = MIN(num_record->node_b_label, stats->lowest_node_num);
}

void count_things_snap(void *record, void *data) {
    graph_stats_t *stats = data;
    graph_snap_record_t *snap_record = record;
    stats->num_edges++;
    stats->highest_node_num = MAX(snap_record->from_node_label, stats->highest_node_num);
    stats->highest_node_num = MAX(snap_record->to_node_label, stats->highest_node_num);
    stats->lowest_node_num = MIN(snap_record->from_node_label, stats->lowest_node_num);
    stats->lowest_node_num = MIN(snap_record->to_node_label, stats->lowest_node_num);
}

void print_things_snap(void *record, void *data) {
    graph_snap_record_t *snap_record = record;
    printf("%-*s: %lld\n", WIDTH, "from_node_label", snap_record->from_node_label);
    printf("%-*s: %lld\n", WIDTH, "to_node_label", snap_record->to_node_label);
    printf("%-*s: %d\n", WIDTH, "sign", snap_record->sign);
}
