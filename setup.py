from setuptools import setup, find_packages

# Read long description from README.md
with open('README.md', 'r') as file:
    long_description = file.read()

# Read requirements from requirements.txt
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="colab_utils",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=["tests", "docs"]),
    install_requires=[
        "requests",
        "pandas",
        "matplotlib",
        "seaborn",
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    author="Nghi Lam Minh Nhut",
    author_email="nghinhut@gmail.com",
    description="A collection of utility functions for Google Colab notebooks",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nghinhut/colab-utils",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
