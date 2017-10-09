from conans import ConanFile, tools
import os
from conans.errors import ConanException


class KeylokConan(ConanFile):
    name = "Keylok"
    version = "2015"
    license = "Proprietary"
    url = "http://github.com/kenfred/conan-keylok"
    description = "KEYLOK Software Piracy Prevention System"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "networking": [True, False]}
    default_options = "shared=False", "networking=False"

    
    def configure(self):
        if self.settings.compiler == "Visual Studio" and self.settings.compiler.version == 15:
            raise ConanException("Visual Studio 2017 libs not available")

    def build_id(self):
        # There is a single zip file for all configurations, so we only need one build variant
        self.info_build.settings.os = "Any"
        self.info_build.settings.compiler = "Any"
        self.info_build.settings.build_type = "Any"
        self.info_build.settings.arch = "Any"
        self.info_build.options.shared = "Any"
        self.info_build.options.networking = "Any"

    def build(self):
        # There is no source to download, only pre-built libraries
        # So its fetched during the build step
        zip_name = "files_sdk.zip"
        url = "https://www.keylok.com/sites/default/files/%s" % zip_name
        self.output.info("Downloading %s..." % url)
        tools.download(url, zip_name)
        tools.unzip(zip_name)
        os.unlink(zip_name)

    def _get_lib_name(self):
        lib_name = ""
        if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio" and not self.options.shared:
            runtime_string = "%s" % self.settings.compiler.runtime
            lib_name = "kfunc%s%s%s" % ("32" if self.settings.arch == "x86" else "64",
                                            runtime_string[:2],
                                            "n" if self.options.networking else "")
        return lib_name

    def package(self):
        if self.settings.os == "Windows":
            if self.settings.compiler == "Visual Studio":
                if self.options.shared:
                    raise ConanException("Not Implemented")
                else:
                    visual_studio_years = {"8": "2005", "9": "2008", "10": "2010", "11": "2012", "12": "2013", "14": "2015"}
                    visual_studio_version_string = "%s" % self.settings.compiler.version
                    src_path = "API/Windows/VS%s" % visual_studio_years[visual_studio_version_string]
                    self.copy("%s.lib" % self._get_lib_name(), src=src_path, dst="lib", keep_path=False)
            else:
                raise ConanException("Not Implemented")
        else:
            raise ConanException("Not Implemented")
        
        # self.copy("*.h", dst="include", src="hello")
        # self.copy("*hello.lib", dst="lib", keep_path=False)
        # self.copy("*.dll", dst="bin", keep_path=False)
        # self.copy("*.so", dst="lib", keep_path=False)
        # self.copy("*.dylib", dst="lib", keep_path=False)
        # self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = [self._get_lib_name()]
