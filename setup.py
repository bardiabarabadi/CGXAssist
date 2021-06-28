from setuptools import setup, find_packages
from shutil import copyfile
import os, platform


def get_long_description():
    return ""

def copy_docs():
    return

copy_docs()
long_description = get_long_description()

setup(
    name="CGXAssist",
    version="0.0.0dev0",
    description="A Python library for connecting and communicate with CGX EEG. "
                "Uses Bleak as the underlying Bluetooth interface.",
    keywords="CGX eeg ble neuroscience",
    url="https://github.com/bardiabarabadi/CGXAssist",
    author="Bardia Barabadi",
    author_email="bardiabarabadi@uvic.ca",
    license="MIT",
    entry_points={},
    packages=['CGXAssist'],
    package_data={},
    include_package_data=True,
    zip_safe=False,
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        "bitstring",
        "numpy",
        "seaborn",
        "pexpect",
        "bleak",
        "pygments",
        "pyserial",
        "esptool",
        "nest_asyncio",
        "scipy"
    ]
    ,
    classifiers=[
        # How mature is this project?  Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Intended Audience :: Science/Research",
        "Topic :: Software Development",
        # Specify the Python versions you support here.  In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Programming Language :: Python",
    ],
)
