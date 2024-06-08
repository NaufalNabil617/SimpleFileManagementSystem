# Import modul tabulate untuk menampilkan tabel dengan baik
from tabulate import tabulate # lakukan perintan pip install tabulate bila belum menginstal

class File:
    def __init__(self, name):
        self.name = name
        self.content = ""
        self.size = 0

    def write(self, text):
        self.content += text
        self.size += len(text)

    def resize(self, new_size):
        if new_size < self.size:
            self.content = self.content[:new_size]
        self.size = new_size

class Directory:
    def __init__(self, name):
        self.name = name
        self.subdirs = {}
        self.files = {}

class FileSystem:
    def __init__(self):
        self.root = Directory("root")
        self.current_dir = self.root
        self.dir_stack = [self.root]
        self.log = []

    def get_current_path(self):
        path_elements = [dir.name for dir in self.dir_stack]
        return "/".join(path_elements)

    def print_directory(self, directory=None, indent=0):
        if directory is None:
            directory = self.current_dir
        print("  " * indent + f"[DIR] {directory.name}")
        for subdir in directory.subdirs.values():
            self.print_directory(subdir, indent + 1)
        for file in directory.files.values():
            print("  " * indent + f"[FILE] {file.name} (size: {file.size} bytes)")

    def change_directory(self, path):
        if path == ".." or path == "-":
            if len(self.dir_stack) > 1:
                self.dir_stack.pop()
                self.current_dir = self.dir_stack[-1]
            else:
                print("Already at the root directory.")
        else:
            if path in self.current_dir.subdirs:
                self.current_dir = self.current_dir.subdirs[path]
                self.dir_stack.append(self.current_dir)
            else:
                print(f"Directory '{path}' does not exist.")
        self.log.append(f"chdir {path}")

    def make_directory(self, name):
        if name in self.current_dir.subdirs:
            print(f"Directory '{name}' already exists.")
        else:
            self.current_dir.subdirs[name] = Directory(name)
            self.log.append(f"mkdir {name}")

    def remove_directory(self, name):
        if name in self.current_dir.subdirs:
            del self.current_dir.subdirs[name]
            self.log.append(f"rmdir {name}")
        else:
            print(f"Directory '{name}' does not exist.")

    def move_directory(self, name, new_path):
        if name in self.current_dir.subdirs:
            if new_path in self.current_dir.subdirs:
                self.current_dir.subdirs[new_path].subdirs[name] = self.current_dir.subdirs.pop(name)
                self.log.append(f"mvdir {name} {new_path}")
            else:
                print(f"Target directory '{new_path}' does not exist.")
        else:
            print(f"Directory '{name}' does not exist.")

    def make_file(self, name):
        if name in self.current_dir.files:
            print(f"File '{name}' already exists.")
        else:
            self.current_dir.files[name] = File(name + ".txt")
            self.log.append(f"mkfil {name}")

    def remove_file(self, name):
        if name in self.current_dir.files:
            del self.current_dir.files[name]
            self.log.append(f"rmfil {name}")
        else:
            print(f"File '{name}' does not exist.")

    def rename_file(self, old_name, new_name):
        if old_name in self.current_dir.files:
            self.current_dir.files[new_name] = self.current_dir.files.pop(old_name)
            self.current_dir.files[new_name].name = new_name + ".txt"
            self.log.append(f"mvfil {old_name} {new_name}")
        else:
            print(f"File '{old_name}' does not exist.")

    def write_to_file(self, name, text):
        if name in self.current_dir.files:
            if text.startswith('"') and text.endswith('"'):
                self.current_dir.files[name].write(text[1:-1])
                self.log.append(f"write {name} {text}")
            else:
                print("Text to write must be enclosed in double quotes.")
        else:
            print(f"File '{name}' does not exist.")

    def view_and_edit_file(self, name):
        if name in self.current_dir.files:
            file = self.current_dir.files[name]
            print(f"Viewing file '{file.name}':")
            print(file.content)  # Menampilkan teks sebelumnya
            edit = input("Do you want to edit this file? (yes/no): ")
            if edit.lower() == "yes":
                new_content = input("Enter new content to append (enclose in double quotes): ")
                if new_content.startswith('"') and new_content.endswith('"'):
                    file.write(new_content[1:-1])
                    self.log.append(f"write {name} {new_content}")
                    print(f"Content written to file '{file.name}'.")
                else:
                    print("Text to write must be enclosed in double quotes.")
        else:
            print(f"File '{name}' does not exist.")


    def undo(self):
        if not self.log:
            print("No actions to undo.")
            return
        
        last_command = self.log.pop()
        cmd, *args = last_command.split()
        
        if cmd == "mkdir":
            self.remove_directory(args[0])
        elif cmd == "rmdir":
            print(f"Cannot undo remove directory '{args[0]}' automatically.")
        elif cmd == "mkfil":
            self.remove_file(args[0])
        elif cmd == "rmfil":
            print(f"Cannot undo remove file '{args[0]}' automatically.")
        elif cmd == "chdir":
            self.change_directory("..")
        elif cmd == "mvdir":
            self.move_directory(args[0], "..")
        elif cmd == "mvfil":
            self.rename_file(args[1], args[0])
        elif cmd == "write":
            file_name, written_text = args[0], ' '.join(args[1:])
            if file_name in self.current_dir.files:
                self.current_dir.files[file_name].content = self.current_dir.files[file_name].content.replace(written_text, '', 1)
                self.current_dir.files[file_name].size -= len(written_text)
        print(f"Undid action: {last_command}")

    def exit(self):
        print("Exiting the program.")
        exit(0)

    def initialize_root(self):
        self.current_dir = self.root
        self.dir_stack = [self.root]
        print("Root directory initialized.")
    
    def print_kelompok_8_os(self):
        kelompok_8_os = """
  
  _  __  ______   _         ____    __  __   _____     ____    _  __     ___       ____     _____ 
 | |/ / |  ____| | |       / __ \  |  \/  | |  __ \   / __ \  | |/ /    / _ \     / __ \   / ____|
 | ' /  | |__    | |      | |  | | | \  / | | |__) | | |  | | | ' /    | (_) |   | |  | | | (___  
 |  <   |  __|   | |      | |  | | | |\/| | |  ___/  | |  | | |  <      > _ <    | |  | |  \___ \ 
 | . \  | |____  | |____  | |__| | | |  | | | |      | |__| | | . \    | (_) |   | |__| |  ____) |
 |_|\_\ |______| |______|  \____/  |_|  |_| |_|       \____/  |_|\_\    \___/     \____/  |_____/ 
                                                                                                  
        """
        print(kelompok_8_os)

def main():

    fs = FileSystem()
    fs.print_kelompok_8_os()
    
    commands = [
        ["root", "initialize root directory"],
        ["print", "print current working directory and all descendants"],
        ["chdir <dir>", "change current working directory (.. refers to parent directory)"],
        ["chdir-", "change to parent directory"],
        ["mkdir <name>", "sub-directory create"],
        ["rmdir <name>", "delete a directory"],
        ["mvdir <name> <path>", "move a directory"],
        ["mkfil <name>", "file create"],
        ["rmfil <name>", "file delete"],
        ["mvfil <old> <new>", "file rename"],
        ["viewedit <name>", "view and edit a file"],
        ["write <name> <text>", "write to file"],
        ["undo", "undo last command"],
        ["exit", "quit the program"]
    ]

    print("Available commands:")
    print(tabulate(commands, headers=["Command", "Description"], tablefmt="fancy_grid"))


    commands = {
        "root": fs.initialize_root,
        "print": fs.print_directory,
        "chdir": fs.change_directory,
        "chdir-": lambda: fs.change_directory(".."),
        "mkdir": fs.make_directory,
        "rmdir": fs.remove_directory,
        "mvdir": fs.move_directory,
        "mkfil": fs.make_file,
        "rmfil": fs.remove_file,
        "mvfil": fs.rename_file,
        "viewedit": fs.view_and_edit_file,
        "write": fs.write_to_file,
        "undo": fs.undo,
        "exit": fs.exit
    }

    while True:
        current_path = fs.get_current_path()
        cmd = input(f"({current_path}) Enter command: ").strip().split(" ", 2)
        if cmd[0] in commands:
            if cmd[0] in ["chdir", "mkdir", "rmdir", "mvdir", "mkfil", "rmfil", "mvfil", "viewedit"]:
                if len(cmd) < 2:
                    print("Missing argument.")
                else:
                    commands[cmd[0]](*cmd[1:])
            elif cmd[0] == "write":
                if len(cmd) < 3:
                    print("Missing argument.")
                else:
                    filename = cmd[1]
                    text = cmd[2]
                    commands[cmd[0]](filename, text)
            else:
                commands[cmd[0]]()
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()
