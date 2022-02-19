#!/usr/bin/env python

from asyncio import run as asyncio_run
from argparse import ArgumentParser, FileType
from json import dumps as json_dumps
from dataclasses import asdict

from public_suffix import download_public_suffix_list
from public_suffix.trie import PublicSuffixListTrieNode


class DumpPublicSuffixTrieArgumentParser(ArgumentParser):

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **(
                dict(
                    description='Dump a Trie representation of the Public Suffix list in JSON.'
                ) | kwargs
            )
        )

        self.add_argument(
            'list_file_path',
            help='A path of a file storing the Public Suffix List',
            nargs='?',
            type=FileType('r', encoding='utf-8')
        )


async def main():

    args = DumpPublicSuffixTrieArgumentParser().parse_args()

    print(
        json_dumps(
            asdict(
                PublicSuffixListTrieNode.from_public_suffix_list(
                    rules=(
                        stripped_line.encode(encoding='idna').decode()
                        for line in (args.list_file_path.read() if args.list_file_path else (await download_public_suffix_list())).splitlines()
                        if (stripped_line := line.strip()) and not stripped_line.startswith('//')
                    )
                )
            )
        )
    )

if __name__ == '__main__':
    asyncio_run(main())
