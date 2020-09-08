import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bbads",
    version="0.0.1",
    author="badbayesian",
    author_email="badbayesian@gmail.com",
    description="Classic algorithms and Data Structures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/badbayesian/bbads",
    packages=setuptools.find_packages(),
    classifiers=["MIT License"],
    python_requires=">=3.7",
)
