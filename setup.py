from setuptools import setup
with open('README.md', 'r') as arq:
    readme = arq.read()

setup(name='aircraft-design',
        version='0.0.1',
        license='MIT',
        author='NisusAerodesign Irisson Lima',
        long_description=readme,
        long_description_content_type='text/markdown',
        author_email='ufsc.nisus@gmail.com',
        keywords='aircraft design VLM vortex lattice',
        description=u'Biblioteca para fazer análises de aeronaves',
        packages=['aircraft_design'],
        install_requires=['numpy', 'matplotlib', 'scipy', 'avlwrapper'])