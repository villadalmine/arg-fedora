#!/bin/bash

__create_user() {
# Create a user to SSH into as.
useradd juan
SSH_USERPASS=juan1234
echo -e "$SSH_USERPASS\n$SSH_USERPASS" | (passwd --stdin juan)
echo ssh juan password: $SSH_USERPASS
}

# Call all functions
__create_user
