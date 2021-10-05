import sys
from requests import get
from pathlib import Path

raw  = "https://raw.githubusercontent.com/EleoEris/custom-cmd/main/README.md"
norm = "https://github.com/EleoEris/custom-cmd/blob/main/README.md"

def print_help():
        print("Useful git commands")
        print("clone1 link path         - clones a single file from github")
        print("                         - link - mandatory - link to the file")
        print("                         - path - where to store the file")
        print("clone1 user repo file    - details of repository")

def main(cmd):
    path = ""
    
    if len(cmd) == 0 or cmd[0] == '--help' or cmd[0] == '-h' or cmd[0] == '/?':
        print_help()
        return(0)
        
    if cmd[0] == 'clone1':              ### Clone a single file from github
                                        ### cmd[1] - link, (cmd[2] - path) or
                                        ### cmd[1] - username, cmd[2] - repo, cmd[3] - branch, cmd[4] - file name, (cmd[5] - path)
        if "github.com" in cmd[1]:      ### User has provided a link
            link = cmd[1].replace("github.com", "raw.githubusercontent.com").replace("blob/", "")
            try:
                path = cmd[2]
            except IndexError:  ### path was not given
                pass
        else:
            try:
                link = f"https://raw.githubusercontent.com/{cmd[1]}/{cmd[2]}/{cmd[3]}/{cmd[4]}"
                try:            ### path was not given
                    path = cmd[5]
                except IndexError:
                    pass
            except IndexError:
                print("Not a github link. Please provide a github link or (in order) the username, repository name, branch and file name")
        if not "link" in locals():
            print("Some error occurred!")
            return(1)
        request = get(link)
        if request.status_code == 200:
            if path:
                with open(path, "w") as output:
                    output.write(request.text)
                    print(f"Saved file successfully to {output.name}.")
            else:
                with open(link[link.rindex("/") + 1:], "w") as output:
                    output.write(request.text)
                    print(f"Saved file successfully to {Path(output.name).resolve()}.")
        else:
            print(f"Couldn't get file from link. Status code: {request.status_code}.\n Please check your input or try visiting the link yourself.\n{link}")


if __name__ == '__main__':
    main(sys.argv[2:]) ### First 2 arguments are path and script name - not necessary
