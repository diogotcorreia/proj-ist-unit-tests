# FileSystem IAED (Project 2) - Tests

This folder contains tests for the 2nd project (FileSystem) for IAED 2020/2021.

## FAQ

FAQs about the FileSystem project itself (not these tests) can be found on the [`FAQ.md`](./FAQ.md) file.

## Using this in your own project

To use this to test your own project, here are the requisites you must meet:

- Be running a Unix system (Linux or MacOS). This should also work on a VM and WSL.
- Have all your `.c` and `.h` in one folder.
- Have `git`, `diff`, `gcc` and `make`(\*) installed on your system (probably already installed).
- Have a Makefile in your project directory that compiles your project to a single executable(\*).

*(\*) = You only need this if you're using method #2.*

### Clone this repository

Start by cloning this repository using `git`.  
**DO NOT CLONE THIS INSIDE YOUR OTHER PROJECT FOLDER, ESPECIALLY IF THAT'S ALSO A GIT REPOSITORY**  
You can clone this anywhere in your system.

```bash
git clone https://github.com/diogotcorreia/proj-ist-unit-tests.git
```

### Method 1: Just Do It! by Raf (easier but less efficient)

1. Go to this projet's tests folder inside where you cloned this repository into (`cd proj-ist-unit-tests/iaed-p2`)
2. Run `./justdoit.sh PATH`, where PATH is where your `*.c` files are (for example, `../Proj2IAED/src`). Do **not** include a trailing slash. If you want to run valgrind with the tests add `valgrind` at the end (`./justdoit.sh PATH valgrind`).
3. That's it!

The script will create `.myout` and `.diff` files in the `tests/` directory so you can analyze them if you need to. To get rid of them, you can run `./justdoit.sh clean`.

### Method 2: Make files (more complex to setup but more efficient)

#### Configure

Then, you have to create the configuration file.
To do that, copy the `config.default` file to `config` and edit it accordingly.

```bash
cd proj-ist-unit-tests/iaedp2 # go into this projet's folder inside the repository's folder if you haven't already
cp config.default config # create the configuration file from the default
nano config # edit the file as you'd like. You can use another editor, like 'vim', 'code', etc. **(as long as it's not emacs)**
```

#### Run the tests

To run the tests, just run `make` in this repository's folder:

```bash
make
```

It will create various `.diff` files in the `tests` directory and tell you which tests fail and which tests pass.

### Whichever Method you Chose: Update the tests

The tests will be updated frequently on this repository.
To make sure you're running an up-to-date copy, just pull from the repository using:

```bash
git pull
```

## About the tests

There are two types of tests:

- Official tests (called `tXX.in`/`tXX.out`)  
  Made available by the teachers
- Community tests (called `ctXXX.in`/`ctXXX.out`)  
  Made by other students

### Contribute

Community tests are _extremely_ welcome!
Feel free to submit a PR.
