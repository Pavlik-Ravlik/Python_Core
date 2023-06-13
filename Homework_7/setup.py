from setuptools import setup, find_namespace_packages

setup(
    name='clear_folders',
    version='1.0.0',
    description='sorts the folder you want',
    url='https://github.com/Pavlik-Ravlik',
    author='Pavlik-Ravlik',
    author_email='pastet1990@icloud.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'],
    packages=find_namespace_packages(),
    entry_points={'console_scripts': [
        'clean-folder = sort_folder.sort:start']}
)
