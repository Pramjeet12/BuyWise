from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = "-e ."


def get_requirements(file_path: str = "requirements.txt") -> List[str]:
    """
    Read requirements.txt and return a clean list of dependencies.
    """
    requirements: List[str] = []
    with open(file_path, "r", encoding="utf-8") as f:
        requirements = [line.strip() for line in f.readlines()]

    requirements = [req for req in requirements if req and req != HYPHEN_E_DOT]
    return requirements


setup(
    name="ShopGenie",
    version="0.0.1",
    author="Pramjeet-Kumar",
    author_email="pramjeetkumar0212@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(),
)

