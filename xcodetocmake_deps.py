import os
import re

def extract_files_from_project(project_path):
    """Extract all source files, headers, frameworks, and resources from the Xcode project."""
    pbxproj_path = os.path.join(project_path, 'project.pbxproj')
    
    # Check if the pbxproj file exists
    if not os.path.exists(pbxproj_path):
        raise FileNotFoundError(f"Error: {pbxproj_path} not found.")
    
    try:
        with open(pbxproj_path, 'r', encoding='utf-8') as f:
            pbxproj_content = f.read()
    except Exception as e:
        raise Exception(f"Error reading {pbxproj_path}: {e}")
    
    # File patterns for different file types
    file_patterns = {
        'source_files': re.compile(r'path\s*=\s*"([^"]+\.(?:m|mm|c|cpp|swift))"'),  # Objective-C, C, C++, Swift
        'header_files': re.compile(r'path\s*=\s*"([^"]+\.(?:h|hpp))"'),            # Headers
        'frameworks': re.compile(r'path\s*=\s*"([^"]+\.framework)"'),              # Frameworks
        'resources': re.compile(r'path\s*=\s*"([^"]+\.(?:plist|xib|storyboard))"') # Resources like plist, xib, storyboard
    }

    files = {'source_files': [], 'header_files': [], 'frameworks': [], 'resources': []}

    # Iterate over each pattern and collect matching files
    try:
        for category, pattern in file_patterns.items():
            for match in pattern.finditer(pbxproj_content):
                file_path = match.group(1)
                if file_path:
                    # Ensure relative paths are resolved to the project path
                    if not os.path.isabs(file_path):
                        file_path = os.path.join(project_path, file_path)
                    files[category].append(file_path)
    except Exception as e:
        raise Exception(f"Error parsing file references in {pbxproj_path}: {e}")
    
    return files

def create_cmake_lists(project_path, files, dependencies, include_headers=True, include_frameworks=True, include_resources=True):
    """Create a CMakeLists.txt file with source files, headers, frameworks, and resources."""
    
    # /* Start the CMakeLists generation */
    project_name = os.path.basename(project_path).replace(".xcodeproj", "")
    
    try:
        with open('CMakeLists.txt', 'w') as cmake_file:
            cmake_file.write("cmake_minimum_required(VERSION 3.10)\n")
            cmake_file.write(f"project({project_name})\n\n")
            
            # /* Add source files to the executable target */
            cmake_file.write("add_executable(${PROJECT_NAME}\n")
            for file in files['source_files']:
                cmake_file.write(f"    {file}\n")
            cmake_file.write(")\n\n")

            # /* Conditionally include headers */
            if include_headers and files['header_files']:
                cmake_file.write("# Header files\n")
                for header in files['header_files']:
                    cmake_file.write(f"#    {header}\n")  # Headers noted for informational purposes

            # /* Conditionally link frameworks */
            if include_frameworks:
                for framework in files['frameworks']:
                    framework_name = os.path.basename(framework).replace(".framework", "")
                    cmake_file.write(f"target_link_libraries(${PROJECT_NAME} {framework_name})\n")
            
            # /* Link additional user-specified dependencies */
            for dep in dependencies:
                cmake_file.write(f"target_link_libraries(${PROJECT_NAME} {dep})\n")

            # /* Conditionally handle resources */
            if include_resources and files['resources']:
                cmake_file.write("\n# Resources\n")
                cmake_file.write("set(RESOURCE_DIR ${CMAKE_BINARY_DIR}/Resources)\n")
                cmake_file.write("file(MAKE_DIRECTORY ${RESOURCE_DIR})\n")
                for resource in files['resources']:
                    cmake_file.write(f"file(COPY {resource} DESTINATION ${{RESOURCE_DIR}})\n")
            
            cmake_file.write("\n")
    except Exception as e:
        raise Exception(f"Error writing CMakeLists.txt: {e}")

def xcode_to_cmake(xcodeproj_path, dependencies, include_headers=True, include_frameworks=True, include_resources=True):
    try:
        files = extract_files_from_project(xcodeproj_path)
    except Exception as e:
        print(e)
        return

    try:
        create_cmake_lists(xcodeproj_path, files, dependencies, include_headers, include_frameworks, include_resources)
    except Exception as e:
        print(e)
        return

if __name__ == "__main__":
    xcode_project_path = input("Enter path to the .xcodeproj directory: ")
    
    if not os.path.isdir(xcode_project_path):
        print(f"Error: {xcode_project_path} is not a valid directory.")
        exit(1)

    deps = input("Enter dependencies separated by space (e.g. pthread OpenGL): ").split()

    # /* Ask user whether to include headers, frameworks, and resources */
    include_headers = input("Include header files in the CMakeLists.txt? (y/n): ").lower() == 'y'
    include_frameworks = input("Include frameworks in the CMakeLists.txt? (y/n): ").lower() == 'y'
    include_resources = input("Include resources in the CMakeLists.txt? (y/n): ").lower() == 'y'
    
    try:
        xcode_to_cmake(xcode_project_path, deps, include_headers, include_frameworks, include_resources)
        print("CMakeLists.txt with dependencies generated.")
    except Exception as e:
        print(f"Error during conversion: {e}")
