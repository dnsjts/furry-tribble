# furry-tribble

This tool is made for formatting the code of an open pull request, and nothing else.

Generally, this is a script, which allows the user to run something on the original code, run something (else) on a bunch of commits, and revert the first command. On the other hand, this is just a ~~not so~~ shiny script, which runs two `git rebase`s with a twist.

## Typical use-case

"Oh shit, I've called this variable "X" for the last N commits, but I want to rename it to "Y" and pretend I've called it "Y" since the beginning of time. I wish there was a tool for this."

## The advantages of this approach:
* Applying a formatter to the whole codebase would be difficult to review. The review is necessary, because no one should trust blindly in a binary.

## TODO:
* Make it possible to override the formatter tool.
* Reduce the number of the irrelevant changes.
* Give a better name for this tool.

## Alternatives:
* [clang-format-diff.py](https://llvm.org/svn/llvm-project/cfe/trunk/tools/clang-format/clang-format-diff.py)
