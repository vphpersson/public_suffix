from __future__ import annotations
from typing import Iterable, TextIO
from pathlib import Path

from public_suffix.structures.public_suffix_list_trie_node import PublicSuffixListTrieNode
from public_suffix.structures.domain_properties import DomainProperties
from public_suffix import get_domain_properties


class PublicSuffixListTrie:
    def __init__(self, root_node: PublicSuffixListTrieNode):
        self._root_node: PublicSuffixListTrieNode = root_node

    def get_domain_properties(self, domain: str) -> DomainProperties | None:
        return get_domain_properties(root_node=self._root_node, domain=domain)

    @classmethod
    def from_public_suffix_list(cls, rules: Iterable[str]) -> PublicSuffixListTrie:
        return cls(
            root_node=PublicSuffixListTrieNode.from_public_suffix_list(rules=rules)
        )

    @classmethod
    def from_public_suffix_list_file(cls, file: TextIO | Path) -> PublicSuffixListTrie:
        return cls(
            root_node=PublicSuffixListTrieNode.from_public_suffix_list_file(file=file)
        )

