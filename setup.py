# idk... this dont work use only CLI and Streamlit ^-^

from setuptools import setup, find_packages

setup(
    name="qrforge",
    version="0.1.0",
    description="qr generator",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "qrcode[pil]>=7.4",
        "Pillow>=10.0",
        "cryptography==44.0.1",
        "streamlit>=1.27",
        "argparse>=1.4",
    ],
    entry_points={
        "console_scripts": [
            "qrforge=cli:main",
        ],
    },
    python_requires=">=3.10",
    include_package_data=True,
)