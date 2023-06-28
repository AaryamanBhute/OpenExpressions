
from distutils.core import setup
setup(
  name = 'openexpressions',
  packages = ['openexpressions'],
  version = '1.0',
  license='MIT',
  description = 'A easy to use and expandable expression parser',
  author = 'Aaryaman Bhute',
  author_email = 'aryamanbhute@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/AaryamanBhute/OpenExpressions',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/AaryamanBhute/OpenExpressions/v_10.tar.gz',    # I explain this later on
  keywords = ['EXPRESSION', 'PARSER', 'EXPANDABLE', 'CUSTOMIZABLE'],   # Keywords that define your package best
  install_requires=[],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
  ],
)