from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Reusable Code Library'

# Setting up
setup(
    name="CodeLib",
    version=VERSION,
    author="Willem van der Schans",
    author_email="willemvanderschans97+CodeLib@gmail.com",
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # additional packages

    keywords=['python', 'code library'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Reference",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)