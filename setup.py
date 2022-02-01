from setuptools import setup


setup(
    name="cms-bb2",
    version="0.0.1",
    description="An SDK used for interacting with the CMS Blue Button 2.0 API",
    py_modules=["bb2"],
    package_dir={"": "src"},
)