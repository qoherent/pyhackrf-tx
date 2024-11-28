from setuptools import setup, find_packages

setup(
    name='pyhackrf-tx',
    version='0.2.1',  # Update the version number
    description='Python interface for HackRF with transmitter support',
    author='Ash Beigi',
    author_email='ash@qoherent.ai',
    url='https://github.com/qoherent/pyhackrf-tx',
    packages=find_packages(),
    install_requires=[
        'numpy',
        # Add other dependencies if necessary
    ],
)
