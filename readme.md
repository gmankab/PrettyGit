# prettygit by gmanka

<img src="https://github.com/gmankab/prettygit/raw/main/img/transparent.png">

user-friendly interface for git, supports commits, pushes, and uploading to [pipy.org](https://pypi.org)

## navigation

- [installation](#installation)
- [installation via terminal](#installation-via-terminal)
- [help](#help)
- [license](#license)


### installation

[prettygit.sh](https://gmankab.github.io/prettygit.sh) - for linux  
[prettygit.bat](https://gmankab.github.io/prettygit.bat) - for windows

### installation via terminal

install on linux:  
`curl -sSL gmankab.github.io/prettygit.sh | sh`

install on any os:  
`pip install prettygit`

launch on any os:  
`python -m prettygit`


### help

to use the script, you do not have to read what is written below

these are just optional arguments you can specify when you run the script

```
   args:  -h | --help
   info:  get help
example:  prettygit --help
```

```
   args:  -b | --branch                      
   info:  set branch for pushing            
example:  prettygit --branch main
```

```
   args:  -r | --remote                         
   info:  set remote for pushing               
example:  prettygit --remote origin
```

```
   args:  -m | --message | --commit_message
   info:  set commit message
example:  prettygit --commit_message aboba
```

```
    args:  -g | --git_path
    info:  permanently set new path for git
examples:  prettygit --git_path /bin/git
           prettygit --git_path D:\\git\\git.exe
```

### changelog[^](#navigation)

you can read changelog [here](https://github.com/gmankab/prettygit/blob/main/changelog.md)


## license

[gnu gpl 3](https://gnu.org/licenses/gpl-3.0.en.html)
