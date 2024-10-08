import os
import subprocess
import sys
import json
import requests
from setuptools import setup, find_packages
from setuptools.command.install import install

class CustomInstallCommand(install):
    def run(self):
        # Call the original install command
        install.run(self)

        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Define paths
        tools_dir = os.path.join(current_dir, 'tools')
        apktool_dir = os.path.join(tools_dir, 'apktool')
   

        # Create tools directory if not exists
        os.makedirs(tools_dir, exist_ok=True)

        # Install APKTool
        if not os.path.exists(apktool_dir):
            os.makedirs(apktool_dir, exist_ok=True)
            apktool_jar = os.path.join(apktool_dir, 'apktool.jar')
            apktool_url = 'https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.7.0.jar'
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
            response = requests.get(apktool_url)
            with open(apktool_jar, 'wb') as file:
                file.write(response.content)
            with open(os.path.join(apktool_dir, 'apktool.bat' if os.name == 'nt' else 'apktool'), 'w') as f:
                f.write(f'java -jar {apktool_jar} %*')
            if os.name != 'nt':
                os.chmod(os.path.join(apktool_dir, 'apktool'), 0o755)

        # Save paths to a configuration file
        config = {
            'apktool_dir': apktool_dir,
           
        }
        with open(os.path.join(current_dir, 'tools_config.json'), 'w') as config_file:
            json.dump(config, config_file)

        print("Setup completed! All tools and dependencies have been installed locally.")

setup(
    name='apkmech-tools',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'rich',
        'androguard'
    ],
    cmdclass={
        'install': CustomInstallCommand,
    },
)
