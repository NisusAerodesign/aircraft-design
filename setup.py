from setuptools import setup, find_packages

include_files = ['bin/.foo']

with open('README.md', 'r') as arq:
    readme = arq.read()

setup(name='aircraft-design',
        version='0.0.9',
        license='MIT',
        author='NisusAerodesign',
        author_email='ufsc.nisus@gmail.com',
        maintainer='Irisson Lima',
        maintainer_email='irisson2203@gmail.com',
        long_description=readme,
        long_description_content_type='text/markdown',
        keywords=['aircraft', 'design', 'VLM', 'vortex lattice'],
        description=u'Biblioteca para fazer análises de aeronaves',
        packages=find_packages(),
        install_requires=['numpy', 'matplotlib', 'scipy', 'avlwrapper', 'requests'],
        package_data={'': include_files},
        url='https://github.com/NisusAerodesign/aircraft-design',
)