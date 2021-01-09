#!/usr/bin/env python

from asyncio import run as asyncio_run
from argparse import ArgumentParser, FileType, Action, Namespace
from typing import Optional
from re import compile as re_compile
from dataclasses import asdict
from json import dumps as json_dumps
from io import TextIOWrapper

from pyutils.my_string import text_align_delimiter

from public_suffix import download_public_suffix_list, DomainProperties
from public_suffix.trie import PublicSuffixListTrie, PublicSuffixListTrieNode


class PublicSuffixArgumentParser(ArgumentParser):

    _FQDN_PATTERN = re_compile(pattern=r'^([a-zA-Z0-9._-])+$')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fqdn_input_group = self.add_mutually_exclusive_group(required=True)

        fqdn_input_group.add_argument(
            '--fqdn',
            help='A fully-qualified domain name about which to retrieve information.',
            action=self._ParseFQDNAction
        )

        fqdn_input_group.add_argument(
            '--fqdns-file',
            help='A path of a file storing FQDNs.',
            type=FileType('r', encoding='utf-8'),
            action=self._ParseFQDNFileAction
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

    class _ParseFQDNAction(Action):
        def __call__(
            self,
            parser: ArgumentParser,
            namespace: Namespace,
            fqdn: str,
            option_string: Optional[str] = None
        ):
            """Check if an input fully-qualified domain name is in the correct format."""

            fqdns: set[str] = getattr(namespace, 'fqdns', set())

            if not PublicSuffixArgumentParser._FQDN_PATTERN.search(string=fqdn):
                parser.error(message=f'The input FQDN is not in the correct format.')

            fqdns.add(fqdn)

            setattr(namespace, self.dest, fqdn)
            setattr(namespace, 'fqdns', fqdns)

    class _ParseFQDNFileAction(Action):
        def __call__(
            self,
            parser: ArgumentParser,
            namespace: Namespace,
            fqdns_file: TextIOWrapper,
            option_string: Optional[str] = None
        ):
            fqdns: set[str] = getattr(namespace, 'fqdns', set())

            for fqdn in fqdns_file.read().splitlines():
                if not PublicSuffixArgumentParser._FQDN_PATTERN.search(string=fqdn):
                    parser.error(message=f'The input FQDN is not in the correct format.')

                fqdns.add(fqdn)

            setattr(namespace, self.dest, fqdns_file)
            setattr(namespace, 'fqdns', fqdns)


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
        public_suffix_list_trie.get_domain_properties(domain=fqdn)
        for fqdn in args.fqdns
    ]

    print(
        json_dumps([asdict(domain_properties) for domain_properties in domain_properties_list])if args.json
        else '\n\n'.join(text_align_delimiter(text=str(domain_properties)) for domain_properties in domain_properties_list)
    )


if __name__ == '__main__':
    asyncio_run(main())
