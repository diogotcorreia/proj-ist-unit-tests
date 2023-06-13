# MML Compiler - Tests

This folder contains tests for the 1st (and only) project (MML Compiler) for Comp 2022/2023.

## Available Tests

There are two kinds of tests: those in the `ok` folder are expected to compile and execute,
and their output should match the corresponding `.out`'s file content.
On the other hand, those in the `nok` folder are expected to not compile at all, which is used
to test if the right assertions are being made by the compiler.

## Clone this repository

Start by cloning this repository using `git`.  
**DO NOT CLONE THIS INSIDE YOUR OTHER PROJECT FOLDER**  
You can clone this anywhere in your system (other than your project folder).

```bash
git clone https://github.com/diogotcorreia/proj-ist-unit-tests.git
```

## Run the tests

You can use the attached script, `test.sh` to run all the tests.

Usage:

```
usage: ./test.sh [flags] <path to executable>
-d display diff in the terminal
-c clean generated result files instead of testing
-x output xml instead of generating asm
-h help - shows this message
```

## Update the tests

The tests will be updated frequently on this repository.
To make sure you're running an up-to-date copy, just pull from the repository using:

```bash
git pull
```

## Running the official tests

The `test.sh` script can be used to run the official tests as well.

To do that, simply create a `official-tests` symlink to the `auto-tests`
directory of the official testing repository.  
For example:

```sh
ln -s ~/path/to/CO23/auto-tests ./official-tests
```

## Troubleshooting

### Cannot find -lrts

If you're getting the following error while running the tests,

```
ld: cannot find -lrts: No such file or directory
```

it is because you do not have RTS installed system-wide.

Newer versions of the script also try to automatically find RTS in the
`$HOME/compiladores/root` folder.

To get around this, you need to tell `ld` where RTS is.
To achieve this, set the `LD_EXTRA_FLAGS` env var to the folder containing the RTS.

Therefore, run the following command before executing the test script
(replace `<ROOT>` with the same `ROOT` in your Makefile).

```bash
export LD_EXTRA_FLAGS="-L<ROOT>/usr/lib"
```

## Contribute

Community tests are _extremely_ welcome!
Feel free to submit a PR.
