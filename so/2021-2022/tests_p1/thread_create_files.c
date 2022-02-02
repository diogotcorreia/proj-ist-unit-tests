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

#define FILE_NAME_MAX_LEN 10
#define THREAD_COUNT 2
#define FILES_TO_CREATE_PER_THREAD 10

void *create_file(void *arg);

/* This test creates as many files as possible concurrently in order to test if
 * inumbers are assigned correctly. */
int main() {
    pthread_t tid[THREAD_COUNT];
    assert(tfs_init() != -1);
    int table[THREAD_COUNT];

    for (int i = 0; i < THREAD_COUNT; ++i) {
        table[i] = i * FILES_TO_CREATE_PER_THREAD + 1;
    }

    for (int i = 0; i < THREAD_COUNT; ++i) {
        if (pthread_create(&tid[i], NULL, create_file, &table[i]) != 0) {
            exit(EXIT_FAILURE);
        }
    }

    for (int i = 0; i < THREAD_COUNT; ++i) {
        pthread_join(tid[i], NULL);
    }

    // Check if files have the correct content
    for (int i = 0; i < THREAD_COUNT * FILES_TO_CREATE_PER_THREAD; ++i) {
        char path[FILE_NAME_MAX_LEN] = {'/'};
        sprintf(path + 1, "%d", i + 1);

        int f = tfs_open(path, 0);
        assert(f != -1);

        char buffer[FILE_NAME_MAX_LEN];
        assert(tfs_read(f, buffer, FILE_NAME_MAX_LEN) != -1);

        assert(strcmp(path, buffer) == 0);

        assert(tfs_close(f) != -1);
    }

    tfs_destroy();
    printf("Successful test.\n");

    return 0;
}

void *create_file(void *arg) {
    int file_i = *((int *)arg);

    for (int i = 0; i < FILES_TO_CREATE_PER_THREAD; i++) {
        char path[FILE_NAME_MAX_LEN] = {'/'};
        sprintf(path + 1, "%d", file_i + i);

        int f = tfs_open(path, TFS_O_CREAT);
        assert(f != -1);

        // write the file name to the file, so we can test if two files got the
        // same inode
        assert(tfs_write(f, path, strlen(path) + 1) == strlen(path) + 1);

        assert(tfs_close(f) != -1);
    }
    return NULL;
}
