from .exception import PathOverRootError
import os

def is_subpath(root, sub):
    root = os.path.abspath(root)
    sub = os.path.abspath(sub)
    return sub.startswith(root)

def remove_prefix(string, prefix):
    if string.startswith(prefix):
        return string[len(prefix):]
    else:
        return string

class VirtualPath:
    def __init__(self, virtual: str):
        self.path = virtual
        self.absolute = False
        if virtual.startswith("/"):
            self.absolute = True

    def to_local_path(self, work_dir, root_dir):
        if not self.absolute:
            path = os.path.join(work_dir, self.path)
        else:
            path = os.path.join(root_dir, self.path[1:])

        if is_subpath(root_dir, path):
            return os.path.normpath(path)
        else:
            raise PathOverRootError(path)
            
    def __str__(self):
        return self.path

def local_to_virtual_abs(local_path, root_dir):
    if not is_subpath(root_dir, local_path):
        raise PathOverRootError(local_path)
    local_path = os.path.abspath(local_path)
    removed = remove_prefix(local_path, root_dir)
    if removed == "":
        return "/"
    else:
        return removed