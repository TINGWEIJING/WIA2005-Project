# WIA2005-Project
## TOC
- [Installation](#installation)
- [Run](#run)
- [Target Features](#target-features)
- [Gits Commands](#gits-commands)

## Installation
- Create venv with the name venv
```bash
py -m venv venv
```
- Activate venv
```bash
venv\Scripts\activate
```
- Install required library
```bash
py -m pip install -r requirements.txt
```

## Run
- Using CMD
```bash
venv\Scripts\activate
set FLASK_APP=core
set FLASK_ENV=development
flask run
```
- Using Power Shell
```bash
venv\Scripts\activate
$env:FLASK_APP = "core"
$env:FLASK_ENV = "development"
flask run
```

## Target Features

## Gits Commands
- Clone repo
```git
git clone url
```

- Update all local branches
```git
git pull --all
```

- Create a new local branch
```git
git branch branch_name
```

- List all local branches
```git
git branch
```

- Switch local branch
```git
git checkout branch_name
```

- Push a new local branch to remote branch
```git
git push -u origin branch_name
```

- Add all files in staging area
```git
git add .
```

- Check git status
```git
git status
```

- Commit changes with a message
```git
git commit -m "your commit message here"
```

- Push changes
```git
git push
```

- Delete branch
```git
git branch -d branch_name
```

- Remove a remote branch
```git
git push --delete origin branch_name_here
```

- Show commit history
```git
git log --graph --oneline --all
```

- Rollback previous commit
```git
git revert comit_id_here
```



