#include "fs/operations.h"
#include <assert.h>
#include <errno.h>
#include <fcntl.h>
#include <pthread.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

#define BUFFER_LEN 120

#define FILE_COUNT 4

char *input_files[] = {
    "input1.txt",
    "input2.txt",
    "input3.txt",
    "input4.txt",
};
char *tfs_files[] = {"/f1", "/f2", "/f3", "/f4"};

void *write_to_file(void *input);
void check_if_file_was_correctly_written(char *input_file, char *tfs_file);

/* This test creates multiple files simultaneously and fill them up with
 * different content. Additionally, various writes are performed that may go
 * over blocks (spill), making sure there is thread-safety when using tfs_write
 * over multiple data blocks. Finally, the contents of each file are read and
 * compared with the original files. */
int main() {
    assert(tfs_init() != -1);

    pthread_t tid[FILE_COUNT];
    int file_id[FILE_COUNT];

    for (int i = 0; i < FILE_COUNT; ++i) {
        file_id[i] = i;
        assert(pthread_create(&tid[i], NULL, write_to_file,
                              (void *)(&file_id[i])) == 0);
    }

    for (int i = 0; i < FILE_COUNT; ++i) {
        assert(pthread_join(tid[i], NULL) == 0);
    }

    for (int i = 0; i < FILE_COUNT; ++i) {
        check_if_file_was_correctly_written(input_files[i], tfs_files[i]);
    }

    printf("Successful test.\n");
    assert(tfs_destroy() == 0);
    return 0;
}

void *write_to_file(void *input) {
    int file_id = *((int *)input);

    // open source file
    FILE *fd = fopen(input_files[file_id], "r");
    assert(fd != NULL);

    char buffer[BUFFER_LEN];
    char *path = tfs_files[file_id];

    int f = tfs_open(path, TFS_O_CREAT);
    assert(f != -1);

    /* read the contents of the file */
    ssize_t r;
    size_t bytes_read = fread(buffer, sizeof(char), BUFFER_LEN, fd);

    while (bytes_read > 0) {
        r = tfs_write(f, buffer, bytes_read);
        assert(r == bytes_read);
        bytes_read = fread(buffer, sizeof(char), BUFFER_LEN, fd);
    }

    assert(tfs_close(f) == 0);
    assert(fclose(fd) == 0);
    return NULL;
}

void check_if_file_was_correctly_written(char *input_file, char *tfs_file) {
    FILE *fd = fopen(input_file, "r");
    assert(fd != NULL);

    char buffer_external[BUFFER_LEN];
    char buffer_tfs[BUFFER_LEN];

    int f = tfs_open(tfs_file, 0);
    assert(f != -1);

    size_t bytes_read_external =
        fread(buffer_external, sizeof(char), BUFFER_LEN, fd);
    ssize_t bytes_read_tfs = tfs_read(f, buffer_tfs, BUFFER_LEN);
    while (bytes_read_external > 0 && bytes_read_tfs > 0) {
        assert(strncmp(buffer_external, buffer_tfs, BUFFER_LEN) == 0);
        bytes_read_external =
            fread(buffer_external, sizeof(char), BUFFER_LEN, fd);
        bytes_read_tfs = tfs_read(f, buffer_tfs, BUFFER_LEN);
    }

    // check if both files reached the end
    assert(bytes_read_external == 0);
    assert(bytes_read_tfs == 0);

    assert(tfs_close(f) == 0);
    assert(fclose(fd) == 0);
}
