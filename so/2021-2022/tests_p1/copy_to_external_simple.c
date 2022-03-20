#include "fs/operations.h"
#include <assert.h>
#include <string.h>
#include <unistd.h>

int main() {

    char *str = "AAA! AAA! AAA! ";
    char *path = "/f1";
    char *path2 = "external_file.txt";
    char to_read[40];

    assert(tfs_init() != -1);

    int file = tfs_open(path, TFS_O_CREAT);
    assert(file != -1);

    assert(tfs_write(file, str, strlen(str)) != -1);

    assert(tfs_close(file) != -1);

    assert(tfs_copy_to_external_fs(path, path2) != -1);

    FILE *fp = fopen(path2, "r");

    assert(fp != NULL);

    assert(fread(to_read, sizeof(char), strlen(str), fp) == strlen(str));

    assert(strncmp(str, to_read, strlen(str)) == 0);

    assert(fclose(fp) != -1);

    unlink(path2);

    printf("Successful test.\n");

    return 0;
}
