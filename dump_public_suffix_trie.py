#!/usr/bin/env python

from asyncio import run as asyncio_run
from typing import Type
from json import dumps as json_dumps
from dataclasses import asdict

from public_suffix.cli import DumpPublicSuffixTrieArgumentParser
from public_suffix import download_public_suffix_list
from public_suffix.structures.public_suffix_list_trie_node import PublicSuffixListTrieNode


async def main():

    args: Type[DumpPublicSuffixTrieArgumentParser.Namespace] = DumpPublicSuffixTrieArgumentParser().parse_args()

    print(
        json_dumps(
            asdict(
                PublicSuffixListTrieNode.from_public_suffix_list(
                    rules=(
                        args.list_file_path.read() if args.list_file_path else (await download_public_suffix_list())
                    ).splitlines()
                )
            )
        )
    )

if __name__ == '__main__':
    asyncio_run(main())
