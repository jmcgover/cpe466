#include "arg_parse.h"

#include <errno.h>
#include <getopt.h>
#include <stdlib.h>
#include <string.h>

#define TRUE  1
#define FALSE 0

/*
 * \brief Parses the arguments passed in from CLI
 *
 * @param [in] <argc> {number of arguments}
 * @param [in] <argv> {pointer to the array of string arguments}
 */
static char     short_options[] = "f:h";
static struct   option long_options[] = {
    {"file", required_argument, NULL, 'f'},
    {"help", no_argument, NULL, 'h'},
    {0, 0, 0, 0}
};
int parse_args(int argc, char **argv, args_t *args) {
    int help_requested = FALSE;
    if (args == NULL) {
        return EINVAL;
    }
    /* Initialize the args struct */
    memset(args, 0, sizeof(args_t));

    /* Parse Options */
    int c;
    int option_index;
    while (-1 != (c = getopt_long(argc, argv,
                    short_options, long_options, &option_index))) {
        /* this_option_optind = optind ? optind : 1; */
        option_index = 0;
        switch (c) {
            case 'f':
                /* graph filename */
                args->graph_filename = optarg;
                break;
            case 'h':
                /* print help options */
                help_requested = TRUE;
                break;
            case '?':
                break;
            default:
                fprintf(stderr, "defaul case reached...\n");
        }
    }
    if (help_requested) {
        print_help(stderr, argc, argv);
        exit(EXIT_SUCCESS);
    }
    if (args->graph_filename == NULL) {
        print_usage(stderr, argc, argv, "Please provide a graph filename.\n");
        return EINVAL;
    }
    return EXIT_SUCCESS;
}

/*
 * \brief Prints simply the usage of the program.
 *
 * @param [in] <stream> {pointer to the outgoing stream to print to
 * @param [in] <argc>   {number of arguments
 * @param [in] <argv>   {pointer to the array of string arguments
 * @param [in] <msg>    {string to print above the usage, if NULL, nothing is
 *                      printed, otherwise, the message outputs with a newline
 *                      character}
 */
#define USAGE_FMT  "usage: %s %s\n"
#define USAGE_OPTS "[-h | --help] <-f  | --file filename>"
int print_usage(FILE *stream, int argc, char **argv, char *msg) {
    if (msg) {
        fprintf(stream, "%s\n", msg);
    }
    fprintf(stream, USAGE_FMT, argv[0], USAGE_OPTS);
    return EXIT_SUCCESS;
}

/*
 * \brief Prints the short and long options with a description.
 *
 * @param [in] <stream>    {Pointer to the outgoing stream to print to}
 * @param [in] <opt_short> {Pointer to first letter in short opt. Can be NULL}
 * @param [in] <opt_long>  {Pointer to string of long option. Can be NULL}
 * @param [in] <opt_descr> {Pointer to string of description. Can be NULL}
 */
#define OPT_WIDTH 25
int print_opt(FILE *stream, char *opt_short, char *opt_long, char *opt_descr) {
    char *description = ""; /*!< initialize to empty string */

    /* Supported functionality to simply exit gracefully without printing */
    if (opt_short == NULL && opt_long == NULL && opt_descr == NULL) {
        return EXIT_SUCCESS;
    }

    /* Indent the argument */
    fprintf(stream, "\t");

    /* If provided a description, print */
    if (opt_descr) {
        description = opt_descr;
    }

    if (opt_short && opt_long) {
        /* Default short AND long args print */
        fprintf(stream, "-%c, --%-*s %s\n",
                *opt_short, OPT_WIDTH - 5, opt_long, description);
    } else {
        if (opt_short) {
            /* Short option only print */
            fprintf(stream, "-%c %-*s %s\n",
                    *opt_short, OPT_WIDTH - 2, "", description);
        } else if (opt_long) {
            /* Long option only print */
            fprintf(stream, "--%-*s %s\n", OPT_WIDTH, opt_long, description);
        }
    }
    return EXIT_SUCCESS;
}

/*
 * \brief Prints the more descriptive help text that includes the long and
 *        short args
 *
 * @param [in] <stream> {pointer to the outgoing stream to print to}
 * @param [in] <argc>   {number of arguments}
 * @param [in] <argv>   {pointer to the array of string arguments}
 */
#define USAGE_DESCR "This will do something"
int print_help(FILE *stream, int argc, char **argv) {
    print_usage(stream, argc, argv, USAGE_DESCR);
    print_opt(stream, "h", "help", "prints this help to stderr and exits");
    print_opt(stream, "f", "file filename", "the filename of the graph file to read");
    return EXIT_SUCCESS;
}
