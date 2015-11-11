#ifndef PAGERANK_H
#define PAGERANK_H
#include "../graph/graph.h"

typedef struct pagerank pagerank_t;

pagerank_t *pagerank_init(graph_t *graph);
double *get_pageranks(pagerank_t *pr);

#endif /* PAGERANK_H */
