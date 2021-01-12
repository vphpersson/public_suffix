# public_suffix

Obtain properties about a domain name using the [Public Suffix List](https://publicsuffix.org/).

The properties include
- The effective top-level domain (eTLD)
- The registered domain
- The subdomain

The list file is either provided to the program or downloaded by the program.
The rules constituting the list are collected in a [trie](https://en.wikipedia.org/wiki/Trie).

## Usage

```
usage: public_suffix.py [-h] [--domain-names-file DOMAIN_NAMES_FILE] [--list-file-path LIST_FILE_PATH] [--json] [domain_name]

Obtain properties about a domain name using the Public Suffix list.

positional arguments:
  domain_name           A domain name about which to retrieve information.

optional arguments:
  -h, --help            show this help message and exit
  --domain-names-file DOMAIN_NAMES_FILE
                        A path of a file storing domain names about which to retrieve information.
  --list-file-path LIST_FILE_PATH
                        A path of a file storing the Public Suffix List.
  --json                Whether to output the domain properties in JSON.

If no domain name or file path is provided, input is read from standard input (stdin). If no public suffix list file path is provided, the list is downloaded.
```

### Examples

#### Domain name as a positional argument

```shell
$ ./public_suffix.py --list-file-path public_suffix_list.dat 'www.example.co.uk'
```

Output:
```
Effective top-level domain (eTLD): co.uk
                Registered domain: example.co.uk
                        Subdomain: www
```

#### Multiple domain names from a file, output in JSON

```shell
$ ./public_suffix.py --list-file-path public_suffix_list.dat --domain-names-file /tmp/domain_names --json
```

Output:
```json
[{"effective_top_level_domain": "org", "registered_domain": "python.org", "subdomain": "docs"}, {"effective_top_level_domain": "co.uk", "registered_domain": "example.co.uk", "subdomain": "www"}, {"effective_top_level_domain": "se", "registered_domain": "sweden.se", "subdomain": "www"}]
```

:thumbsup:
