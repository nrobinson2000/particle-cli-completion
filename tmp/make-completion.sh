#!/bin/bash

particle 2>&1 | tail +9 | head -34 | awk '{print }' > level0

for command in $(cat level0); do particle help $command; done
