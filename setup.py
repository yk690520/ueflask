from setuptools import find_packages,setup
setup(
    name = 'ueflask',     #pypi中的名称，pip或者easy_install安装时使用的名称
    version = '1.4',
    author ='mlea',
    author_email='yk690520@outlook.com',
    description='This is a plugins for uediter',
    keywords='uediter',
    url='https://github.com/yk690520/ueflask',
    packages = find_packages(),
    include_package_data=True,
    #需要安装的依赖
    install_requires=[
        'flask>=1.0.2',
        'qiniu>=7.2.2'
    ],
    # 此项需要，否则卸载时报windows error
    zip_safe=False

)