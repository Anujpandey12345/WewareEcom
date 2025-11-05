from setuptools import setup
from Cython.Build import cythonize
from setuptools.extension import Extension
import numpy as np

extensions = [
    Extension('shop.recommender.similarity', ['shop/recommender/similarity.pyx'], include_dirs=[np.get_include()])
]

setup(
    name='shop_recommender',
    ext_modules=cythonize(extensions, annotate=False),
)
