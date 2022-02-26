from setuptools import setup, find_packages
from pathlib import Path

HERE = Path(__file__).resolve().parent

readme = (HERE / 'README.rst').read_text("utf-8")

setup(
    author="Brénainn Woodsend",
    author_email='bwoodsend@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    description=
    "A really boring package which finds and displays licenses in an assortment of CLI/GUI formats.",
    install_requires=[],
    extras_require={
        "test": ['pytest>=3', 'pytest-order', 'coverage', 'pytest-cov']
    },
    license="MIT license",
    long_description=readme,
    package_data={"lamancha": []},
    keywords='lamancha',
    name='lamancha',
    packages=find_packages(include=['lamancha', 'lamancha.*']),
    url='https://github.com/bwoodsend/lamancha',
    version="0.1.0",
)
