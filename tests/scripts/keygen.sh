#!/bin/bash

# Key Size
SIZE=64

# Generate Key
if [ "$1" != "" ]; then
    python -c "import secrets; print(secrets.token_urlsafe($1))"
else
    python -c "import secrets; print(secrets.token_urlsafe($SIZE))"
fi
