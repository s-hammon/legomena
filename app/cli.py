import argparse

from main import zipf_command

def main():
    parser = argparse.ArgumentParser(
        prog="lego",
        description="A CLI for (simple) analysis of text corpora. Incorporates Zipf's Law, Chi-Square tests, and ratio of words used only once, twice, thrice, and so on."
    )

    subparsers = parser.add_subparsers(dest="command")

    def add_common_args(subparser):
        group = subparser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            "--file", "-f",
            help="The path to the text file to analyze",
        )
        group.add_argument(
            "--config", "-c",
            help="The path to the configuration file (must be YAML or JSON)",
        )
        subparser.add_argument(
            "--combine", type=bool, default=False,
            help="Combine the text from multiple files into a single corpus. Can only be used with --config",
        )
        subparser.add_argument(
            "--from-gutenberg", type=bool, default=False,
            help="If the text is from Project Gutenberg. Lego will remove header/footer text. Can only be used with --file",
        )

    zipf_parser = subparsers.add_parser("zipf", help="Analyze the text according to Zipf's Law")
    add_common_args(zipf_parser)

    wordcount_parser = subparsers.add_parser("wordcount", help="Get word dictionary of the text, and teh count of each word that appears.")
    add_common_args(wordcount_parser)

    args = parser.parse_args()
    if args.combine and not args.config:
        raise ValueError("--combine flag can only be used with --config")
    if args.from_gutenberg and not args.file:
        raise ValueError("--from-gutenberg flag can only be used with --file")

    if args.command == "zipf":
        zipf_command(**vars(args))
    elif args.command == "wordcount":
        raise NotImplementedError("Wordcount is not yet implemented.")
    else:
        parser.print_help()


main()