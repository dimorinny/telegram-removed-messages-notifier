#!/usr/bin/env bash

set -eux

telegram_removed_messages_notifier \
    --api-id ${API_ID} \
    --api-hash ${API_HASH} \
    --phone-number ${PHONE_NUMBER} \
    --messages-buffer-size ${MESSAGES_BUFFER_SIZE} \
    start ${SESSION_NAME}