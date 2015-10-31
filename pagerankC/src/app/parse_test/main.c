#include "../../lib/arg_parse/arg_parse.h"

/*
 * Runs the main sequence of instructions
 */
int main(int argc, char **argv) {
    int rtn;
    args_t args = {0};

    rtn = parse_args(argc, argv, &args);
    if (rtn || args.help_printed) {
        return rtn;
    }
    printf("Graph Filename: %s\n", args.graph_filename);
    print_usage(stdout, argc, argv, NULL);
    print_help(stderr, argc, argv);
    fprintf(stdout, "Hello, World!\n");
    return 0;
}

