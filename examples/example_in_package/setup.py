from setuptools import setup, find_packages

setup(
    name='mypackage',
    version='0.1.0',
    description='An example package',
    packages=find_packages(),
    install_requires=[
        "loguru",
        "mashumaro",
        "setuptools",
        "upandup"
    ],
    python_requires='>=3.11',
)