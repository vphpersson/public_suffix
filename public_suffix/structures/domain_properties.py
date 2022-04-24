from dataclasses import dataclass


@dataclass
class DomainProperties:
    effective_top_level_domain: str
    registered_domain: str
    subdomain: str

    def __str__(self) -> str:
        return (
            f'Effective top-level domain (eTLD): {self.effective_top_level_domain}\n'
            f'Registered domain: {self.registered_domain}\n'
            f'Subdomain: {self.subdomain}'
        )
