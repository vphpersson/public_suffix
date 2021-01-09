#!/usr/bin/env python

from asyncio import run as asyncio_run

from public_suffix import download_public_suffix_list


async def main():
    print(await download_public_suffix_list())


if __name__ == '__main__':
    asyncio_run(main())
