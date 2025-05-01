import setuptools

version = {}
with open("./cms_bluebutton/version.py") as fp:
    exec(fp.read(), version)

setuptools.setup(version=version['__version__'])
