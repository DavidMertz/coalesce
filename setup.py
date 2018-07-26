from distutils.core import setup

with open("README") as fh:
    long_description = fh.read()

setup(
    name='coalescing',
    version='0.1.1',
    description='Access messy nested data structures',
    long_description=long_description,
    url="https://github.com/DavidMertz/coalesce",
    author='David Mertz',
    author_email='mertz@gnosis.cx',
    py_modules=['coalesce'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
