from setuptools import setup

version = "1.1.0"

description = """ A python package for visualizing non-linear dynamics and chaos. (2D phase portraits, 3D chaotic trajectories, Maps, Cobweb plots...)"""


def setup_package():
    metadata = dict(
        name="phaserportrait",
        maintainer="Víctor Loras & Unai Lería",
        maintainer_email="vhloras@gmail.com?cc=unaileria@gmail.com",
        description=description,
        url="https://phaseportrait.github.io/",
        author="Víctor Loras & Unai Lería",
        download_url="https://pypi.org/project/phaseportrait/",
        project_urls={
            "Documentation": "https://phaseportrait.github.io/",
            "Source Code": "https://github.com/phaseportrait/phaseportrait",
            "GUI": "https://github.com/phaseportrait/phaseportrait-gui",
        },
        license='MIT License',
        version=version,
        python_requires='>=3.8',
        zip_safe=False,
    )
    
    setup(**metadata)


if __name__=='__main__':
    setup_package()