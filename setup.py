from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='upandup',
    version='0.1.0',
    description='A simple schema versioning system for Python dataclasses',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/smrfeld/upandup',
    packages=find_packages(),
    install_requires=[
        "loguru",
        "mashumaro",
        "pytest",
        "setuptools"
    ],
    python_requires='>=3.11',
    license='MIT'
)