#!/bin/bash

# Strips all binaries in provided dir
for i in $(find $1* -executable);
    do strip $i
done
