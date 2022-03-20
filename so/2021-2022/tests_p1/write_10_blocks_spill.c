#include "../fs/operations.h"
#include <assert.h>
#include <string.h>

#define COUNT 40
#define SIZE 250

/**
   This test fills in a new file up to 10 blocks via multiple writes,
   where some calls to tfs_write may imply filling in 2 consecutive blocks,
   then checks if the file contents are as expected
 */

int main() {

    char *path = "/f1";

    /* Writing this buffer multiple times to a file stored on 1KB blocks will
       sometimes target 2 consecutive blocks (since 1KB is *not* a multiple of
       SIZE=250)
    */
    char input[SIZE];
    memset(input, 'A', SIZE);

    char output[SIZE];

    assert(tfs_init() != -1);

    /* Write input COUNT times into a new file */
    int fd = tfs_open(path, TFS_O_CREAT);
    assert(fd != -1);
    for (int i = 0; i < COUNT; i++) {
        assert(tfs_write(fd, input, SIZE) == SIZE);
    }
    assert(tfs_close(fd) != -1);

    /* Open again to check if contents are as expected */
    fd = tfs_open(path, 0);
    assert(fd != -1);

    for (int i = 0; i < COUNT; i++) {
        assert(tfs_read(fd, output, SIZE) == SIZE);
        assert(memcmp(input, output, SIZE) == 0);
    }

    assert(tfs_close(fd) != -1);

    printf("Successful test.\n");

    return 0;
}