from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="CHIDS",
    version="1.0.0",
    author="Asbat El Khairi",
    author_email="asbat.el_khairi@siemens.com",
    description="CHIDS: Contextualizing System Calls in Containers for Anomaly-Based Intrusion Detection",
    packages=find_packages(),
    platforms=['linux_x86_64'],
    install_requires=[
        'joblib',
        'keras',
        'rich',
        'numpy',
        'matplotlib',
        'networkx',
        'nltk',
        'pandas',
        'typer[all]',
        'scikit_learn',
        'scipy',
        'setuptools',
        'tabulate',
        'tensorflow'],
    zip_safe=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
