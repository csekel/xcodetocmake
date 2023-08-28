# Xcode to CMake Converter

This is a set of simple tools designed by RadNight Technologies LLC. It's made to help you convert basic Xcode `.xcodeproj` projects into `CMakeLists.txt` configurations.

## Maintainer

**CliffSekel**  
RadNight Technologies LLC

## Features

- Extracts source files from `.xcodeproj`.
- Generates a basic `CMakeLists.txt`.
- Allows for manual specification of dependencies.

## Limitations

- This converter is basic and may not support all complexities of larger Xcode projects.
- Dependencies have to be manually specified for now.
- Does not automatically detect linked libraries, build settings, or other Xcode configurations.

## Usage

1. Clone the repository.
2. Run the provided Python script:  
   ```bash
   python xcode_to_cmake.py
   ```
3. When prompted, enter the path to your `.xcodeproj` directory.
4. Next, enter any dependencies your project requires, separated by spaces (e.g., `pthread OpenGL`).
5. A `CMakeLists.txt` file with the specified configurations will be generated in the current directory.

## Contributing

If you face any issues or have feature requests, feel free to open an issue on this GitHub repository. Contributions in the form of pull requests are also welcome!

## License

This project is licensed under the terms of the MIT license. Check the `LICENSE` file for more information.
