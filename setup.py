"""Setup configuration for Sigmanael.

Copyright © 2026 NAEL Abdelmajid Yacoub AlNaimat. All Rights Reserved.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="sigmanael",
    version="0.1.0",
    author="NAEL Abdelmajid Yacoub AlNaimat",
    description="A unique personal assistant chatbot that adapts to your behavior",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/naelnaimat-netizen/Sigmanael-",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Communications :: Chat",
        "Topic :: Office/Business :: Scheduling",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "sigmanael=sigmanael.main:main",
            "sigmanael-server=sigmanael.server:main",
        ],
    },
)
