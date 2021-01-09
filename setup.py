from setuptools import setup, find_packages

setup(
    name='public_suffix',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'httpx',
        'pyutils @ git+ssh://git@github.com/vphpersson/pyutils.git#egg=pyutils'
    ]
)
