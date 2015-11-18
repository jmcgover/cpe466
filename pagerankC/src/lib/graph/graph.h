#ifndef GRAPH_H
#define GRAPH_H

/*
 *
 */
typedef struct graph graph_t;

/* Constructor*/
graph_t *graph_init();
void graph_destroy(graph_t *graph);

/* Modifiers */
int add_in_link(graph_t *graph, long long from_node, long long to_node);

/* Getters */
long long get_nodes_num_in_links(graph_t *graph, long long node);
long long **get_in_link_nodes(graph_t *graph);
long long *get_in_links(graph_t *graph, long long node);
long long *get_in_edges(graph_t *graph, long long node);
long long *get_num_in_links(graph_t *graph);
long long *get_num_out_links(graph_t *graph);
long long get_highest_node_num(graph_t *graph);
long long get_num_nodes(graph_t *graph);
int *get_node_nums_used(graph_t *graph);

/* Hadnler */
void graph_num_handler(void *record, void *data);
void graph_snap_handler(void *record, void *data);

#endif /* GRAPH_H */
