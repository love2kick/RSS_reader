from setuptools import setup, find_packages

setup(
    name='RSS_reader',
    version='0.2',
    description='Fancy RSS-reader',
    author='DB',
    package_dir={'':'src'},
    packages=find_packages(include=['src', 'src.*']),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'lxml',
        'xmltodict'
    ],
    entry_points={
        'console_scripts': ['RSS_reader=src.rss_reader']
    },
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    
)