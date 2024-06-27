from setuptools import setup, find_packages

def read_requirements():
    """Reads requirements from 'requirements.txt'."""
    with open('requirements.txt') as f:
        return f.read().splitlines()

entry_points = {
    'console_scripts': [
        'sifra = cli:cli',
    ],
}

setup(
    author = 'Prateek Chhikara',
    author_email = 'prateekchhikara24@gmail.com',
    name = 'sifra',
    version = '1.0',
    packages = find_packages(),
    include_package_data = True,
    install_requires = read_requirements(),
    entry_points = entry_points,
)