#!/usr/bin/env python
import sys
from setuptools import setup, find_packages


dev_requires = [
    'Sphinx==1.2.2',
]

install_requires = [
    'nodeconductor>=0.101.2',
    'paypalrestsdk>=1.10.0',
    'xhtml2pdf>=0.0.6',
    'Pillow>=2.0.0,<3.0.0',
]


setup(
    name='nodeconductor-paypal',
    version='0.3.5',
    author='OpenNode Team',
    author_email='info@opennodecloud.com',
    url='http://nodeconductor.com',
    description='NodeConductor PayPal allows to make payments via PayPal',
    long_description=open('README.rst').read(),
    package_dir={'': 'src'},
    packages=find_packages('src', exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=install_requires,
    zip_safe=False,
    extras_require={
        'dev': dev_requires,
    },
    entry_points={
        'nodeconductor_extensions': (
            'nodeconductor_paypal = nodeconductor_paypal.extension:PayPalExtension',
        ),
    },
    # tests_require=tests_requires,
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
    ],
)
