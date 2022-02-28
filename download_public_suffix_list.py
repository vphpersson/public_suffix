#!/usr/bin/env python

from asyncio import run as asyncio_run

from public_suffix.cli import DownloadPublicSuffixListArgumentParser
from public_suffix import download_public_suffix_list


async def main():
    DownloadPublicSuffixListArgumentParser().parse_args()
    print(await download_public_suffix_list())


if __name__ == '__main__':
    asyncio_run(main())
