import os
import subprocess
import sys
import shutil

def parse_build_file(build_file):
    """Parse the BUILD file to get the list of source files."""
    with open(build_file, 'r') as f:
        content = f.read()

    source_files = content.split('main:')[1].strip().split()
    source_files = [f for f in source_files if f.endswith('.cc')]
    return source_files

def compile_package(package_path, source_files):
    """Compile the source files in the given package using clang++."""
    full_paths = [os.path.join(package_path, f) for f in source_files]
    temp_dir = os.path.join(package_path, 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    output_binary = os.path.join(temp_dir, 'main')
    compile_command = ['clang++', '--std=c++17', '-o', output_binary] + full_paths
    print(f"Compiling {package_path}...")
    subprocess.run(compile_command, check=True)

    return output_binary, temp_dir

def run_project(binary_path):
    """Run the compiled project binary."""
    print(f"Running {binary_path}...")
    subprocess.run([binary_path], check=True)

def cleanup_binary(binary_path, temp_dir):
    """Remove the compiled binary and temp directory."""
    print(f"Cleaning up {binary_path}...")
    os.remove(binary_path)
    shutil.rmtree(temp_dir)

def build_project(base_path):
    """Build all packages under the base project directory."""
    binaries = []
    for root, dirs, files in os.walk(base_path):
        if 'BUILD' in files:
            build_file = os.path.join(root, 'BUILD')
            source_files = parse_build_file(build_file)
            if source_files:
                output_binary, temp_dir = compile_package(root, source_files)
                binaries.append((output_binary, temp_dir))

    return binaries

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 build_tool.py <path_to_project>")
        sys.exit(1)

    project_root = sys.argv[1]
    if not os.path.isdir(project_root):
        print(f"Error: The directory {project_root} does not exist.")
        sys.exit(1)

    binaries = build_project(project_root)
    for binary, temp_dir in binaries:
        run_project(binary)
        cleanup_binary(binary, temp_dir)

if __name__ == "__main__":
    main()
