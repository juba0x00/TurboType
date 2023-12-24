from setuptools import setup, find_packages
        
setup(
    name="TurboType",
    version="1337.0",
    author="1337",
    description="A Game for Typing challenge",
    packages=find_packages(),
    package_data={'TurboType': ['data/*'],},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["pygame"],
    entry_points={"console_scripts": ["TurboType = TurboType.TurboType:main"]},
)
