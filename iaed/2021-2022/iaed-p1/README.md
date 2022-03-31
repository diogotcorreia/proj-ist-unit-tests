# IAED Proj1 custom tests

A repo with custom tests for the first project of IAED

Automatically test with the script:
```
./test.sh [flags] <path to executable> <path to tests dir>
```
- `-d` flag shows in the terminal the diff of expected output with actual output (if `colordiff` is installed, this diff will be colorized)<br>

- `-c` flag removes generated `.result` files (instead of testing)

- `-v` flag runs tests in valgrind

- `-h` flag (as usual) shows this information

**Note**: Custom tests are often made to test a single functionality and not the entire program, this also reduces the risk of creating wrong tests.

Feel free to contribute custom tests and report wrong ones
