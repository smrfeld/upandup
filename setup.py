from setuptools import setup, find_packages

setup(
    name='upandup',
    version='0.1.0',
    description='A schema versioning system for Python dataclasses',
    url='https://github.com/smrfeld/upandup',
    packages=find_packages(),
    install_requires=[
        # Add your package dependencies here
        # 'numpy>=1.18.1',
        # 'pandas>=1.0.3',
    ],
    python_requires='>=3.11',
)