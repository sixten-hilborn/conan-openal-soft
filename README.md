# conan-openal-soft
Conan.io script for openal-soft.

### OS support
Windows:
  Not tested yet.
  
Linux:
  Tested on Ubuntu 16.14. Be aware that script installs *libasound2-dev*. If this library is not available on the system, there will be a problem to run openal properly. For more info please go to https://github.com/kcat/openal-soft.
  
MacOSX:
  Tested on El Capitan. No issues detected.
  
### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
    boost/1.72.20@R3v3nX/testing

    [options]
    
    [generators]
    cmake

Complete the installation of requirements for your project running:

    conan install . --build=missing 

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.
