from setuptools import setup, find_packages

setup(
    name='fancy_rss_reader',
    version='0.2',
    description='Fancy RSS-reader',
    author='DB',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'argparse',
        'requests',
        'beautifulsoup4',
        'lxml',
        'xmltodict'
    ],
    entry_points={
        'console_scripts': ['RSS_reader=reader.rss_reader:main']
    },
    tests_require=['pytest'],
    
)