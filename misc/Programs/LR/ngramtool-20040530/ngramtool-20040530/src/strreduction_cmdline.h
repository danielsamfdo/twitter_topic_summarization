/* strreduction_cmdline.h */

/* File autogenerated by gengetopt version 2.10  */

#ifndef STRREDUCTION_CMDLINE_H
#define STRREDUCTION_CMDLINE_H

/* If we use autoconf.  */
#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#ifndef CMDLINE_PARSER_PACKAGE
#define CMDLINE_PARSER_PACKAGE "strreduction"
#endif

#ifndef CMDLINE_PARSER_VERSION
#define CMDLINE_PARSER_VERSION ""
#endif

struct gengetopt_args_info
{
  char * from_arg;	/* input stream encoding (for character ngram only) (default='UTF-8').  */
  char * to_arg;	/* output stream encoding (for character ngram only) (default='UTF-8').  */
  char * output_arg;	/* write output to file,use stdout if omitted.  */
  int algorithm_arg;	/* using Nth reduction algorithm (default='2').  */
  int char_flag;	/* enter char gram mode, default is word ngram model (default=off).  */
  int sort_flag;	/* sort result (default=off).  */
  int time_flag;	/* show time cost by reduction algorithm on stderr (not including I/O) (default=off).  */
  int freq_arg;	/* frequence threshold needed in algorithm 1,2,4 (default='1').  */
  int m1_arg;	/* minimum n-gram need in algorithm 4 (default='1').  */

  int help_given ;	/* Whether help was given.  */
  int version_given ;	/* Whether version was given.  */
  int from_given ;	/* Whether from was given.  */
  int to_given ;	/* Whether to was given.  */
  int output_given ;	/* Whether output was given.  */
  int algorithm_given ;	/* Whether algorithm was given.  */
  int char_given ;	/* Whether char was given.  */
  int sort_given ;	/* Whether sort was given.  */
  int time_given ;	/* Whether time was given.  */
  int freq_given ;	/* Whether freq was given.  */
  int m1_given ;	/* Whether m1 was given.  */

  char **inputs ; /* unamed options */
  unsigned inputs_num ; /* unamed options number */
} ;

int cmdline_parser (int argc, char * const *argv, struct gengetopt_args_info *args_info);

void cmdline_parser_print_help(void);
void cmdline_parser_print_version(void);

#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* STRREDUCTION_CMDLINE_H */