from os import path

from setuptools import find_packages, setup

from hosting_benchmark.version import __version__

BASE_DIR = path.abspath(path.dirname(__file__))

with open(path.join(BASE_DIR, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

required_packages = [
    'click',
    'requests',
    'terminaltables',
]

extras_require = {
    "dev": ["ipython", "twine"],
    "test": ["mock", "munch", "pytest", "pytest-mock < 3.0"],
}

setup(
    name="hosting-benchmark",
    version=__version__,
    description="PHP Web-hosting benchmark",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Jakub Szafrański",
    author_email="kontakt@samu.pl",
    url="https://github.com/samupl/hosting-benchmark",
    packages=find_packages(),
    test_suite="tests",
    install_requires=required_packages,
    extras_require=extras_require,
    tests_require=extras_require["test"],
    entry_points={
        "console_scripts": [
            "hosting-benchmark = hosting_benchmark.benchmark:cli",
        ]
    },
    include_package_data=True,
)
