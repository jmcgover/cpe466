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
static char     short_options[] = "f:h:NLSHQ";
static struct   option long_options[] = {
    {"file",    required_argument, NULL, 'f'},
    {"help",    no_argument, NULL, 'h'},
    {"NUM",     no_argument, NULL, 'N'},
    {"LABEL",   no_argument, NULL, 'L'},
    {"SNAP",    no_argument, NULL, 'S'},
    {"HANDLE",  no_argument, NULL, 'H'},
    {"QUIET",   no_argument, NULL, 'Q'},
    {0, 0, 0, 0}
};
int parse_args(int argc, char **argv, args_t *args) {
    int help_requested = FALSE;
    if (args == NULL) {
        return EINVAL;
    }
    /* Initialize the args struct */
    memset(args, 0, sizeof(args_t));
    args->type = NONE;

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
            case 'N':
                /* NUM type graph */
                args->type = NUM;
                break;
            case 'L':
                /* LABEL type graph */
                args->type = LABEL;
                break;
            case 'S':
                /* SNAP type graph */
                args->type = SNAP;
                break;
            case 'H':
                /* QUIET type graph */
                args->type = HANDLE;
                break;
            case 'Q':
                /* QUIET type graph */
                args->type = QUIET;
                break;
            case '?':
                break;
            default:
                fprintf(stderr, "default case reached...\n");
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
#define USAGE_OPTS "[-h | --help] [-N | -L | -S] <-f  | --file filename>"
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
    fprintf(stream, "By default, the graph file is loaded and printed.\n");
    fprintf(stream, "The following mutually exclusive options will \
                     interpret and store the graph accordingly: \n");
    print_opt(stream, "N", "NUM", "graph has numbered nodes");
    print_opt(stream, "L", "LABEL", "graph has labeled nodes");
    print_opt(stream, "S", "SNAP", "graph is from the SNAP dataset");
    print_opt(stream, "H", "HANDLE", "uses the supplied handler to parse the line");
    print_opt(stream, "Q", "QUIET", "same as default but without printing");
    return EXIT_SUCCESS;
}
