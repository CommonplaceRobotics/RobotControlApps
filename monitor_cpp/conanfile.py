import os

from conan import ConanFile


class Recipe(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "CMakeToolchain"
    
    # Make sure grpc build and tool requirements use the same options so it won't be built twice (to save time)
    grpc_options = {
        "csharp_ext": "False",
        "csharp_plugin": "False",
        "node_plugin": "False",
        "objective_c_plugin": "False",
        "otel_plugin": "False",
        "php_plugin": "False",
        "python_plugin": "False",
        "ruby_plugin": "False",
    }
    
    def requirements(self):
        # These requirements are linked to the product binary
        self.requires("grpc/1.81.0", options=self.grpc_options, run=True)

    def build_requirements(self):
        # These requirements are tools or for testing and therefore are not part of the product
        
        # If cross compiling
        if str(self.settings.arch).startswith("arm"):
            self.tool_requires("grpc/1.81.0", options=self.grpc_options)
            
        # Needed for protoc only, auto-picks the version req'd by grpc
        self.tool_requires("protobuf/[^6.0.0]")
        
        self.test_requires("gtest/[^1.13]")
            
    def layout(self):
        # Defines the directory structure
        if self.settings.os == "Windows":
            self.folders.generators = os.path.join(
                "out",
                "conan",
                str(self.settings.os),
                str(self.settings.build_type),
                "generators",
            )
            self.folders.build = os.path.join(
                "out", "build", str(self.settings.os), str(self.settings.build_type)
            )
        else:
            # Linux: also distinguish architecture
            self.folders.generators = os.path.join(
                "out",
                "conan",
                str(self.settings.os),
                str(self.settings.arch),
                str(self.settings.build_type),
                "generators",
            )
            self.folders.build = os.path.join(
                "out",
                "build",
                str(self.settings.os),
                str(self.settings.arch),
                str(self.settings.build_type),
            )