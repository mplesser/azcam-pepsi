from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    "ipython",
    "azcam",
    "azcam-archon",
    "azcam-ds9",
]

setup(
    name="azcam-pepsi",
    version="21.1",
    description="azcam environment for PEPSI",
    long_description=long_description,
    author="Michael Lesser",
    author_email="mlesser@arizona.edu",
    keywords="",
    packages=find_packages(),
    zip_safe=False,
    url="https://mplesser.github.io/azcam/",
    install_requires=requirements,
)
