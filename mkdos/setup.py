from setuptools import setup, find_packages

setup(
    name='mkdos',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'scapy',
        'requests',
        'progressbar2',
    ],
    entry_points={
        'console_scripts': [
            'mkdos=mkdos.mkdos:main',
        ],
    },
)