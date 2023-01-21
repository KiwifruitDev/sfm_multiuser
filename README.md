# SFM Multiuser

*Prepare for trouble, and make it double!*

This is a Python 3 script that allows you to quickly create, commit, push and pull from Git repositories for Source Filmmaker.

This script works for both the Source 1 and Source 2 versions of SFM.

## Requirements

- [Python 3](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

## Installation

1. Clone this repository to your computer in SFM's `SourceFilmmaker` folder. This should create an `sfm_multiuser` folder next to your `game` folder.
2. Open the `sfm_multiuser` folder and run `start.bat` to start the script.
3. Follow the instructions in the script to set up your Git repository and user.
4. Open a session specified in one of your `elements\sessions` folders.
5. Any time the file is modified, the script will automatically commit and push the changes to your Git repository.

## Helper Script

For Source 1 users, there is a helper script to reload the session file.

This can be accessed by adding the repo name to your `gameinfo.txt` and opening the script from "Scripts" > "KiwifruitDev" > "Multiuser"

## Avoid Map Loading

To avoid loading the map every time the session is loaded, simply remove the map from `mapname` in the `activeClip` property in the element viewer.

This will require users to load the map manually via console, or through my [Asset Browser](https://steamcommunity.com/sharedfiles/filedetails/?id=2918590103)

## References

- datamodel.py
