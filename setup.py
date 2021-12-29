import setuptools
import os


def package_files(directory):
    # https://stackoverflow.com/questions/27664504/how-to-add-package-data-recursively-in-python-setup-py/27664856
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


original_files = package_files('spherize_texture/original')
spherized_files = package_files('spherize_texture/spherized')


with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="spherize_texture",
    version="0.1.0.1",
    author="Selewirre Iskvary",
    author_email="selewirre@gmail.com",
    description="A tool for creating spherical-looking objects out of images.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/selewirre/spherize_texture",
    packages=setuptools.find_packages(),
    package_dir={'spherize_texture': 'spherize_texture'},
    package_data={'spherize_texture': original_files + spherized_files},
    install_requires=['pillow',
                      'numpy',
                      'pyqt5',
                      'scipy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GNU GPL v3 license",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)

