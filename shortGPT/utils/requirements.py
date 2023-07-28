import os
import platform


class Requirements:
    '''Manage requirements for the project'''

    def __init__(self):
        self.package_path = os.path.dirname(os.path.realpath(__file__))
        self.requirements_path = os.path.join(self.package_path, '..', '..', 'requirements.txt')

    def get_list_requirements(self):
        '''Get the list of requirements packages from requirements.txt'''
        with open(self.requirements_path) as f:
            requirements = f.read().splitlines()

        # remove comments and empty lines
        requirements = [line for line in requirements if not line.startswith('#')]
        requirements = [line for line in requirements if line.strip()]

        # extract package name from protocol
        requirements = [line.split('/')[-1] for line in requirements if not line.startswith('git+')]
        requirements = [line.split('/')[-1] for line in requirements if not line.startswith('http')]
        requirements = [line.split('/')[-1] for line in requirements if not line.startswith('https')]
        requirements = [line.split('/')[-1] for line in requirements if not line.startswith('ssh')]
        requirements = [line.split('/')[-1] for line in requirements if not line.startswith('git')]

        # sort alphabetically
        requirements.sort()

        return requirements

    def get_os_name(self):
        '''Get the name of the operating system'''
        return platform.system()

    def get_os_version(self):
        '''Get the version of the operating system'''
        return platform.version()

    def get_python_version(self):
        '''Get the version of Python installed'''
        return platform.python_version()

    def is_all_requirements_installed(self):
        '''Check if all requirements are installed'''
        requirements = self.get_list_requirements()
        for requirement in requirements:
            if not self.is_requirement_installed(requirement):
                return False
        return True

    def is_requirement_installed(self, package_name):
        '''Check if a package is installed'''
        import importlib
        try:
            importlib.import_module(package_name)
            return True
        except ImportError:
            return False

    def get_version(self, package_name):
        '''Get the version of a package'''
        import pkg_resources
        try:
            return pkg_resources.get_distribution(package_name).version
        except:
            return None

    def get_all_requirements_versions(self):
        '''Get the versions of all requirements'''
        requirements = self.get_list_requirements()
        versions = {}
        for requirement in requirements:
            versions[requirement] = self.get_version(requirement)
        return versions

    def get_all_requirements_not_installed(self):
        '''Get the list of all requirements not installed'''
        requirements = self.get_list_requirements()
        not_installed = {}
        for requirement in requirements:
            # if version is None then the package is not installed
            if self.get_version(requirement) is None:
                not_installed[requirement] = self.get_version(requirement)
        return not_installed


if __name__ == '__main__':
    '''Display information about the system and requirements'''
    requirements_manager = Requirements()
    if not requirements_manager.is_all_requirements_installed():
        print("Error : Some requirements are missing")
        print("Please install all requirements from requirements.txt")
        print("You can install them by running the following command:")
        print("pip install -r requirements.txt")

    print(f"System information:")
    print(f"OS name : {requirements_manager.get_os_name()}")
    print(f"OS version : {requirements_manager.get_os_version()}")
    print(f"Python version : {requirements_manager.get_python_version()}")

    # list all requirements and their versions
    print("List of all requirements and their versions:")
    all_req_versions = requirements_manager.get_all_requirements_versions()
    for req_name, req_version in all_req_versions.items():
        print(f"{req_name}=={req_version}")

    print("List of all requirements not installed:")
    all_req_not_installed = requirements_manager.get_all_requirements_not_installed()
    for req_name, req_version in all_req_not_installed.items():
        print(f"{req_name}=={req_version}")
