from setuptools import setup, find_packages

setup(
    name='rss_reader',
    version='0.2',
    packages=find_packages(include=['main', 'main.*']),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'lxml',
        'xmltodict'
    ],
    entry_points={
        'console_scripts': ['rss_reader=main.rss_reader']
    },
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    
)