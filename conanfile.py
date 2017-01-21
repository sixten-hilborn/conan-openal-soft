from conans import ConanFile, CMake
from conans.tools import get, SystemPackageTool, replace_in_file
import sys
import os

class openal(ConanFile):
	name = "openal-soft"
	version = "1.17.2"
	FOLDER_NAME = "openal-soft-openal-soft-1.17.2"
	settings = "os", "compiler", "build_type", "arch"
	generators = "cmake"
	url = "https://github.com/sixten-hilborn/conan-openal-soft"
	author = "Bartlomiej Parowicz (bparowicz@gmail.com)"
	exports = ["FindOpenAl.cmake"]
	license = "MIT License"

	def system_requirements(self):
		if self.settings.os == "Linux":
			installer = SystemPackageTool()
			installer.update()
			installer.install("libasound2-dev")

	def source(self):
		get("https://github.com/kcat/openal-soft/archive/openal-soft-1.17.2.tar.gz")
		replace_in_file("{0}/CMakeLists.txt".format(self.FOLDER_NAME), "PROJECT(OpenAL)", """PROJECT(OpenAL)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
""")

	def build(self):
		cmake = CMake(self.settings)

		args = ["-DCMAKE_INSTALL_PREFIX=install"]

		self.run("cmake %s %s %s" % (self.FOLDER_NAME, cmake.command_line, ' '.join(args)))
		self.run("cmake --build . --target install %s" % cmake.build_config)
		self.run("echo cmake --build. --target install %s" % cmake.build_config)

	def package(self):
		self.copy("*.h", dst="include", src="install/include")
		self.copy("*.lib", dst="lib", src="install/lib", keep_path=False)
		self.copy("*.a", dst="lib", src="install/lib", keep_path=False)
		self.copy("*.so*", dst="lib", src="install/lib", keep_path=False, links=True)
		self.copy("*.dll", dst="bin", src="install/bin", keep_path=False)
		self.copy("*.dylib", dst="lib", src="install/bin", keep_path=False)

	def package_info(self):
		if self.settings.os == "Windows":
			self.cpp_info.libs = ["OpenAL32"]
		else:
			self.cpp_info.libs = ["openal"]
