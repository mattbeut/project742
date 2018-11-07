#!/bin/bash

for i in $(find $1* -executable);
    do strip $i
done
