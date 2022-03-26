# lid-Driven Cativy flow solver

Simple CFD solver with user interface written in Python.

The API could contain functionality for the following:

- Easily configurable parameters like gravity, jump velocity, walking speed, etc.
- Hooks for terrain generation.

## How to Run

Recommended pre-installation of ```Anaconda enviroment

```shell
git clone https://github.com/PRIDEmartins/Code.git
python CAVITY_FLOW.py
```

### If you don't have pip or git

For pip:

- Mac or Linux: install with `sudo easy_install pip` (Mac or Linux) - or (Linux) find a package called 'python-pip' in your package manager.
- Windows: [install Distribute then Pip](http://stackoverflow.com/a/12476379/992887) using the linked .MSI installers.

For git:

- Mac: install [Homebrew](http://mxcl.github.com/homebrew/) first, then `brew install git`.
- Windows or Linux: see [Installing Git](http://git-scm.com/book/en/Getting-Started-Installing-Git) from the _Pro Git_ book.

See the [wiki](https://github.com/fogleman/Minecraft/wiki) for this project to install Python, and other tips.

## How to run:

![alt text](https://1drv.ms/u/s!Ao2qdFkyoOVdjqQam3q_9aYB7eNgTg?e=4iHgbL)

### Moving

- W: forward
- S: back
- A: strafe left
- D: strafe right
- Mouse: look around
- Space: jump
- Tab: toggle flying mode

### Building

- Selecting type of block to create:
    - 1: brick
    - 2: grass
    - 3: sand
- Mouse left-click: remove block
- Mouse right-click: create block

### Quitting

- ESC: release mouse, then close window
