# Tests for IA (P4) project

This directory contains some community and the public tests for the IA (P4) project.

Automatically test with the script:

```
./test.sh [flags] <path_to_takuzu.py> <path_to_tests_dir>
```

- `-d` flag shows in the terminal the diff of expect output with actual output
- `-c` flag removes generated `.result` files (instead of testing)
- `-h` flag (as usual) shows this information

## Example

```bash
./test.sh -d ~/documents/takuzu-ia/takuzu.py public-tests
```
