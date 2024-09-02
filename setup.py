import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lego",
    version="0.0.1",
    author="s-hammon",
    description=("A CLI for (simple) analysis of text corpora. Incorporates Zipf's Law, "
                 "Chi-Square tests, and ratio of words used only once, twice, thrice, and so on."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/s-hammon/legomena",
    project_urls={
        "Bug Tracker": "https://github.com/s-hammon/legomena/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Typing :: Typed"
    ],
    install_requires=[
        "numpy",
        "pyyaml"
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "lego = app.cli:main"
        ]
    }
)