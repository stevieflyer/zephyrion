from setuptools import setup, find_packages


def read_requirements():
    with open('requirements.txt', 'r') as f:
        requirements = f.readlines()
    return [req.strip() for req in requirements if req.strip() and not req.startswith('#')]


setup(
    name='zephyrion',
    version='0.1.17',
    packages=find_packages(exclude=['test', 'test.*']),
    install_requires=read_requirements(),
    url='https://github.com/stevieflyer/zephyrion',
    author='steveflyer',
    author_email='steveflyer7@gmail.com',
    description='',
    long_description=open('./README.md').read(),
    long_description_content_type='text/markdown',
)
