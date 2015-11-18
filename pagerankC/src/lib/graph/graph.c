#include "graph.h"

#include "../../include/graph_types.h"

#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ERRNO errno ? errno : EXIT_FAILURE
#define STRERR errno ? strerror(errno) : "errno is useless"
#define GRAPH_ASSERT(SUCCESS_COND, TODO) {\
    if (!(SUCCESS_COND)) {\
        fprintf(stderr, "%s:%d:%s:(%d)%s\n", \
            __FILE__, __LINE__, __func__, errno, STRERR);\
        TODO;\
    }\
}

#define MAX(a, b) (a > b ? a : b)
#define MIN(a, b) (a < b ? a : b)
#define TRUE  1
#define FALSE 0

struct graph {
    /* long long num_nodes;        Number of nodes (not necessarily size) */
    long long num_edges;        /* Number of nodes (not necessarily size) */
    long long highest_node_num; /* Last index in arrays below. */
    long long *num_out_links;   /* Each element is the node number's number of outgoing edges */
    long long *num_in_links;    /* Each element is the node number's number of incoming edges */
    long long **in_link_nodes;  /* Each element points to an array containing the node
                                   number that inlinks */
    int *node_nums_used;        /* Whether each node is used */
    int num_nodes;        /* Whether each node is used */
};

/* Constructor*/
graph_t *graph_init(long long initial_highest) {
    graph_t *new_graph = NULL;
    new_graph = calloc(1, sizeof(graph_t));
    if (initial_highest) {
        new_graph->highest_node_num = initial_highest;
        new_graph->num_out_links    = calloc(initial_highest + 1, sizeof(long long));
        new_graph->num_in_links     = calloc(initial_highest + 1, sizeof(long long));
        new_graph->in_link_nodes    = calloc(initial_highest + 1, sizeof(long long *));
    }
    return new_graph;
}
void graph_destroy(graph_t *graph) {
    free(graph);
}

/* Modifiers */
int resize_graph(graph_t *graph, long long new_highest) {
    long long *num_out_links;
    long long *num_in_links;
    int *node_nums_used;
    long long **in_link_nodes;

    if (new_highest == 0) {
        return EXIT_SUCCESS;
    }
    if (graph->highest_node_num > new_highest) {
        return EXIT_FAILURE;
    }

    num_out_links    = calloc(new_highest + 1, sizeof(long long));
    num_in_links     = calloc(new_highest + 1, sizeof(long long));
    in_link_nodes    = calloc(new_highest + 1, sizeof(long long *));
    node_nums_used   = calloc(new_highest + 1, sizeof(int));

    GRAPH_ASSERT(num_out_links, exit(ERRNO));
    GRAPH_ASSERT(num_in_links, exit(ERRNO));
    GRAPH_ASSERT(in_link_nodes, exit(ERRNO));
    GRAPH_ASSERT(node_nums_used, exit(ERRNO));

    if (graph->highest_node_num) {
        memcpy(num_out_links , graph->num_out_links , (graph->highest_node_num + 1) * sizeof(long long));
        memcpy(num_in_links  , graph->num_in_links  , (graph->highest_node_num + 1) * sizeof(long long));
        memcpy(in_link_nodes , graph->in_link_nodes , (graph->highest_node_num + 1) * sizeof(long long *));
        memcpy(node_nums_used, graph->node_nums_used, (graph->highest_node_num + 1) * sizeof(int));
    }

    free(graph->num_out_links);
    free(graph->num_in_links);
    free(graph->in_link_nodes);
    free(graph->node_nums_used);

    graph->highest_node_num = new_highest;
    graph->num_out_links    = num_out_links;
    graph->num_in_links     = num_in_links;
    graph->in_link_nodes    = in_link_nodes;
    graph->node_nums_used   = node_nums_used;

    return EXIT_SUCCESS;
}
int add_in_link(graph_t *graph, long long from_node, long long to_node) {
    long long *new_neighbors = NULL;
    long long new_highest_node = LLONG_MIN;
    long long noi = -1;
    long long i;

    if (from_node == to_node) {
        return EXIT_SUCCESS;
    }

    if (noi == to_node) {
        printf("Size before resizing: %lld\n", graph->num_in_links[to_node]);
    }
    new_highest_node = MAX(from_node, to_node);
    if (new_highest_node > graph->highest_node_num) {
        /*
        fprintf(stderr, "Inscreasing data structures size to %lld...\n", new_highest_node);
        */
        resize_graph(graph, new_highest_node);
    }

    /* Increase size of in-links list */
    new_neighbors = calloc(graph->num_in_links[to_node] + 1, sizeof(long long));
    GRAPH_ASSERT(new_neighbors, exit(ERRNO));
    /* Copy the previous links over */
    memcpy(new_neighbors, graph->in_link_nodes[to_node], graph->num_in_links[to_node] * sizeof(long long));
    /* Free former space */
    if (to_node == noi) {
        printf("Adding %lld to node %lld (%lld): \n", from_node, noi, graph->num_in_links[to_node]);
        for (i = 0; i < graph->num_in_links[to_node]; i++) {
            printf("%lld, ", graph->in_link_nodes[to_node][i]);
        }
        printf("->");
        for (i = 0; i < graph->num_in_links[to_node] + 1; i++) {
            printf("%lld, ", new_neighbors[i]);
        }
        printf("\n");
    }
    free(graph->in_link_nodes[to_node]);
    /* Point to new list */
    graph->in_link_nodes[to_node] = new_neighbors;

    if (graph->num_in_links[to_node] == 0 && graph->num_out_links[to_node] == 0) {
        graph->num_nodes++;
    }
    if (graph->num_in_links[from_node] == 0 && graph->num_out_links[from_node] == 0) {
        graph->num_nodes++;
    }
    if (to_node == from_node) {
        fprintf(stderr, "FUCK FUCK FUCK %lld == %lld\n", to_node, from_node);
    }

    /* Record new in link */
    graph->in_link_nodes[to_node][graph->num_in_links[to_node]] = from_node;
    graph->num_in_links[to_node]++;
    graph->num_out_links[from_node]++;
    graph->node_nums_used[to_node] = TRUE;
    graph->node_nums_used[from_node] = TRUE;
    return EXIT_SUCCESS;
}

/* Getters */
long long *get_in_links(graph_t *graph, long long node) {
    return graph->in_link_nodes[node];
}

long long get_nodes_num_in_links(graph_t *graph, long long node) {
    return graph->num_in_links[node];
}
/*
long long *get_in_edges(graph_t *graph, long long node) {
    return graph->in_link_edges[node];
}
*/
long long **get_in_link_nodes(graph_t *graph) {
    return graph->in_link_nodes;
}
long long *get_num_in_links(graph_t *graph) {
    return graph->num_in_links;
}
long long *get_num_out_links(graph_t *graph) {
    return graph->num_out_links;
}

long long get_highest_node_num(graph_t *graph) {
    return graph->highest_node_num;
}
long long get_num_nodes(graph_t *graph) {
    return graph->num_nodes;
}
int *get_node_nums_used(graph_t *graph) {
    return graph->node_nums_used;
}

void graph_num_handler(void *record, void *data) {
    /*
    graph_num_record_t *parsed = record;
    graph_t *graph = data;
    long long from_node;
    long long to_node;
    long long edge_value;
    */
}
void graph_snap_handler(void *record, void *data) {
    graph_snap_record_t *parsed = record;
    graph_t *graph = data;
    add_in_link(graph, parsed->from_node_label, parsed->to_node_label);
}
