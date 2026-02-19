from pathlib import Path
from setuptools import find_packages, setup


README = Path(__file__).parent / "README.md"

setup(
    name="mercury-framework",
    version="3.0.0",
    description="Mercury - an educational, safe framework for security research and simulation.",
    long_description=README.read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    author="Voltsparx",
    author_email="voltsparx@gmail.com",
    python_requires=">=3.10",
    packages=find_packages(
        include=["mercury", "mercury.*", "mercury_plugins", "mercury_plugins.*", "detection", "detection.*"]
    ),
    include_package_data=True,
    install_requires=["colorama>=0.4.6"],
    extras_require={"dev": ["pytest>=7.0"]},
    entry_points={"console_scripts": ["mercury=mercury.launcher:main"]},
    zip_safe=False,
)
