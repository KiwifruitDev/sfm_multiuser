# SFM Multiuser
# =====================
# MIT License
# 
# Copyright (c) 2023 KiwifruitDev
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import datamodel, random, os, threading, time, sys, json

print("SFM Multiuser by KiwifruitDev")

# Seed the random number generator
random.seed()

cwd = os.getcwd()

config = {}

# Load config.json
if os.path.exists(os.path.join(cwd, "multiuser.json")):
    with open(os.path.join(cwd, "multiuser.json"), "r") as f:
        config = json.load(f)
else:
    # Generate config.json
    print("No config.json found.\nThe config will always be saved in the script directory. (multiuser.json)\nGenerating all possible config options...")
    config["repo_name"] = input("Enter repo name, this is where the project files are stored: ")
    #config["repo_push"] = input("Do you want to use the psuedoname author system? This is only needed if you're not pushing to a remote repository. (y/n): ")
    config["repo_existing"] = input("Can you clone your repository? If you've just created a remote, you can't clone from it immediately. (y/n): ")
    config["repo_remote"] = input("Enter the remote URL ending in .git (if any): ")
    #config["repo_readme"] = input("Do you want to add a README.md? This will ensure Git push calls can be made. (y/n): ")
    #print("Psuedoname author system (Ignore if disabled):")
    #config["author_first_name"] = input("Enter your Git first name (leave blank to generate a psuedoname): ")
    #config["author_last_name"] = input("Enter your Git last name: ")
    #config["author_email"] = input("Enter your Git email: ")
    config["sessions"] = input("Enter unique session names to track, separated by , (e.g. 'my_session,session2'): ")
    config["source2"] = input("Are you using Source 2? (y/n): ")
    print("Saving config.json...")
    with open(os.path.join(cwd, "multiuser.json"), "w") as f:
        json.dump(config, f, indent=4)

class Author():
    def __init__(self, first=None, last="", email=None):
        if not first and email:
            first = email.split("@")[0].split(".")[0].capitalize()
        if not first:
            first = "Unknown"
        self.first = first
        self.last = last
        if email is None:
            email = first.lower() + (last != "" and "." or "") + last.lower() + "@sfm-multi.us"
        self.email = email

    def git_name(self):
        return self.first + (self.last != "" and " " or "") + self.last + " <" + self.email + ">"

class NameGenerator():
    first_names = [
        "Aardvark", "Baboon", "Camel",
        "Dingo", "Elephant", "Ferret",
        "Giraffe", "Hippo", "Iguana",
        "Jackal", "Koala", "Lemur",
        "Mongoose", "Newt", "Ocelot",
        "Panda", "Quail", "Rabbit",
        "Snake", "Tiger", "Uakari",
        "Vulture", "Wallaby", "Xerus",
        "Yak", "Zebra",
    ]

    last_names = [
        "Apple", "Banana", "Cantaloupe",
        "Dragonfruit", "Elderberry", "Fig",
        "Grapefruit", "Honeydew", "Iceberg",
        "Jackfruit", "Kiwi", "Lemon",
        "Mango", "Nectarine", "Orange",
        "Papaya", "Quince", "Raspberry",
        "Strawberry", "Tangerine", "Ugli",
        "Vanilla", "Watermelon", "Xigua",
        "Yuzu", "Zucchini",
    ]

    def __init__(self):
        pass
    
    def generate_name(self):
        first = self.first_names[random.randint(0, len(self.first_names) - 1)]
        last = self.last_names[random.randint(0, len(self.last_names) - 1)]
        return Author(first, last)

globalNameGenerator = NameGenerator()

class Git():
    remote = False
    remoteSetup = False
    useAuthor = False
    writing = False

    def __init__(self, repo_path):
        self.repo_path = repo_path
        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)
        useAuthor = "y" #config["repo_push"]
        if useAuthor != "y":
            print("Author system is enabled.")
            self.useAuthor = True
            author = self.getAuthor()
            if not author:
                author = self.promptAuthor()
            self.author = author
        self.repo_path = repo_path
        os.chdir(self.repo_path)
        dontSetupRemote = False
        if not os.path.exists(os.path.join(self.repo_path, ".git")):
            dontSetupRemote = True
            print("Initializing git repository...")
            remote = config["repo_remote"]
            if remote != "":
                existing = config["repo_existing"]
                if existing == "y":
                    os.system("git clone %s" % remote)
                else:
                    os.system("git init")
                    os.system("git remote add origin %s" % remote)
                    # Prompt to add readme
                    should = "y" #config["repo_readme"]
                    if should == "y":
                        dontSetupRemote = False
                        with open("README.md", "w") as f:
                            f.write("# %s\n\nThis repository was created by SFM Multiuser." % self.repo_path)
                        os.system("git add README.md")
                        os.system("git commit -m \"Added README.md\"")
                        os.system("git push --set-upstream origin main")
        # Query git for remote
        self.remoteSetup = os.popen("git remote get-url origin").read().strip()
        if self.remoteSetup != "" and not dontSetupRemote:
            self.remote = True
        os.chdir(cwd)
    
    def add(self, file_path):
        os.chdir(self.repo_path)
        os.system("git add \"%s\"" % file_path)
        os.chdir(cwd)

    def commit(self, message="Changed by SFM Multiuser"):
        os.chdir(self.repo_path)
        sys_string = "git commit -m \"%s\"%s" % (message, self.useAuthor and " --author=\"%s\"" % self.author.git_name() or "")
        if not self.remote and self.remoteSetup:
            os.system("git push --set-upstream origin main")
        os.system(sys_string)
        os.chdir(cwd)

    def push(self):
        if self.remote:
            os.chdir(self.repo_path)
            os.system("git push")
            os.chdir(cwd)

    def pull(self, files_tracked):
        if self.remote:
            self.writing = True
            os.chdir(self.repo_path)
            # Pull silently and wait for it to finish
            os.popen("git pull").read()
            os.chdir(cwd)
            # Search every root folder in cwd for an "elements" folder
            for folder in os.listdir(os.path.join(cwd, "..", "game")):
                # Is this a folder?
                if not os.path.isdir(os.path.join(cwd, "..", "game", folder)):
                    continue
                # Make sure it's not our own repo
                if folder == config["repo_name"]:
                    continue
                # Does this folder have a sessions folder?
                if os.path.exists(os.path.join(cwd, "..", "game", folder, "elements", "sessions")):
                    # Check if any of the sessions are in this folder
                    for i in range(len(files_tracked)):
                        session = os.path.basename(files_tracked[i][0])
                        # Does this session exist in this folder?
                        if not os.path.exists(os.path.join(cwd, "..", "game", folder, "elements", "sessions", session)):
                            continue
                        # Copy the session file
                        dm = datamodel.load(os.path.join(self.repo_path, "elements", "sessions", session))
                        try:
                            dm.write(os.path.join(cwd, "..", "game", folder, "elements", "sessions", session), "binary", (config["source2"] == "y" and 9 or 5))
                            # Write timestamp to files_tracked[i][1]
                            files_tracked[i][1] = os.path.getmtime(os.path.join(cwd, "..", "game", folder, "elements", "sessions", session))
                        except:
                            pass
            self.writing = False
        return files_tracked

    def createAuthor(self):
        # Create author.txt with first, last, and email
        author = globalNameGenerator.generate_name()
        email = author.first.lower() + "." + author.last.lower() + "@sfm-multi.us"
        author_file = open(os.path.join(self.repo_path, "multiuser", "author.txt"), "w")
        print("Creating psuedoname %s %s <%s>" % (author.first, author.last, email))
        author_file.write("%s\n%s\n%s" % (author.first, author.last, email))
        author_file.close()
        return author

    def getAuthor(self):
        try:
            author_file = open(os.path.join(self.repo_path, "multiuser", "author.txt"), "r")
            lines = author_file.readlines()
            author = Author(lines[0].strip(), lines[1].strip(), lines[2].strip())
            author_file.close()
        except:
            author = None
        return author

    def promptAuthor(self):
        print("Creating a new author.txt for SFM Multiuser...")
        first = config["author_first_name"]
        if first == "":
            return self.createAuthor()
        last = config["author_last_name"]
        email = config["author_email"]
        author_file = open(os.path.join(self.repo_path, "multiuser", "author.txt"), "w")
        author_file.write("%s\n%s\n%s" % (first, last, email))
        author_file.close()
        author = Author(first, last, email)
        return author

class SourceControl():
    # This class tracks a file for changes
    git = None
    files_tracked = []
    searchPaths = []

    def __init__(self, repo_name, files):
        self.repo_folder = os.path.join(cwd, "..", "game", repo_name)
        if not os.path.exists(self.repo_folder):
            os.makedirs(self.repo_folder)
        # Git init
        self.git = Git(self.repo_folder)
        self.session_folder = os.path.join(self.repo_folder, "elements", "sessions")
        if not os.path.exists(self.session_folder):
            os.makedirs(self.session_folder)
        # Start change thread
        for file in files:
            # Is file blank space?
            if file == "":
                continue
            # If file doesn't end in .dmx, add it
            if not file.endswith(".dmx"):
                file += ".dmx"
            # Search every root folder in cwd for an "elements" folder
            for folder in os.listdir(os.path.join(cwd, "..", "game")):
                # Is this a folder?
                if not os.path.isdir(os.path.join(cwd, "..", "game", folder)):
                    continue
                # Make sure it's not our own repo
                if folder == repo_name:
                    continue
                # Does this folder have an "elements" folder?
                if os.path.exists(os.path.join(cwd, "..", "game", folder, "elements")):
                    self.searchPaths.append(folder)
            # Search through searchpaths for file
            found = False
            search = ""
            for path in self.searchPaths:
                search = os.path.join(cwd, "..", "game", path, "elements", "sessions", file)
                if os.path.exists(search):
                    found = True
                    break
            # If file doesn't exist
            if not found:
                print("Session does not exist and won't be tracked: " + file)
                continue
            print("Session found: " + file)
            self.files_tracked.append([search, os.path.getmtime(search)])
        if len(self.files_tracked) == 0:
            print("No files to track, exiting...")
            sys.exit()
        else:
            self.change_thread = threading.Thread(target=self.change_thread)
            self.change_thread.start()
            print("Ready")
            while True:
                # Join for 0.1 second
                try:
                    self.change_thread.join(0.1)
                except KeyboardInterrupt:
                    print("Exiting...")
                    sys.exit()

    def isChanged(self, index):
        if self.git.writing:
            return False
        timestamp = os.path.getmtime(self.files_tracked[index][0])
        changed = timestamp != self.files_tracked[index][1]
        self.files_tracked[index][1] = timestamp
        return changed
        
    # Periodically pull at 5 second intervals
    tick = 0
    
    def change_thread(self):
        while True:
            for i in range(len(self.files_tracked)):
                if self.git.writing:
                    time.sleep(0.1)
                if self.isChanged(i):
                    self.on_change(i)
                if self.tick >= 50:
                    self.files_tracked = self.git.pull(self.files_tracked)
                    self.tick = 0
            self.tick += 1
            time.sleep(0.1)

    def on_change(self, index):
        self.git.writing = True
        # Turn self.files_tracked[index][0] into relative path
        relPath = os.path.relpath(self.files_tracked[index][0], cwd)
        relPath = os.path.join(*relPath.split(os.path.sep)[1:])
        relPath = os.path.join(*relPath.split(os.path.sep)[1:])
        relPath = os.path.join(*relPath.split(os.path.sep)[1:])
        print("File timestamp updated: " + relPath)
        # Remove user data
        dm = datamodel.load(self.files_tracked[index][0])
        dm.root["activeClip"] = None
        dm.root["settings"] = None
        gitPath = os.path.join(self.git.repo_path, relPath)
        os.makedirs(os.path.dirname(gitPath), exist_ok=True)
        try:
            dm.write(self.files_tracked[index][0], "binary", (config["source2"] == "y" and 9 or 5))
            dm.write(gitPath, "keyvalues2", 1)
        except:
            print("Failed to write file: " + relPath)
            self.git.writing = False
            return
        # Add to git
        self.git.add(relPath)
        self.git.commit("Changed by SFM Multiuser")
        self.git.push()
        # Update last modified
        self.files_tracked[index][1] = os.path.getmtime(self.files_tracked[index][0])
        self.git.writing = False

globalMultiuser = SourceControl(config["repo_name"], config["sessions"].split(","))
