from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterable, TextIO, Optional
from pathlib import Path

from public_suffix import DomainProperties


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
    def from_public_suffix_list_file(cls, file: TextIO | Path) -> PublicSuffixListTrieNode:

        lines_iter: Iterable[str] = file.read_text().splitlines() if isinstance(file, Path) else file

        return PublicSuffixListTrieNode.from_public_suffix_list(
            rules=(
                stripped_line.encode(encoding='idna').decode()
                for line in lines_iter
                if (stripped_line := line.strip()) and not stripped_line.startswith('//')
            )
        )


class PublicSuffixListTrie:
    def __init__(self, root_node: PublicSuffixListTrieNode):
        self._root_node: PublicSuffixListTrieNode = root_node

    def get_domain_properties(self, domain: str) -> Optional[DomainProperties]:
        from public_suffix import get_domain_properties

        return get_domain_properties(root_node=self._root_node, domain=domain)
