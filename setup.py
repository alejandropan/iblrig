from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='iblrig',
    version='3.7.0',
    description='IBL rig code',
    license="MIT",
    long_description=long_description,
    author='Niccolò Bonacchi',
    url="https://www.internationalbrainlab.com/",
    packages=find_packages(),  # same as name
    install_requires=[],  # external packages as dependencies
    scripts=[]
)
