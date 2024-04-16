r"""
       ___      __             __   
  ____/ (_)____/ /________  __/ /__ 
 / __  / / ___/ __/ ___/ / / / / _ \
/ /_/ / / /__/ /_/ /  / /_/ / /  __/
\__,_/_/\___/\__/_/   \__,_/_/\___/ 

"""

from setuptools import setup

__title__ = "dictrule"
__description__ = "Python rules defined by a dict and a text generator from the rules"
__url__ = "https://github.com/elhoangvu/dictrule"
__version__ = "0.1.0"
__author__ = "Zooxy Le"
__author_email__ = "elhoangvu@gmail.com"
__license__ = "Apache-2.0"
__copyright__ = "Copyright Zooxy Le"
__readme__ = ""

with open(file="README.md", mode="r", encoding="utf-8") as f:
    readme = f.read()

if __name__ == "__main__":
    setup(
        name=__title__,
        version=__version__,
        description=__description__,
        long_description=__readme__,
        long_description_content_type="text/markdown",
        author=__author__,
        author_email=__author_email__,
        url=__url__,
        packages=["dictrule"],
        package_data={"": ["LICENSE", "NOTICE"]},
        package_dir={"": "src"},
        include_package_data=True,
        python_requires=">=3.7",
        license=__license__,
        zip_safe=False,
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: Apache Software License",
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
