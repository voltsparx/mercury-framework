# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="mercury-framework",
    version="0.1.0",
    description="Mercury — an educational, safe framework for security research and simulation (harmless stubs only).",
    author="voltsparx",
    author_email="voltsparx@gmail.com",
    python_requires=">=3.8",
    packages=find_packages(include=["mercury", "mercury.*", "mercury_plugins", "mercury_plugins.*"]),
    install_requires=[
        # Add dependencies if needed
    ],
    include_package_data=True,
    zip_safe=False,
)
