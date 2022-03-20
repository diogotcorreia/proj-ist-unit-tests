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

#define BUFFER_LEN 120
#define THREAD_COUNT 8
#define REPEAT_COUNT 100
#define FILL_COUNT (BUFFER_LEN * REPEAT_COUNT)

#define TFS_FILE "/dQw4w9WgXcQ"

typedef struct {
    int file_id;
    int thread_id;
} append_data_t;

void *append(void *input);
void *count_letters(void *input);

/* Test writing and reading to/from the same file descriptor on multiple threads
 * concurrently. */
int main() {
    assert(tfs_init() != -1);

    int file_id = tfs_open(TFS_FILE, TFS_O_CREAT);
    assert(file_id != -1);

    pthread_t tid[THREAD_COUNT];
    append_data_t append_data[THREAD_COUNT];

    for (int i = 0; i < THREAD_COUNT; ++i) {
        append_data[i].file_id = file_id;
        append_data[i].thread_id = i;
        assert(pthread_create(&tid[i], NULL, append, &append_data[i]) == 0);
    }

    for (int i = 0; i < THREAD_COUNT; ++i) {
        assert(pthread_join(tid[i], NULL) == 0);
    }

    assert(tfs_close(file_id) == 0);
    file_id = tfs_open(TFS_FILE, 0);
    assert(file_id != -1);

    int global_count[THREAD_COUNT] = {0};
    void *count_result;

    for (int i = 0; i < THREAD_COUNT; ++i) {
        assert(pthread_create(&tid[i], NULL, count_letters, &file_id) == 0);
    }

    for (int i = 0; i < THREAD_COUNT; ++i) {
        assert(pthread_join(tid[i], &count_result) == 0);
        for (int j = 0; j < THREAD_COUNT; ++j) {
            global_count[j] += ((int *)count_result)[j];
        }
        free(count_result);
    }

    for (int i = 0; i < THREAD_COUNT; ++i) {
        assert(global_count[i] == FILL_COUNT);
    }

    assert(tfs_close(file_id) == 0);

    printf("Successful test.\n");
    assert(tfs_destroy() == 0);
    return 0;
}

void *append(void *input) {
    append_data_t *append_data = (append_data_t *)input;

    char buffer[BUFFER_LEN];

    memset(buffer, append_data->thread_id, BUFFER_LEN);
    ssize_t r;
    for (int i = 0; i < REPEAT_COUNT; i++) {
        /* write the contents of the file */
        r = tfs_write(append_data->file_id, buffer, BUFFER_LEN);
        assert(r == BUFFER_LEN);
    }

    return NULL;
}

void *count_letters(void *input) {
    int file_id = *((int *)input);

    int *counts = calloc(THREAD_COUNT, sizeof(int));
    assert(counts != NULL);
    char buffer[BUFFER_LEN];

    ssize_t bytes_read = tfs_read(file_id, buffer, BUFFER_LEN);

    while (bytes_read > 0) {
        /* write the contents of the file */
        for (ssize_t i = 0; i < bytes_read; ++i) {
            int thread_id = buffer[i];
            assert(thread_id >= 0 && thread_id < THREAD_COUNT);
            ++counts[thread_id];
        }
        bytes_read = tfs_read(file_id, buffer, BUFFER_LEN);
    }

    return counts;
}
