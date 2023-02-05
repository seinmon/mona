from setuptools import setup


def readme():
    """Read and return the content of README.md file."""
    with open('README.md', encoding='utf-8') as readme_file:
        return readme_file.read()


setup(name='mona',
      version='0.0.1',
      description='Lightweight resource monitoring and analysis tool.',
      long_description=readme(),
      long_description_content_type='text/markdown',
      url='http://github.com/seinmon/mona',
      author='Hossein Monjezi',
      author_email='hossein.monjezi@live.com',
      license='MIT',
      packages=['mona', 'mona.core'],
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
          'Intended Audience :: Developers'
      ],
      install_requires=['psutil'],
      entry_points={'console_scripts': ['mona=mona.main:main']},
      zip_safe=False)
