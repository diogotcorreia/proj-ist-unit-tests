# Tests for the 2nd IAED Project

This directory contains some community and the public tests for the second IAED project. 

Automatically test with the script:
```
./test.sh [flags] <path_to_executable> <path_to_tests_dir>
```
- `-d` flag shows in the terminal the diff of expect output with actual output(if `colordiff` is installed, this diff will be colorized)
- `-c` flag removes generated `.result` files (instead of testing)
- **`-v` flag runs tests in valgrind**
- `-h` flag (as usual) shows this information

Alternatively, if your executable file `proj2` is located in the root of this directory, you can run `make` in each tests' directory. `make clean` will clear generated files.
This is a more efficient alternative, however, not too significant for the amount of available tests.

