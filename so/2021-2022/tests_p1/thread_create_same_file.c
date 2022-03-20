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

#define TFS_FILE "/f1"
#define THREAD_COUNT 20

void *create_file(void *arg);
void assert_file_has_correct_content();

/* This test creates as many files as possible concurrently with the same name
 * in order to test if it does not create the same file twice. Each thread adds
 * a character to the file to be able to check if it's the same file or not. */
int main() {
    pthread_t tid[THREAD_COUNT];
    int *fd[THREAD_COUNT];
    assert(tfs_init() != -1);

    for (int i = 0; i < THREAD_COUNT; ++i) {
        if (pthread_create(&tid[i], NULL, create_file, NULL) != 0) {
            exit(EXIT_FAILURE);
        }
    }

    for (int i = 0; i < THREAD_COUNT; ++i) {
        pthread_join(tid[i], (void **)&fd[i]);
    }

    char dummy_buffer[THREAD_COUNT + 1];
    char content = 'A';
    for (int i = 0; i < THREAD_COUNT; ++i) {
        // read until reaching the end of the file, then write to it
        assert(tfs_read(*fd[i], &dummy_buffer, THREAD_COUNT + 1) != -1);
        assert(tfs_write(*fd[i], &content, 1) == 1);

        assert(tfs_close(*fd[i]) != -1);
        free(fd[i]);
    }

    assert_file_has_correct_content();

    tfs_destroy();
    printf("Successful test.\n");

    return 0;
}

void *create_file(void *arg) {
    (void)arg;

    int *f = malloc(sizeof(int));
    assert(f != NULL);
    *f = tfs_open(TFS_FILE, TFS_O_CREAT);
    assert(*f != -1);

    return f;
}

void assert_file_has_correct_content() {
    int f = tfs_open(TFS_FILE, 0);
    assert(f != -1);

    char buffer[THREAD_COUNT + 1];

    // if it reads less than what we asked, means we reached the end of the file
    assert(tfs_read(f, buffer, THREAD_COUNT + 1) == THREAD_COUNT);

    assert(tfs_close(f) != -1);
}
