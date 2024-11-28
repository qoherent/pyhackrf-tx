from setuptools import setup, find_packages

setup(
    name='pyhackrftx',
    version='0.2.1',  # just a basic increment over the original
    description='Python interface for HackRF with transmitter support',
    author='Ash Beigi',
    author_email='info@qoherent.ai',
    license='GPLv3',
    url='https://github.com/qoherent/pyhackrftx',
    packages=['pyhackrftx'],
    install_requires=[
        'numpy',
    ],
)
