#ifndef GRAPH_PARSE_H
#define GRAPH_PARSE_H

typedef struct graph_num_record graph_num_record_t;
struct graph_num_record {
    long long line_no;
    long long node_a;
    long long node_a_val;
    long long node_b;
    long long node_b_val;
};

char *parse_graph_num_line(char *beg_line, graph_num_record_t *record);

#endif /* GRAPH_PARSE_H */
