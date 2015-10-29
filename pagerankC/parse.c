#include "parse.h"

#include <stdio.h>
#include <errno.h>

#define TRUE  1
#define FALSE 0

typedef struct args args_t;
struct args {
    char *graph_filename;
};
int parse_args(int argc, char **argv);
void print_usage(int argc, char **argv, char *msg);
int print_help(FILE *stream, int argc, char **argv);

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

/*
 * \brief Parses the arguments passed in from CLI
 *
 * @param argc   int number of arguments
 * @param argv   char ** pointer to the array of string arguments
 */
int parse_args(int argc, char **argv, args_t *args) {
    if (args == NULL) {
        return EINVAL;
    }

    return EXIT_SUCCESS;
}

/*
 * \brief Prints simply the usage of the program.
 *
 * @param stream FILE * pointer to the outgoing stream to print to
 * @param argc   int number of arguments
 * @param argv   char ** pointer to the array of string arguments
 * @param msg    char *  string to print above the usage, if NULL, nothing is
 *               printed, otherwise, the message outputs with a newline
 *               character
 */
#define USAGE_FMT  "%s %s\n"
#define USAGE_OPTS "[none yet...]"
int print_usage(FILE *stream, int argc, char **argv, char *msg) {
    if (msg) {
        fprintf(stream, "%s\n", msg);
    }
    fprintf(stream, USAGE_FMT, argv[0], USAGE_OPTS);
    return EXIT_SUCCESS;
}

/*
 * \brief Prints the short and long options with a description
 *
 * @param stream FILE * pointer to the outgoing stream to print to
 * @param argc   int number of arguments
 * @param argv   char ** pointer to the array of string arguments
 */
#define OPT_WIDTH 10
int print_opt(File *stream, char opt_short, char *opt_long, char *description) {
    if (opt_short && opt_long) {
        fprintf(stream, "-%c, --%-*s %s", opt_short, OPT_WIDTH, opt_long, description);
    } else {
        if (opt_short) {
            fprintf(stream, "-%c %-*s %s", opt_short, OPT_WIDTH, " ", description);
        } else if (opt_long) {
            fprintf(stream, "%-*s %s", opt_short, OPT_WIDTH, opt_long, description);
        } else {
        }
    }
    return EXIT_SUCCESS;
}

/*
 * \brief Prints the more descriptive help text that includes the long and
 *        short args
 *
 * @param stream FILE * pointer to the outgoing stream to print to
 * @param argc   int number of arguments
 * @param argv   char ** pointer to the array of string arguments
 */
#define USAGE_DESCR "This will do something"
int print_help(FILE *stream, int argc, char **argv) {
    fprintf(stream, "%s\n", USAGE_DESCR);
    return EXIT_SUCCESS;
}
