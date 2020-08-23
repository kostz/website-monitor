import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='website-monitor',
    version='1.0',
    author='Kost Zhukov',
    author_email='kost.zhukov@gmail.com',
    description='website monitoring utility with kafka transport and postgresql persistent storage',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    python_requires='>=3.6'
)