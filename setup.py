r"""
       ___      __             __   
  ____/ (_)____/ /________  __/ /__ 
 / __  / / ___/ __/ ___/ / / / / _ \
/ /_/ / / /__/ /_/ /  / /_/ / /  __/
\__,_/_/\___/\__/_/   \__,_/_/\___/ 

"""

import os
import pytest
from setuptools import setup

about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(
    file=os.path.join(here, "src", "dictrule", "__version__.py"),
    mode="r",
    encoding="utf-8",
) as file:
    exec(file.read(), about)

with open(file="README.md", mode="r", encoding="utf-8") as f:
    readme = f.read()

if __name__ == "__main__":
    setup(
        name=about["__title__"],
        version=about["__version__"],
        description=about["__description__"],
        long_description=readme,
        long_description_content_type="text/markdown",
        author=about["__author__"],
        author_email=about["__author_email__"],
        url=about["__url__"],
        packages=[],
        package_data={"": ["LICENSE", "NOTICE"]},
        package_dir={"": "src"},
        include_package_data=True,
        python_requires=">=3.7",
        license=about["__license__"],
        zip_safe=False,
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
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
        cmdclass={"test": pytest},
        project_urls={
            "Documentation": "https://github.com/elhoangvu/dictrule",
            "Source": "https://github.com/elhoangvu/dictrule",
        },
    )
