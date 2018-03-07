from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='HuhuSeg',   

    version='0.3.07',  

    description='Simple Chinese segmentator, keywords extractor and other examples',  

    url = 'https://github.com/Colearo/HuhuSeg',

    author='Kechen Lu',  

    author_email='colearolu@icloud.com',  

    license='GNU General Public License v3 (GPLv3)',

    long_description=long_description,

    classifiers=[  
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Information Analysis',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='chinese-segmentation keywords-extraction nlp',  

    packages=['huhu_seg'], 
    package_dir={'huhu_seg': 'src/huhu_seg'},

    install_requires=['numpy'],  

    package_data={'huhu_seg': ['lexicon/*.segd']}, 

)
