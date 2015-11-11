#ifndef GRAPH_TYPES_H
#define GRAPH_TYPES_H

/* ----------Graph file types---------- */
typedef enum {
    NONE = 0,
    NUM,
    LABEL,
    SNAP,
    HANDLE,
    QUIET
} graph_filetype_e;

/* ----------Graph record types---------- */
/*
 * Graph record handler
 *
 * \typedef
 *
 * @param [in] <record> {}
 * @param [in,out] <data> {data that the handler may need to }
 */
typedef void (*graph_record_handler_f)(void *record, void *data);

/*
 * NUM
 */
typedef struct graph_num_record graph_num_record_t;
struct graph_num_record {
    long long line_no;
    long long node_a_label;
    long long node_a_val;
    long long node_b_label;
    long long node_b_val;
};

/*
 * LABEL
 */
typedef struct graph_label_record graph_label_record_t;
struct graph_label_record {
    long long line_no;
    char * node_a_label;
    long long node_a_val;
    char * node_b_label;
    long long node_b_val;
};

/*
 * SPAN
 */
typedef struct graph_snap_record graph_snap_record_t;
struct graph_snap_record {
    long long line_no;
    long long from_node_label;
    long long to_node_label;
    int sign;
};

#endif /* GRAPH_TYPES_H */
