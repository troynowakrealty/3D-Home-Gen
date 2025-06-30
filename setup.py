from setuptools import setup

setup(
    name='blendertoolbox',
    version='0.0.5',
    description='Some Blender functions for rendering paper figures',
    url='https://github.com/HTDerekLiu/BlenderToolbox/',
    author='Hsueh-Ti Derek Liu',
    author_email='hsuehtil@gmail.com',
    license='Apache 2.0',
    packages=['blendertoolbox'],
    install_requires=[
        'numpy',
        # Blender Python API `bpy` must also be installed separately.
        # It is distributed via Blender and only available for certain
        # Python versions, so we do not list it as a strict dependency.
    ],
    classifiers=[
        'Programming Language :: Python :: 3.10',
    ],
)
