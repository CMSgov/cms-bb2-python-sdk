from setuptools import setup


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cms-bb2",
    version="1.0.0",
    author="CMS Blue Button 2.0 Team",
    author_email="bb2@example.com",  # TODO: Do we want to include?
    license="Apache Software License",
    description="An SDK used for interacting with the CMS Blue Button 2.0 API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CMSgov/cms-bb2-python-sdk",
    # For classifiers: https://pypi.org/classifiers/
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    py_modules=["bluebutton"],
    package_dir={"": "src"},
    python_requires=">=3.6",
    install_requires=[
        "requests >= 2.0",
    ],
    extras_require={
        "dev": [
            "pytest >= 6.0",
        ],
    },
)
