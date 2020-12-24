from dataclasses import dataclass
from typing import Optional, Union, cast

from public_suffix.trie import PublicSuffixListTrieNode


@dataclass
class DomainProperties:
    effective_top_level_domain: str
    registered_domain: str
    subdomain: str


def get_domain_properties(root_node: PublicSuffixListTrieNode, domain: str) -> DomainProperties:
    """
    Retrieves properties of a domain name using the public suffix list.

    :param root_node: The root node of the trie storing the public suffix list information.
    :param domain: The domain name about which to retrieve properties.
    :return: Properties of the provided domain.
    """

    dns_name_components: list[str] = domain.lower().split('.')

    match_map: list[Union[bool, None]] = [None] * len(dns_name_components)

    def traverse_node(node: PublicSuffixListTrieNode, depth: int = 1) -> None:
        if depth == 1:
            # "If no rules match, the prevailing rule is "*""
            match_map[-depth] = False

        for name in {'*', dns_name_components[-depth]}:
            next_node = cast(Optional[PublicSuffixListTrieNode], node.key_to_child.get(name))
            if next_node is None:
                continue

            match_map[-depth] = next_node.negate
            if depth == len(dns_name_components):
                return

            traverse_node(node=next_node, depth=depth + 1)

    traverse_node(node=root_node)

    hit_index = match_map.index(False)

    effective_top_level_domain = '.'.join(dns_name_components[hit_index:])
    return DomainProperties(
        effective_top_level_domain=effective_top_level_domain,
        registered_domain=(
            registered_domain
            if (registered_domain := '.'.join(dns_name_components[hit_index-1:])) != effective_top_level_domain
            else ''
        ),
        subdomain='.'.join(dns_name_components[:hit_index-1])
    )
