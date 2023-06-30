from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["pandas~=1.5.3", "requests~=2.29.0"]


setup(
    name="K5CodeLibrary",
    version="0.0.3",
    author="Willem van der Schans",
    author_email="willemvanderschans97+codelib@gmail.com",
    description="In-house code library to promote code re-usability",
    long_description=readme,
    long_description_content_type="text/markdown",
    url='https://www.github.com/Kydoimos97/CodeLibrary',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
