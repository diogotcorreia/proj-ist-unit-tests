# IAED Proj1 custom tests

A repo with custom tests for the first project of IAED

Automatically test with the script:
```
./test.sh <relative_path_to_executable> <relative_path_to_tests_dir> <flags>
```
`-v` flag shows in the terminal the diff of expected output with actual output<br>

`-c` flag removes generated `.result` files

**Note**: Custom tests are often made to test a single functionality and not the entire program, this also reduces the risk of creating wrong tests.

Feel free to contribute custom tests and report wrong ones
