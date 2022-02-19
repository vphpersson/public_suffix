from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Iterable, TextIO
from functools import partial


@dataclass
class TrieNode:
    key_to_child: dict[str, TrieNode] = field(default_factory=dict)


@dataclass
class PublicSuffixListTrieNode(TrieNode):
    dns_name_component: str = ''
    negate: bool = False

    @classmethod
    def from_public_suffix_list(cls, rules: Iterable[str]) -> PublicSuffixListTrieNode:
        root_node = cls()

        for rule in rules:
            if rule.startswith('!'):
                negate = True
                dns_name = rule[1:]
            else:
                negate = False
                dns_name = rule

            current_node = root_node
            for dns_name_component in dns_name.split('.')[::-1]:
                next_node = current_node.key_to_child.setdefault(dns_name_component, PublicSuffixListTrieNode())
                next_node.dns_name_component = dns_name_component

                current_node = next_node

            # The last current node is the leaf node corresponding to the DNS name of the rule.
            current_node.negate = negate

        return root_node

    @classmethod
    def from_public_suffix_list_file(cls, file: TextIO) -> PublicSuffixListTrieNode:
        return PublicSuffixListTrieNode.from_public_suffix_list(
            rules=(
                stripped_line.encode(encoding='idna').decode()
                for line in file
                if (stripped_line := line.strip()) and not stripped_line.startswith('//')
            )
        )


class PublicSuffixListTrie:
    def __init__(self, root_node: PublicSuffixListTrieNode):
        from public_suffix import get_domain_properties

        self.get_domain_properties = partial(get_domain_properties, root_node=root_node)
