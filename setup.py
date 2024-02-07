from setuptools import setup, find_packages

setup(
    name='upandup',
    version='0.1.0',
    description='A simple schema versioning system for Python dataclasses',
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