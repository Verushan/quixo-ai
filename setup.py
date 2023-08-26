from setuptools import setup, find_packages


with open("README.rst") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="quixo-ai",
    version="0.1.0",
    description="Quixo AI Agent",
    long_description=readme,
    author="Vershan Naidoo",
    author_email="verushannaidoo@gmail.com",
    url="https://github.com/Elementrix08/quixo-ai",
    license=license,
    packages=find_packages(exclude=("tests", "docs")),
)
