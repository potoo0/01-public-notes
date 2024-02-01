# doc: https://man7.org/linux/man-pages/man1/bash.1.html
# 1. Compound Commands
# a. `()` execute in subshell
(cd /tmp && ls) # not affect current shell's environment

if (cd "$BASE" && git rev-parse --is-inside-work-tree); then
    echo "$BASE inside git work tree."
    exit 0
fi
