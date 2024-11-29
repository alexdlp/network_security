"""
The setup.py file is an essential part of packaging and distributing python projects

It is used by setuptools (or distutils in older python versions) to define the configuration of your proyect, such as its metadata, dependencies and more...

the use of setup.py has been replaced in some cases by pyproject.toml, a standard file for building packages, introduced in PEP518. implement in the future
"""

from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str]:
    """Returns the list of requirements
    """

    requirement_list: List[str]=[]

    try: 
        with open('requirements.txt', 'r') as file:

            lines = file.readlines()

            for line in lines:
                requirement = line.strip()

                if requirement and requirement!= '-e .':
                    requirement_list.append(requirement)

    except FileNotFoundError:
        print("requirementes.txt file not foud")

        return requirement_list


setup(
    name = "NetworkSecurity",
    version = "0.0.1",
    author = "AlexDLP",
    author_email="alexdlp.dlp@gmail.com",
    packages = find_packages(),
    install_requires = get_requirements()
)
