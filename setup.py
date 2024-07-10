from setuptools import setup, find_packages

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