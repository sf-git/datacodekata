#!/bin/bash
MSYS2_ARG_CONV_EXCL="*" docker run -ti --rm -v "$(pwd)":/work  --entrypoint fwf_cli dck_problem1:0.0.1 --spec_file spec.json --fwf_file o.txt -n 15