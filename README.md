```bash
docker run \
    -d \
    --workdir='<in-container-folder-with-session-database-file>' \
    -e API_ID='<api-id>' \
    -e API_HASH='<api-hash>' \
    -e PHONE_NUMBER='<phone-number>' \
    -e MESSAGES_BUFFER_SIZE='<messages-buffer-size>' \
    -e SESSION_NAME='<session-name>' \
    -v <local-folder-with-session-database-file>:<in-container-folder-with-session-database-file> \
    dimorinny/removed-messages-notifier
```