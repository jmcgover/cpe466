#include "parse.h"

/*
 * Runs the main sequence of instructions
 */
int main(int argc, char **argv) {
    int rtn;
    args_t args;

    rtn = parse_args(argc, argv, &args);
    if (rtn) {
        return rtn;
    }
    fprintf(stdout, "Hello, World!\n");
    return 0;
}

