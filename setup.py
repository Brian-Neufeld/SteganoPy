from setuptools import setup, Extension
import pybind11

cpp_args = ['-std=c++11', '-stdlib=libc++', '-mmacosx-version-min=10.7']

sfc_module = Extension(
    'encryptionmodule',
    sources=['encryptionmodule.cpp'],
    include_dirs=[pybind11.get_include()],
    language='c++',
    extra_compile_args=cpp_args,
    )

setup(
    name='encryptionmodule',
    version='1.0',
    description='Python package for data encryption',
    ext_modules=[sfc_module],
)
