from pathlib import Path
from random import randbytes, randint
import sys

class AutoShredder():
    def __init__(self,
                 ### FOLDER TO SHRED
                 folder_name         : str,
                 ### FILES WILL BE MOVED TEMPORARILY TO A FOLDER WITH THIS NAME IF USING FOLDER
                 erasure_dir_name   = "to-shred"):
        self.target         = Path(folder_name)
        self.target_name    = folder_name
        self.erasure_dir    = Path(erasure_dir_name)

    def run(self): ### RETURNS EXIT STATUS
        try:
            if self.target.is_dir():
                self.erasure_dir.mkdir(exist_ok = True)
                self.shred_pt1(self.target)
                self.shred_pt2()
                print(f"Shredded {self.target_name}")
                return 0
            else:
                self.target.write_bytes(randbytes(len(self.target.read_bytes())))
                new_name = str(randint(10**150, 10**200))
                self.target.rename(new_name)
                Path(new_name).unlink()
                print(f"Shredded {self.target_name}")
        except Exception as e:
            print(e)
            return 1

    ### ITERATES shred_data OVER FILES
    def shred_pt1(self, folder: Path):
        for file in folder.iterdir():
            self.shred_data(file)
            
    ### OVERWRITES FILE DATA AND NAME WITH RANDOM VALUES
    ### AND PUTS THEM IN A TEMPORARY FOLDER erasure_dir
    def shred_data(self, file: Path):
        try:
            if file.is_dir():
                self.shred_pt1(file)
                file.rename(self.erasure_dir / str(randint(10**150, 10**200)))
            else:
                file.write_bytes(randbytes(len(file.read_bytes())))
                Path(file).rename(self.erasure_dir / str(randint(10**150, 10**200)))
        except FileExistsError:
            self.shred_data(file)

    ### DELETES THE TEMPORARY FOLDER
    def shred_pt2(self):
        ### I don't wanna import any more modules
        for file in self.erasure_dir.iterdir():
            if file.is_dir():
                file.rmdir()
            else:
                file.unlink()
        new_name = str(randint(10**150, 10**200))
        Path(self.target).rename(self.erasure_dir / new_name)
        (self.erasure_dir / new_name).rmdir()
        self.erasure_dir.rmdir()


def print_help():
        print("File shredder")
        print("Use this command with the name of (or path to) a file to shred it")


def main(cmd) -> int: # like cpp int main() {}
    # check if help was invoked
    if len(cmd) == 0 or cmd[0] == '--help' or cmd[0] == '-h' or cmd[0] == '/?':
        print_help()
        return 0

    # actual commands
    elif len(cmd) > 1:
        print("You passed too many variables:")
        for i, var in enumerate(cmd):
            print(f"{i}.\t{var}")
        print("Do not forget to put path in quotes \" \" if it contains a space")
        return 0
    else:
        shredder = AutoShredder(cmd[0])
        return shredder.run()

if __name__ == '__main__':
    main(sys.argv[2:])

