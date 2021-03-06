from conans import CMake, ConanFile, tools
import os


class OpenALConan(ConanFile):
    name = "openal"
    description = "OpenAL Soft is a software implementation of the OpenAL 3D audio API."
    topics = ("conan", "openal", "audio", "api")
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.openal.org"
    license = "MIT"
    exports_sources = ["CMakeLists.txt", "patches/*"]
    generators = "cmake"

    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if tools.Version("1.20") <= self.version and self.settings.compiler.get_safe("cppstd"):
            tools.check_min_cppstd(self, "11")

        if self.options.shared:
            del self.options.fPIC
        if tools.Version('1.20') > self.version:
            del self.settings.compiler.libcxx
            del self.settings.compiler.cppstd

    def requirements(self):
        if self.settings.os == "Linux":
            self.requires("libalsa/1.1.9")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = "openal-soft-openal-soft-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.definitions["LIBTYPE"] = "SHARED" if self.options.shared else "STATIC"
        self._cmake.definitions["ALSOFT_UTILS"] = False
        self._cmake.definitions["ALSOFT_EXAMPLES"] = False
        self._cmake.definitions["ALSOFT_TESTS"] = False
        self._cmake.definitions["CMAKE_DISABLE_FIND_PACKAGE_SoundIO"] = True
        self._cmake.configure(build_folder=self._build_subfolder)
        return self._cmake

    def build(self):
        for patch in self.conan_data.get("patches", {}).get(self.version, []):
            tools.patch(**patch)
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        self.copy("COPYING", dst="licenses", src=self._source_subfolder)
        tools.rmdir(os.path.join(self.package_folder, "share"))
        tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))
        tools.rmdir(os.path.join(self.package_folder, "lib", "cmake"))

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "OpenAL"
        self.cpp_info.names["cmake_find_package_multi"] = "OpenAL"
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.system_libs.extend(["dl", "m"])
        elif self.settings.os == "Macos":
            self.cpp_info.frameworks.extend(["AudioToolbox", "CoreAudio", "CoreFoundation"])
        elif self.settings.os == "Windows":
            self.cpp_info.system_libs.extend(["winmm", "ole32", "shell32", "User32"])
        self.cpp_info.includedirs = ["include", "include/AL"]
        if not self.options.shared:
            self.cpp_info.defines.append("AL_LIBTYPE_STATIC")
