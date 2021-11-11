import setuptools

# For version number interpretation see: https://semver.org
VERSION = '1.1.0'

setuptools.setup(name='japh',
                 version=VERSION,
                 description='',
                 url='',
                 author='',
                 author_email='',
                 license='Private',
                 packages=setuptools.find_packages(where="src"),
                 package_dir={"": "src"},
                 include_package_data=True,
                 entry_points={
                     'console_scripts': ['japh=japh.main:start_app'],
                 },
                 zip_safe=False,
                 install_requires=["typer", "pyyaml", "pydantic"])