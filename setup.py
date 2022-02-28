from setuptools import setup, find_packages

setup(
    name='public_suffix',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'httpx',
        'string_utils_py @ git+https://github.com/vphpersson/string_utils_py.git#egg=string_utils_py'
    ]
)
