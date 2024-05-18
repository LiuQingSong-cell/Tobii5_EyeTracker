from setuptools import Extension, setup

tracker_module = Extension("EyeTracker", 
                           sources=['EyeTracker.cpp'], 
                           include_dirs=['C:/tobii_stream/include/tobii'], 
                           library_dirs=['./'], 
                           libraries=['tobii_stream_engine'], 
                        )   

setup(
    name='EyeTracker',
    version='1.0',
    description='Python extension for Tobii eye tracker5 device',
    ext_modules=[tracker_module]
)