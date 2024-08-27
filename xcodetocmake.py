import os
import plistlib

def extract_files_from_project(project_path):
    # Extract all source files from the Xcode project.
    pbxproj_path = os.path.join(project_path, 'project.pbxproj')
    
    # Open the Xcode project file in binary read mode
    with open(pbxproj_path, 'rb') as f:
        # Load the project file using plistlib
        pbxproj = plistlib.load(f, fmt=plistlib.FMT_XML)
    
    # Initialize an empty dictionary to store file references
    file_references = {}
    # Iterate over the objects in the project file
    for key, value in pbxproj['objects'].items():
        # Check if the object is a file reference
        if value.get('isa') == 'PBXFileReference':
            # Get the file path
            file_path = value.get('path')
            # If the file path exists, add it to the dictionary
            if file_path:
                file_references[key] = file_path
    
    # Return a list of all file paths
    return list(file_references.values())

def create_cmake_lists(project_path, source_files):
    # Create a basic CMakeLists.txt file.
    project_name = os.path.basename(project_path).replace(".xcodeproj", "")
    
    # Open a new CMakeLists.txt file in write mode
    with open('CMakeLists.txt', 'w') as cmake_file:
        # Write the minimum required CMake version
        cmake_file.write("cmake_minimum_required(VERSION 3.10)\n")
        # Write the project name
        cmake_file.write(f"project({project_name})\n\n")
        # Start the add_executable command
        cmake_file.write("add_executable(${PROJECT_NAME}\n")
        
        # Write each source file path into the CMakeLists.txt
        for file in source_files:
            cmake_file.write(f"    {file}\n")
        
        # Close the add_executable command
        cmake_file.write(")\n")

def xcode_to_cmake(xcodeproj_path):
    # Extract source files from the Xcode project
    source_files = extract_files_from_project(xcodeproj_path)
    # Create the CMakeLists.txt file with the extracted source files
    create_cmake_lists(xcodeproj_path, source_files)

if __name__ == "__main__":
    # Prompt the user to enter the path to the .xcodeproj directory
    xcode_project_path = input("Enter path to the .xcodeproj directory: ")
    # Convert the Xcode project to a CMake project
    xcode_to_cmake(xcode_project_path)
    # Inform the user that the CMakeLists.txt file has been generated
    print("CMakeLists.txt generated.")
