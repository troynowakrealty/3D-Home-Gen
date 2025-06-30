from setuptools import setup

setup(
    name='blendertoolbox',
    version='0.0.6',
    description='Some Blender functions for rendering paper figures',
    url='https://github.com/HTDerekLiu/BlenderToolbox/',
    author='Hsueh-Ti Derek Liu',
    author_email='hsuehtil@gmail.com',
    license='Apache 2.0',
    packages=['blendertoolbox'],
    install_requires=[ ],
    entry_points={
        'console_scripts': [
            'bt-render=blendertoolbox.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3.10',
    ],
)