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

## Contribute

Community tests are _extremely_ welcome!
Feel free to submit a PR.
