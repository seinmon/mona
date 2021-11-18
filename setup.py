from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='monalyza',
      version='0.0.1',
      description='Lightweight resource monitoring and analysis tool.',
      long_description=readme(),
      long_description_content_type='text/markdown',
      url='http://github.com/seinmon/monalyza',
      author='Hossein Monjezi',
      author_email='hossein.monjezi@stud.uni-saarland.de',
      license='MIT',
      packages=['monalyza', 
               'monalyza.monitoring'],
      classifiers=[
          'Environment :: Console'
          'Development Status :: 2 - Pre-Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6'
          'Programming Language :: Python :: 3.7'
          'Programming Language :: Python :: 3.8'
          'Programming Language :: Python :: 3.9'
          'Programming Language :: Python :: 3.10'
          'Programming Language :: Python :: 3.11'
          'Topic :: System :: Monitoring'
          'Topic :: Scientific/Engineering'
          'Operating System :: OS Independent'
          'Intended Audience :: Developers'
      ],
      install_requires=['psutil'],
      zip_safe=False)
