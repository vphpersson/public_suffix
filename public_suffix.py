#!/usr/bin/env python

from asyncio import run as asyncio_run
from argparse import ArgumentParser, FileType, Action, Namespace
from typing import Optional
from re import compile as re_compile
from dataclasses import asdict
from json import dumps as json_dumps
from io import TextIOWrapper
from sys import stdin

from pyutils.my_string import text_align_delimiter

from public_suffix import download_public_suffix_list, DomainProperties
from public_suffix.trie import PublicSuffixListTrie, PublicSuffixListTrieNode


class PublicSuffixArgumentParser(ArgumentParser):

    _DOMAIN_NAME_PATTERN = re_compile(pattern=r'^([a-zA-Z0-9._-])+$')

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            description='Obtain properties about a domain name using the Public Suffix list.',
            epilog=(
                'If no domain name or file path is provided, input is read from standard input (stdin). '
                'If no public suffix list file path is provided, the list is downloaded.'
            ),
            **kwargs
        )

        self.add_argument(
            'domain_name',
            help='A domain name about which to retrieve information.',
            action=self._ParseDomainNameAction,
            nargs='?'
        )

        self.add_argument(
            '--domain-names-file',
            help='A path of a file storing domain names about which to retrieve information.',
            type=FileType('r', encoding='utf-8'),
            action=self._ParseDomainNamesFileAction
        )

        self.add_argument(
            '--list-file-path',
            help='A path of a file storing the Public Suffix List.',
            type=FileType('r', encoding='utf-8')
        )

        self.add_argument(
            '--json',
            help='Whether to output the domain properties in JSON.',
            action='store_true'
        )

    class _ParseDomainNameAction(Action):
        def __call__(
            self,
            parser: ArgumentParser,
            namespace: Namespace,
            domain_name: Optional[str],
            option_string: Optional[str] = None
        ):
            """Check if an input fully-qualified domain name is in the correct format."""

            domain_names: set[str] = getattr(namespace, 'domain_names', set())

            if domain_name is not None:
                if not PublicSuffixArgumentParser._DOMAIN_NAME_PATTERN.search(string=domain_name):
                    parser.error(message=f'The input domain name is not in the correct format: {domain_name}')

                domain_names.add(domain_name)

            setattr(namespace, self.dest, domain_name)
            setattr(namespace, 'domain_names', domain_names)

    class _ParseDomainNamesFileAction(Action):
        def __call__(
            self,
            parser: ArgumentParser,
            namespace: Namespace,
            domain_names_file: TextIOWrapper,
            option_string: Optional[str] = None
        ):
            domain_names: set[str] = getattr(namespace, 'domain_names', set())

            for line_number, domain_name in enumerate(domain_names_file.read().splitlines(), start=1):
                if not PublicSuffixArgumentParser._DOMAIN_NAME_PATTERN.search(string=domain_name):
                    parser.error(message=f'An input domain name is not in the correct format ({domain_names_file.name}:{line_number}): {domain_name}')

                domain_names.add(domain_name)

            setattr(namespace, self.dest, domain_names_file)
            setattr(namespace, 'domain_names', domain_names)


async def main():
    args = PublicSuffixArgumentParser().parse_args()

    public_suffix_list_trie = PublicSuffixListTrie(
        root_node=PublicSuffixListTrieNode.from_public_suffix_list(
            rules=(
                args.list_file_path.read() if args.list_file_path else (await download_public_suffix_list())
            ).splitlines()
        )
    )

    domain_properties_list: list[DomainProperties] = [
        public_suffix_list_trie.get_domain_properties(domain=domain_name.strip())
        for domain_name in (args.domain_names or stdin)
    ]

    print(
        json_dumps([asdict(domain_properties) for domain_properties in domain_properties_list])if args.json
        else '\n\n'.join(text_align_delimiter(text=str(domain_properties)) for domain_properties in domain_properties_list)
    )


if __name__ == '__main__':
    asyncio_run(main())
