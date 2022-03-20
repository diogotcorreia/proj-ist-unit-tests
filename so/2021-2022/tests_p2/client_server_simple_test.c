#include "client/tecnicofs_client_api.h"
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

/*  This test is similar to test1.c from the 1st exercise.
    The main difference is that this one explores the
    client-server architecture of the 2nd exercise. */

#define CLIENT_COUNT 20
#define CLIENT_PIPE_NAME_LEN 40
#define CLIENT_PIPE_NAME_FORMAT "/tmp/tfs_c%d"

void run_test(char *server_pipe, int client_id);

int main(int argc, char **argv) {
    if (argc < 2) {
        printf(
            "You must provide the following arguments: 'server_pipe_path'\n");
        return 1;
    }

    int child_pids[CLIENT_COUNT];

    for (int i = 0; i < CLIENT_COUNT; ++i) {
        int pid = fork();
        assert(pid >= 0);
        if (pid == 0) {
            /* run test on child */
            run_test(argv[1], i);
            exit(0);
        } else {
            child_pids[i] = pid;
        }
    }

    for (int i = 0; i < CLIENT_COUNT; ++i) {
        int result;
        waitpid(child_pids[i], &result, 0);
        assert(WIFEXITED(result));
        // printf("Client %d exited successfully.\n", i);
    }

    printf("Successful test.\n");

    return 0;
}

void run_test(char *server_pipe, int client_id) {
    char *str = "AAA!";
    char *path = "/f1";
    char buffer[40];

    int f;
    ssize_t r;

    char client_pipe[40];
    sprintf(client_pipe, CLIENT_PIPE_NAME_FORMAT, client_id);
    assert(tfs_mount(client_pipe, server_pipe) == 0);

    f = tfs_open(path, TFS_O_CREAT);
    assert(f != -1);

    r = tfs_write(f, str, strlen(str));
    assert(r == strlen(str));

    assert(tfs_close(f) != -1);

    f = tfs_open(path, 0);
    assert(f != -1);

    r = tfs_read(f, buffer, sizeof(buffer) - 1);
    assert(r == strlen(str));

    buffer[r] = '\0';

    assert(strcmp(buffer, str) == 0);

    assert(tfs_close(f) != -1);

    assert(tfs_unmount() == 0);
}
