from setuptools import setup, find_packages

setup(
    name='RSS_reader',
    version='0.2',
    description='Fancy RSS-reader',
    author='DB',
    packages=find_packages(include=['reader'],
                           exclude=['reader.tests']),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'lxml',
        'xmltodict'
    ],
    entry_points={
        'console_scripts': ['RSS_reader=reader.rss_reader:main']
    },
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    
)