from setuptools import setup, find_packages
from typing import List  

__version__ = "0.0.1"
SRC_REPO = "expense_tracking"

setup(
    name=SRC_REPO,
    version=__version__,
    description = "This is a Expense Tracking System",
    author="Aadarsh Kushwaha",
    author_email="aadarshkushwaha0208@gmail.com",
    packages=find_packages()
)