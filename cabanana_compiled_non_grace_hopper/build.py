import os
import shutil
import subprocess
import argparse

def cmake_build_cabana(cabana_source_dir, kokkos_install_dir, cabana_install_dir):
    """
    cabana_source_dir: git clone from github
    kokkos_install_dir: Directory of compiled kokkos
    cabana_install_dir: directory where we want to install cabana to
    
    """
    print("Starting to build Cabana...")
    build_dir = os.path.join(cabana_source_dir, 'build')
    print("Build directory: {}".format(build_dir))
    print("kokkos is installed in directory:{}".format(kokkos_install_dir))
    print("cabana will be installed in directory:{}".format(cabana_install_dir))
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)
        print("Created build directory.")
    if not os.path.exists(cabana_install_dir):
        os.makedirs(cabana_install_dir)
        print("Install Cabana to directory:{}".format(cabana_install_dir))
    cmake_command = [
        'cmake',
        '-D', 'CMAKE_BUILD_TYPE=Debug',
        '-D', 'CMAKE_PREFIX_PATH={}'.format(kokkos_install_dir),
        '-D', 'CMAKE_INSTALL_PREFIX={}'.format(cabana_install_dir),
        '-D', 'Cabana_REQUIRE_OPENMP=ON',
        '-D', 'Cabana_ENABLE_EXAMPLES=ON',
        '-D', 'Cabana_ENABLE_TESTING=OFF', 
        '-D', 'Cabana_ENABLE_PERFORMANCE_TESTING=OFF',
        '-D', 'Cabana_ENABLE_CAJITA=ON',
        '..'
    ]
    print("Running CMake command:")
    print(' '.join(cmake_command))
    try:
        subprocess.check_call(cmake_command, cwd=build_dir)
        print("CMake configuration successful.")
        subprocess.check_call(['make', 'install'], cwd=build_dir)
        print("Make install successful.")
    except subprocess.CalledProcessError as e:
        print("Error occurred while executing: {}".format(e.cmd))
        print("Exit status: {}".format(e.returncode))



if __name__ == "__main__":
    home_dir = os.environ.get('HOME', '')
    parser = argparse.ArgumentParser(description="Build and install Cabana with Kokkos")
    default_kokkos_install_dir = os.path.join(home_dir,'kokkos_install')
    default_cabana_source_dir = os.path.join(home_dir,'Cabana')
    default_cabana_install_dir = os.path.join(home_dir,'Cabana_install')
    parser.add_argument("--kokkos_install_dir", help="The directory of the installed Kokkos source", default=default_kokkos_install_dir)
    parser.add_argument("--cabana_source_dir", help="The directory of the Cabana source", default=default_cabana_source_dir)
    parser.add_argument("--cabana_install_dir", help="The directory of the installed Cabana source", default=default_cabana_install_dir)
    args = parser.parse_args()
    cmake_build_cabana(args.cabana_source_dir, args.kokkos_install_dir,args.cabana_install_dir)
