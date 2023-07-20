from typing import Type

from public_suffix.structures.domain_properties import DomainProperties
from public_suffix.structures.public_suffix_list_trie_node import PublicSuffixListTrieNode


try:
    from httpx import AsyncClient
except ImportError:
    AsyncClient = Type[None]


PUBLIC_SUFFIX_LIST_URL = 'https://publicsuffix.org/list/public_suffix_list.dat'


def get_domain_properties(root_node: PublicSuffixListTrieNode, domain: str) -> DomainProperties | None:
    """
    Retrieves properties of a domain name using the public suffix list.

    :param root_node: The root node of the trie storing the public suffix list information.
    :param domain: The domain name about which to retrieve properties.
    :return: Properties of the provided domain.
    """

    dns_name_components: list[str] = domain.lower().split('.')

    match_map: list[bool | None] = [None] * len(dns_name_components)

    def traverse_node(node: PublicSuffixListTrieNode, depth: int = 1) -> None:
        if depth == 1:
            # "If no rules match, the prevailing rule is "*""
            match_map[-depth] = False

        for name in {'*', dns_name_components[-depth]}:
            next_node: PublicSuffixListTrieNode | None = node.key_to_child.get(name)
            if next_node is None:
                continue

            match_map[-depth] = next_node.negate

            if depth == len(dns_name_components):
                return

            traverse_node(node=next_node, depth=depth + 1)

    traverse_node(node=root_node)

    hit_index = match_map.index(False)

    effective_top_level_domain: str = '.'.join(dns_name_components[hit_index:])
    registered_domain: str = '.'.join(dns_name_components[hit_index - 1:])

    if effective_top_level_domain not in root_node.key_to_child and registered_domain == effective_top_level_domain:
        return None

    return DomainProperties(
        effective_top_level_domain=effective_top_level_domain,
        registered_domain=registered_domain,
        subdomain='.'.join(dns_name_components[:hit_index - 1])
    )


async def _download_public_suffix_list(http_client: AsyncClient) -> str:
    response = await http_client.get(PUBLIC_SUFFIX_LIST_URL)
    response.raise_for_status()

    return response.text


async def download_public_suffix_list(http_client: AsyncClient | None = None) -> str:
    """
    Download the Public Suffix List.

    :param http_client: An HTTP client with which to retrieve the Public Suffix List.
    :return: The Public Suffix List as string.
    """

    if not http_client:
        async with AsyncClient() as http_client:
            return await _download_public_suffix_list(http_client=http_client)
    else:
        return await _download_public_suffix_list(http_client=http_client)
