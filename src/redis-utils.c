#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <hiredis.h>


size_t getFileSize(FILE *file) ;

int main(int argc, char **argv) {
    unsigned int j;
    redisContext *c;
    redisReply *reply;
    const char *hostname = (argc > 2) ? argv[2] : "127.0.0.1"; // defaulted to home
    int port = (argc > 3) ? atoi(argv[3]) : 6379;
    char *content_name = argv[1];

    struct timeval timeout = { 1, 500000 }; // 1.5 seconds
    c = redisConnectWithTimeout(hostname, port, timeout);
    if (c == NULL || c->err) {
        if (c) {
            printf("Connection error: %s\n", c->errstr);
            redisFree(c);
        } else {
            printf("Connection error: can't allocate redis context\n");
        }
        exit(1);
    }

    /* PING server */
    reply = redisCommand(c,"PING");
    printf("PING: %s\n", reply->str);
    freeReplyObject(reply);

    FILE *file = fopen(content_name, "rb");
    if (file == NULL) {
        fprintf(stderr, "Error opening file %s\n", content_name);
        exit(1);
    }

    size_t size = getFileSize(file);
    char *buff = malloc(size);

    int len = fread(buff, 1, size, file);

    if (len != size) {
        printf("%d %d\n", (int)len, (int)size);
        fprintf(stderr, "Read failed");
        exit(1);
    }



    /* Set a key using binary safe API */
    reply = redisCommand(c,"SET %b %b", content_name, strlen(content_name), buff, size);
    printf("SET (binary API): %s\n", reply->str);
    freeReplyObject(reply);

    /* Disconnects and frees the context */
    redisFree(c);

    return 0;
}

size_t getFileSize(FILE *file) 
{
    size_t size;
    fseek(file, 0L, SEEK_END);
    size =  ftell(file);
    fseek(file, 0L, SEEK_SET);

    return size;
}