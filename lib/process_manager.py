import os
import asyncio

from tempfile import TemporaryDirectory
from lib.site_interface import SiteInterface

class ProcessManager:
    def __init__(self, site_interface: SiteInterface, config: dict):
        self.site_interface = site_interface
        self.process_wrapper_path = config.get("ProcessWrapperPath")

    def run(self, executable_path, args: list = None) -> str:
        remote_path = asyncio.run(self.site_interface.upload(executable_path))

        with open(self.process_wrapper_path, "r") as f:
            file_content = f.read().replace("[TRANSFER_DIR]", self.site_interface.transfer_dir)
        with TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, os.path.basename(self.process_wrapper_path))
            with open(temp_file_path, "w") as f:
                f.write(file_content)
            command = [remote_path]
            if args:
                command += args
            
            return asyncio.run(self.site_interface.run(temp_file_path, command))
