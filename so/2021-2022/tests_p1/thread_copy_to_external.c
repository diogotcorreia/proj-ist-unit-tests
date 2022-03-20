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

#define MAX_EXTERNAL_FILE_NAME 40
#define SAVE_COUNT_PER_FILE 8
#define THREAD_COUNT 6
#define FILE_COUNT 4

char *input_files[] = {
    "input1.txt",
    "input2.txt",
    "input3.txt",
    "input4.txt",
};
char *tfs_files[] = {"/f1", "/f2", "/f3", "/f4"};

void *write_to_file(void *input);
void *copy_external_thread(void *thread_i);
void check_if_file_was_correctly_written(int file_id);

/* Tests if the TFS files are copied to the external FS concurrently. After
 * copying, compares the contents between the original and the copy, deleting
 * the copy. */
int main() {
    assert(tfs_init() != -1);

    pthread_t tid[FILE_COUNT];
    int file_id[FILE_COUNT];

    // create files concurrently (not really a part of the test, but why not)
    for (int i = 0; i < FILE_COUNT; ++i) {
        file_id[i] = i;
        assert(pthread_create(&tid[i], NULL, write_to_file,
                              (void *)(&file_id[i])) == 0);
    }

    for (int i = 0; i < FILE_COUNT; ++i) {
        assert(pthread_join(tid[i], NULL) == 0);
    }

    pthread_t tid2[THREAD_COUNT];
    int thread_id[THREAD_COUNT];

    // copy to external fs concurrently
    for (int i = 0; i < THREAD_COUNT; ++i) {
        thread_id[i] = i;
        assert(pthread_create(&tid2[i], NULL, copy_external_thread,
                              (void *)(&thread_id[i])) == 0);
    }

    for (int i = 0; i < THREAD_COUNT; ++i) {
        assert(pthread_join(tid2[i], NULL) == 0);
    }

    for (int i = 0; i < FILE_COUNT; ++i) {
        check_if_file_was_correctly_written(i);
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

void *copy_external_thread(void *thread_i) {
    for (int file_id = 0; file_id < FILE_COUNT; ++file_id) {
        for (int i = 0; i < SAVE_COUNT_PER_FILE; ++i) {
            char external_path[MAX_EXTERNAL_FILE_NAME];
            sprintf(external_path, "./test_out_f%d_t%d_%d.txt", file_id,
                    *((int *)thread_i), i);

            assert(tfs_copy_to_external_fs(tfs_files[file_id], external_path) ==
                   0);
        }
    }

    return NULL;
}

void check_if_file_was_correctly_written(int file_id) {
    FILE *fd = fopen(input_files[file_id], "r");
    assert(fd != NULL);

    char buffer_external[BUFFER_LEN];
    char buffer_copied[BUFFER_LEN];

    for (int thread_i = 0; thread_i < THREAD_COUNT; ++thread_i) {
        for (int i = 0; i < SAVE_COUNT_PER_FILE; ++i) {
            rewind(fd);

            char external_path[MAX_EXTERNAL_FILE_NAME];
            sprintf(external_path, "./test_out_f%d_t%d_%d.txt", file_id,
                    thread_i, i);

            FILE *fd2 = fopen(external_path, "r");
            assert(fd2 != NULL);

            size_t bytes_read_external =
                fread(buffer_external, sizeof(char), BUFFER_LEN, fd);
            size_t bytes_read_copied =
                fread(buffer_copied, sizeof(char), BUFFER_LEN, fd2);
            while (bytes_read_external > 0 && bytes_read_copied > 0) {
                assert(strncmp(buffer_external, buffer_copied, BUFFER_LEN) ==
                       0);
                bytes_read_external =
                    fread(buffer_external, sizeof(char), BUFFER_LEN, fd);
                bytes_read_copied =
                    fread(buffer_copied, sizeof(char), BUFFER_LEN, fd2);
            }

            // check if both files reached the end
            assert(bytes_read_external == 0);
            assert(bytes_read_copied == 0);

            assert(fclose(fd2) == 0);

            assert(unlink(external_path) == 0);
        }
    }

    assert(fclose(fd) == 0);
}
