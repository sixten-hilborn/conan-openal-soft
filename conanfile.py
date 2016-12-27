from conans import ConanFile, CMake
from conans.tools import get
import sys
import os

class openal(ConanFile):
	name = "openal-soft"
	version = "1.17.2"
	FOLDER_NAME = "openal-soft-openal-soft-1.17.2"
	settings = "os", "compiler", "build_type", "arch"
	url = "https://github.com/R3v3nX/conan-openal-soft"
	author = "Bartlomiej Parowicz (bparowicz@gmail.com)"
	exports = ["FindOpenAl.cmake"]
	license = "MIT License"

	def source(self):
		get("https://github.com/kcat/openal-soft/archive/openal-soft-1.17.2.tar.gz")
	
	def system_requirements(self):
		if self.settings.os == "Linux":
			self.run("sudo apt-get install libasound2-dev")

	def build(self):
		cmake = CMake(self.settings)

		args  = ["-DCMAKE_INSTALL_PREFIX=install"]

		self.run("cmake %s %s %s" % (self.FOLDER_NAME, cmake.command_line, ' '.join(args)))
		self.run("cmake --build . --target install %s" % cmake.build_config)
		self.run("echo cmake --build. --target install %s" % cmake.build_config)

	def package(self):
		self.copy("*.h", dst = "OpenAL32", src = os.path.join(self.FOLDER_NAME, "OpenAL32"))
		self.copy("*.h", dst = "include", src = os.path.join(self.FOLDER_NAME, "include"))
		self.copy("*.h", dst = "Alc", src = os.path.join(self.FOLDER_NAME, "Alc"))
		
		self.copy("*", dst = "lib", src = "install/lib")

	def package_info(self):
		if self.settings.os == "Windows":
			self.cpp_info.libs = [ "OpenAL32"]
		else:
			self.cpp_info.libs = ["openal"]
