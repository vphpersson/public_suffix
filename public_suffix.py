#!/usr/bin/env python

from asyncio import run as asyncio_run
from dataclasses import asdict
from json import dumps as json_dumps
from sys import stdin
from typing import Type

from string_utils_py import text_align_delimiter

from public_suffix.cli import PublicSuffixArgumentParser
from public_suffix import download_public_suffix_list
from public_suffix.structures.public_suffix_list_trie import PublicSuffixListTrie
from public_suffix.structures.domain_properties import DomainProperties


async def main():
    args: Type[PublicSuffixArgumentParser.Namespace] = PublicSuffixArgumentParser().parse_args()

    public_suffix_list_trie = PublicSuffixListTrie.from_public_suffix_list(
        rules=(
            args.list_file_path.read() if args.list_file_path else (await download_public_suffix_list())
        ).splitlines()
    )

    domain_properties_list: list[DomainProperties] = [
        public_suffix_list_trie.get_domain_properties(domain=domain_name.strip())
        for domain_name in (args.domain_names or stdin)
    ]

    print(
        json_dumps([
            (asdict(domain_properties) if domain_properties is not None else None)
            for domain_properties in domain_properties_list
        ]) if args.json else '\n\n'.join(
            (text_align_delimiter(text=str(domain_properties)) if domain_properties is not None else 'None')
            for domain_properties in domain_properties_list
        )
    )


if __name__ == '__main__':
    asyncio_run(main())
