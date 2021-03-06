/*
  File autogenerated by gengetopt version 2.10
  generated with the following command:
  gengetopt -i text2ngram.ggo -u -F text2ngram_cmdline 

  The developers of gengetopt consider the fixed text that goes in all
  gengetopt output files to be in the public domain:
  we make no copyright claims on it.
*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* If we use autoconf.  */
#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "getopt.h"

#include "text2ngram_cmdline.h"

void
cmdline_parser_print_version (void)
{
  printf ("%s %s\n", CMDLINE_PARSER_PACKAGE, CMDLINE_PARSER_VERSION);
}

void
cmdline_parser_print_help (void)
{
  cmdline_parser_print_version ();
  printf("\n"
  "Purpose:\n"
  "  Extract arbitrary N-Grams from raw text file. Optionally it can\n"
  "  convert a set of text streams into a ngram table file [.ngram] and generate\n"
  "  ptable index:[.ptable] for later use with `extractngram'.\n"
  "  \n"
  "  Example:\n"
  "  1. text2ngram -n3 file\n"
  "  extract all trigram from a file to stdout.\n"
  "  \n"
  "  2. text2ngram file1 file2 file3 -o corpus\n"
  "  will calculate three files into one big corpus.ngram file and\n"
  "  generate a index file (corpus.ptable) with a corpus.vocab file.\n"
  "  \n"
  "  3. text2ngram file -F gbk -T gbk -f5 -n3 -m10 -c --nopunct\n"
  "  will extract *Character* 3-gram to 10-gram with frequency > 5 from a\n"
  "  text file encoded in GBK and output ngrams in GBK encoding. All\n"
  "  ngrams with (CJK) punctuations are discarded (--nopunct)\n"
  "  \n"
  "  This program can also extract N-gram directly from in-memory ptable\n"
  "  and ltable provided that all the corpus can be fit in memory and no\n"
  "  ngram file name given (-o).  For the extraction of N-gram from large\n"
  "  corpus, considering extractngram utility.  By default, all\n"
  "  input/output encoding assume to be UTF-8.\n"
  "  \n"
  "  Note: Use mmap() for disk merging is fast but may exceed 2G memory\n"
  "  limitation on some OS (Win32) when processing large corpus (>1G). \n"
  "\n"
  "Usage: %s [OPTIONS]... [FILES]...\n", CMDLINE_PARSER_PACKAGE);
  printf("   -h         --help           Print help and exit\n");
  printf("   -V         --version        Print version and exit\n");
  printf("   -FSTRING   --from=STRING    input stream encoding (for character ngram only) (default='UTF-8')\n");
  printf("   -TSTRING   --to=STRING      output stream encoding (for character ngram only) (default='UTF-8')\n");
  printf("   -oSTRING   --output=STRING  ngram file name\n");
  printf("   -MINT      --mem=INT        size of memory(MB) to use (default='50')\n");
  printf("   -c         --char           counting char ngram (default=off)\n");
  printf("              --mmap           use mmap() for disk merging (default=off)\n");
  printf("   -nINT      --min-n=INT      extract N gram (where N >= n)\n");
  printf("   -mINT      --max-n=INT      extract N gram (N <= m) (max M=255,M=N if omitted)\n");
  printf("   -fINT      --freq=INT       extract N gram whose freq >= f (default='1')\n");
  printf("              --nopunct        exclude N gram with punctuations and special symbols (non-word) (default=off)\n");
  printf("   -wINT      --wordlen=INT    average word length when count word ngrams.this option is a hint for pre-allocate memory (default='3')\n");
}


static char *gengetopt_strdup (const char *s);

/* gengetopt_strdup() */
/* strdup.c replacement of strdup, which is not standard */
char *
gengetopt_strdup (const char *s)
{
  char *result = (char*)malloc(strlen(s) + 1);
  if (result == (char*)0)
    return (char*)0;
  strcpy(result, s);
  return result;
}

int
cmdline_parser (int argc, char * const *argv, struct gengetopt_args_info *args_info)
{
  int c;	/* Character of the parsed option.  */
  int missing_required_options = 0;

  args_info->help_given = 0 ;
  args_info->version_given = 0 ;
  args_info->from_given = 0 ;
  args_info->to_given = 0 ;
  args_info->output_given = 0 ;
  args_info->mem_given = 0 ;
  args_info->char_given = 0 ;
  args_info->mmap_given = 0 ;
  args_info->min_n_given = 0 ;
  args_info->max_n_given = 0 ;
  args_info->freq_given = 0 ;
  args_info->nopunct_given = 0 ;
  args_info->wordlen_given = 0 ;
#define clear_args() { \
  args_info->from_arg = gengetopt_strdup("UTF-8") ;\
  args_info->to_arg = gengetopt_strdup("UTF-8") ;\
  args_info->output_arg = NULL; \
  args_info->mem_arg = 50 ;\
  args_info->char_flag = 0;\
  args_info->mmap_flag = 0;\
  args_info->freq_arg = 1 ;\
  args_info->nopunct_flag = 0;\
  args_info->wordlen_arg = 3 ;\
}

  clear_args();

  args_info->inputs = NULL;
  args_info->inputs_num = 0;

  optarg = 0;
  optind = 1;
  opterr = 1;
  optopt = '?';

  while (1)
    {
      int option_index = 0;
      char *stop_char;

      static struct option long_options[] = {
        { "help",	0, NULL, 'h' },
        { "version",	0, NULL, 'V' },
        { "from",	1, NULL, 'F' },
        { "to",	1, NULL, 'T' },
        { "output",	1, NULL, 'o' },
        { "mem",	1, NULL, 'M' },
        { "char",	0, NULL, 'c' },
        { "mmap",	0, NULL, 0 },
        { "min-n",	1, NULL, 'n' },
        { "max-n",	1, NULL, 'm' },
        { "freq",	1, NULL, 'f' },
        { "nopunct",	0, NULL, 0 },
        { "wordlen",	1, NULL, 'w' },
        { NULL,	0, NULL, 0 }
      };

      stop_char = 0;
      c = getopt_long (argc, argv, "hVF:T:o:M:cn:m:f:w:", long_options, &option_index);

      if (c == -1) break;	/* Exit from `while (1)' loop.  */

      switch (c)
        {
        case 'h':	/* Print help and exit.  */
          clear_args ();
          cmdline_parser_print_help ();
          exit (EXIT_SUCCESS);

        case 'V':	/* Print version and exit.  */
          clear_args ();
          cmdline_parser_print_version ();
          exit (EXIT_SUCCESS);

        case 'F':	/* input stream encoding (for character ngram only).  */
          if (args_info->from_given)
            {
              fprintf (stderr, "%s: `--from' (`-F') option given more than once\n", CMDLINE_PARSER_PACKAGE);
              clear_args ();
              exit (EXIT_FAILURE);
            }
          args_info->from_given = 1;
          args_info->from_arg = gengetopt_strdup (optarg);
          break;

        case 'T':	/* output stream encoding (for character ngram only).  */
          if (args_info->to_given)
            {
              fprintf (stderr, "%s: `--to' (`-T') option given more than once\n", CMDLINE_PARSER_PACKAGE);
              clear_args ();
              exit (EXIT_FAILURE);
            }
          args_info->to_given = 1;
          args_info->to_arg = gengetopt_strdup (optarg);
          break;

        case 'o':	/* ngram file name.  */
          if (args_info->output_given)
            {
              fprintf (stderr, "%s: `--output' (`-o') option given more than once\n", CMDLINE_PARSER_PACKAGE);
              clear_args ();
              exit (EXIT_FAILURE);
            }
          args_info->output_given = 1;
          args_info->output_arg = gengetopt_strdup (optarg);
          break;

        case 'M':	/* size of memory(MB) to use.  */
          if (args_info->mem_given)
            {
              fprintf (stderr, "%s: `--mem' (`-M') option given more than once\n", CMDLINE_PARSER_PACKAGE);
              clear_args ();
              exit (EXIT_FAILURE);
            }
          args_info->mem_given = 1;
          args_info->mem_arg = strtol (optarg,&stop_char,0);
          break;

        case 'c':	/* counting char ngram.  */
          if (args_info->char_given)
            {
              fprintf (stderr, "%s: `--char' (`-c') option given more than once\n", CMDLINE_PARSER_PACKAGE);
              clear_args ();
              exit (EXIT_FAILURE);
            }
          args_info->char_given = 1;
          args_info->char_flag = !(args_info->char_flag);
          break;

        case 'n':	/* extract N gram (where N >= n).  */
          if (args_info->min_n_given)
            {
              fprintf (stderr, "%s: `--min-n' (`-n') option given more than once\n", CMDLINE_PARSER_PACKAGE);
              clear_args ();
              exit (EXIT_FAILURE);
            }
          args_info->min_n_given = 1;
          args_info->min_n_arg = strtol (optarg,&stop_char,0);
          break;

        case 'm':	/* extract N gram (N <= m) (max M=255,M=N if omitted).  */
          if (args_info->max_n_given)
            {
              fprintf (stderr, "%s: `--max-n' (`-m') option given more than once\n", CMDLINE_PARSER_PACKAGE);
              clear_args ();
              exit (EXIT_FAILURE);
            }
          args_info->max_n_given = 1;
          args_info->max_n_arg = strtol (optarg,&stop_char,0);
          break;

        case 'f':	/* extract N gram whose freq >= f.  */
          if (args_info->freq_given)
            {
              fprintf (stderr, "%s: `--freq' (`-f') option given more than once\n", CMDLINE_PARSER_PACKAGE);
              clear_args ();
              exit (EXIT_FAILURE);
            }
          args_info->freq_given = 1;
          args_info->freq_arg = strtol (optarg,&stop_char,0);
          break;

        case 'w':	/* average word length when count word ngrams.this option is a hint for pre-allocate memory.  */
          if (args_info->wordlen_given)
            {
              fprintf (stderr, "%s: `--wordlen' (`-w') option given more than once\n", CMDLINE_PARSER_PACKAGE);
              clear_args ();
              exit (EXIT_FAILURE);
            }
          args_info->wordlen_given = 1;
          args_info->wordlen_arg = strtol (optarg,&stop_char,0);
          break;


        case 0:	/* Long option with no short option */
          /* use mmap() for disk merging.  */
          if (strcmp (long_options[option_index].name, "mmap") == 0)
          {
            if (args_info->mmap_given)
              {
                fprintf (stderr, "%s: `--mmap' option given more than once\n", CMDLINE_PARSER_PACKAGE);
                clear_args ();
                exit (EXIT_FAILURE);
              }
            args_info->mmap_given = 1;
            args_info->mmap_flag = !(args_info->mmap_flag);
            break;
          }
          
          /* exclude N gram with punctuations and special symbols (non-word).  */
          else if (strcmp (long_options[option_index].name, "nopunct") == 0)
          {
            if (args_info->nopunct_given)
              {
                fprintf (stderr, "%s: `--nopunct' option given more than once\n", CMDLINE_PARSER_PACKAGE);
                clear_args ();
                exit (EXIT_FAILURE);
              }
            args_info->nopunct_given = 1;
            args_info->nopunct_flag = !(args_info->nopunct_flag);
            break;
          }
          

        case '?':	/* Invalid option.  */
          /* `getopt_long' already printed an error message.  */
          exit (EXIT_FAILURE);

        default:	/* bug: option not considered.  */
          fprintf (stderr, "%s: option unknown: %c\n", CMDLINE_PARSER_PACKAGE, c);
          abort ();
        } /* switch */
    } /* while */


  if ( missing_required_options )
    exit (EXIT_FAILURE);

  if (optind < argc)
    {
      int i = 0 ;
  
      args_info->inputs_num = argc - optind ;
      args_info->inputs = 
        (char **)(malloc ((args_info->inputs_num)*sizeof(char *))) ;
      while (optind < argc)
        args_info->inputs[ i++ ] = gengetopt_strdup (argv[optind++]) ; 
    }
  
  return 0;
}
