#ifndef GRAPH_TYPES_H
#define GRAPH_TYPES_H

typedef enum {
    NONE = 0,
    NUM,
    LABEL,
    SNAP,
    QUIET
} graph_filetype_e;

typedef struct graph_num_record graph_num_record_t;
struct graph_num_record {
    long long line_no;
    long long node_a_label;
    long long node_a_val;
    long long node_b_label;
    long long node_b_val;
};

#endif /* GRAPH_TYPES_H */
