r"""
       ___      __             __   
  ____/ (_)____/ /________  __/ /__ 
 / __  / / ___/ __/ ___/ / / / / _ \
/ /_/ / / /__/ /_/ /  / /_/ / /  __/
\__,_/_/\___/\__/_/   \__,_/_/\___/ 

"""

from pathlib import Path
from setuptools import setup

this_directory = Path(__file__).parent

about = {}
with open(
    file=this_directory / "src" / "dictrule" / "__version__.py",
    mode="r",
    encoding="utf-8",
) as file:
    exec(file.read(), about)

long_description = (this_directory / "README.md").read_text()

if __name__ == "__main__":
    setup(
        name=about["__title__"],
        version=about["__version__"],
        description=about["__description__"],
        long_description=long_description,
        long_description_content_type="text/markdown",
        author=about["__author__"],
        author_email=about["__author_email__"],
        url=about["__url__"],
        packages=["dictrule", "dictrule/built_in_rules"],
        package_data={"": ["LICENSE", "NOTICE"]},
        package_dir={"": "src"},
        include_package_data=True,
        python_requires=">=3.7",
        license=about["__license__"],
        zip_safe=False,
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: Implementation :: PyPy",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Text Processing :: Markup",
        ],
        project_urls={
            "Documentation": "https://github.com/elhoangvu/dictrule",
            "Source": "https://github.com/elhoangvu/dictrule",
        },
    )
