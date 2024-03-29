import setuptools


version = {}
with open("./cms_bluebutton/version.py") as fp:
    exec(fp.read(), version)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cms-bluebutton-sdk",
    version=version['__version__'],
    author="CMS Blue Button 2.0 Team",
    author_email="BlueButtonAPI@cms.hhs.gov",
    license="CC0 1.0 Universal",
    description="An SDK used for interacting with the CMS Blue Button 2.0 API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CMSgov/cms-bb2-python-sdk",
    # For classifiers: https://pypi.org/classifiers/
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "requests >= 2.0",
        "requests-toolbelt >= 0.9.1",
        "pyyaml >= 5.0",
    ],
    extras_require={
        "dev": [
            "pytest >= 6.0",
            "requests-mock >= 1.9.3",
        ],
    },
)
