import os
import plistlib

def extract_files_from_project(project_path):
    """Extract all source files from the Xcode project."""
    pbxproj_path = os.path.join(project_path, 'project.pbxproj')
    
    with open(pbxproj_path, 'rb') as f:
        pbxproj = plistlib.load(f, fmt=plistlib.FMT_XML)
    
    file_references = {}
    for key, value in pbxproj['objects'].items():
        if value.get('isa') == 'PBXFileReference':
            file_path = value.get('path')
            if file_path:
                file_references[key] = file_path
    
    return list(file_references.values())

def create_cmake_lists(project_path, source_files, dependencies):
    """Create a basic CMakeLists.txt file with dependencies."""
    project_name = os.path.basename(project_path).replace(".xcodeproj", "")
    
    with open('CMakeLists.txt', 'w') as cmake_file:
        cmake_file.write(f"cmake_minimum_required(VERSION 3.10)\n")
        cmake_file.write(f"project({project_name})\n\n")
        cmake_file.write("add_executable(${PROJECT_NAME}\n")
        
        for file in source_files:
            cmake_file.write(f"    {file}\n")
        
        cmake_file.write(")\n")
        
        for dep in dependencies:
            cmake_file.write(f"target_link_libraries(${PROJECT_NAME} {dep})\n")

def xcode_to_cmake(xcodeproj_path, dependencies):
    source_files = extract_files_from_project(xcodeproj_path)
    create_cmake_lists(xcodeproj_path, source_files, dependencies)

if __name__ == "__main__":
    xcode_project_path = input("Enter path to the .xcodeproj directory: ")
    deps = input("Enter dependencies separated by space (e.g. pthread OpenGL): ").split()
    xcode_to_cmake(xcode_project_path, deps)
    print("CMakeLists.txt with dependencies generated.")