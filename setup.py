from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyterminal-emulator",  # Replace with a unique name for your package
    version="1.1.0",  # Start with 0.0.1 and increment for new releases
    author="Aarav Shah",  # Replace with your name
    author_email="aaravprogrammers@gmail.com",  # Replace with your email
    description="A Linux Terminal Emulator development Package for various os",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ap1311/pyterminal-emulator",  # Optional: Link to your GitHub repo
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Or whatever license you choose
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "Topic :: System :: Shells",
    ],
    install_requires=[
        'requests',
        'pycurl',
    ],
    entry_points={
        'console_scripts': [
            'pyterminalx=pyterminalx.commands:main',  # Example
        ],
    },
)