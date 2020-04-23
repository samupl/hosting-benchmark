from setuptools import find_packages, setup

from hosting_benchmark.version import __version__

required_packages = [
    'click',
    'requests',
]

extras_require = {
    "dev": ["ipython", "twine"],
    "test": ["mock", "munch", "pytest", "pytest-mock < 3.0"],
}

setup(
    name="hosting-benchmark",
    version=__version__,
    description="PHP Web-hosting benchmark",
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
)
