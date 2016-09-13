from conans import ConanFile, CMake
import sys
import os

class openal(ConanFile):
	name = "openal-soft"
	version = "1.17.2"
	FOLDER_NAME = "openal-soft"
	settings = "os" , "compiler", "build_type", "arch"
    url = "https://bitbucket.org/dsobczyk/conan-asio"
    author = "Bartlomiej Parowicz (bparowicz@gmail.com)"
	license = "https://github.com/kcat/openal-soft/blob/master/COPYING"
	options = {"shared": [True, False]}
	default_options = "shared=False"

	def source(self):
		self.run("git clone https://github.com/kcat/openal-soft.git")

	def build(self):
		cmake = CMake(self.settings)

		args  = ["-DCMAKE_INSTALL_PREFIX=install"]

		if self.options.shared:
			args += ["-DBUILD_SHARED_LIBS=ON"]  
		else: 
			args += ["-DBUILD_SHARED_LIBS=OFF"]

		self.run("cmake %s %s %s" % (self.FOLDER_NAME, cmake.command_line, ' '.join(args)))
		self.run("cmake --build . --target install %s" % cmake.build_config)
		self.run("echo cmake --build. --target install %s" % cmake.build_config)

	def package(self):
		self.copy("*.h", dst = "OpenAL32", src = os.path.join(self.FOLDER_NAME, "OpenAL32"))
		self.copy("*.h", dst = "include", src = os.path.join(self.FOLDER_NAME, "include"))
		self.copy("*.h", dst = "Alc", src = os.path.join(self.FOLDER_NAME, "Alc"))

		self.copy("*.dll", dst = "lib", src = "install/lib")
		self.copy("*.lib", dst = "lib", src = "install/lib")
		self.copy("*.dylib", dst = "lib", src = "install/lib")
		self.copy("*.a", dst = "lib", src = "install/lib")

	def package_info(self):
		if self.settings.os == "Linux":
			self.cpp_info.libs = ["openal"]
		elif self.settings.os == "Windows":
			self.cpp_info.libs = [ "OpenAL32"]
		elif self.settings.os == "Macos":
			self.cpp_info.libs = ["OpenAL"]
