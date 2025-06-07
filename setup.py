from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyterminal-emulator",  # Replace with a unique name for your package
    version="0.0.1",  # Start with 0.0.1 and increment for new releases
    author="Aarav Shah",  # Replace with your name
    author_email="aaravprogrammers@gmail.com",  # Replace with your email
    description="A Linux Terminal Emulator development Package for various os",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ap1311/",  # Optional: Link to your GitHub repo
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Or whatever license you choose
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "Topic :: System :: Shells",
    ],
    python_requires='>=3.6',  # Minimum Python version your code supports
    install_requires=[
        'requests',
        'pycurl',
        'os',
        'subprocess',
        'shutil',
        'stat',
        'platform',
        'shlex',
        'tarfile',
        'gzip',
        'shutil',
        'zipfile',
        'sys',
        'io'
    ],
    py_modules=['command'], # This line is crucial for single-file modules
)