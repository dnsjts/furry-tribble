#!/usr/bin/env python3
import subprocess
import os
import sys

SHELL = "/bin/bash"


def common_ancestor_to_head(revision):
    merge_base_result = subprocess.run(
        ["git", "merge-base", "HEAD", revision], stdout=subprocess.PIPE, check=True
    )
    return merge_base_result.stdout.strip().decode("utf-8")


def remove_first(common_ancestor):
    my_env = os.environ.copy()
    my_env["SHELL"] = SHELL
    my_env["GIT_SEQUENCE_EDITOR"] = "sed -i '1s/pick/drop/'"

    my_command = [
        "git",
        "rebase",
        "--autostash",
        "--interactive",
        "-X",
        "patience",
        "-X",
        "theirs",
        common_ancestor,
    ]
    subprocess.Popen(my_command, env=my_env).wait()


def make_initial_change(target_revision, change_command="echo"):
    git_log_result = subprocess.run(
        ["git", "log", '--format="%H"', "-n", "1"], stdout=subprocess.PIPE, check=True
    )
    head_commitid = git_log_result.stdout.strip().decode("utf-8")

    my_env = os.environ.copy()
    my_env["SHELL"] = SHELL
    my_env["GIT_SEQUENCE_EDITOR"] = r"sed -i '1i exec {}\n'".format(
        '{} {} {} {} "{}"'.format(
            __file__, target_revision, "initial", head_commitid, change_command
        )
    )

    common_ancestor = common_ancestor_to_head(target_revision)

    my_command = [
        "git",
        "rebase",
        "--autostash",
        "--interactive",
        "-X",
        "theirs",
        "--empty=drop",
        "--exec",
        "git diff --diff-filter=ACMR HEAD^ HEAD --name-only | {change_command}; git commit --all --amend --no-edit --no-gpg-sign --no-verify".format(
            change_command=change_command
        ),
        common_ancestor,
    ]

    subprocess.Popen(my_command, env=my_env).wait()


if __name__ == "__main__":
    if len(sys.argv) > 3:
        print(sys.argv[1])
        if (
            sys.argv[2] == "initial"
            and sys.argv[3] is not None
            and sys.argv[4] is not None
        ):
            commitid = sys.argv[3]
            change_command = sys.argv[4]
            subprocess.run(
                "git diff --diff-filter=ACMR --name-only {before_rebase_commitid} HEAD | {change_command}".format(
                    before_rebase_commitid=commitid, change_command=change_command,
                ),
                shell=True,
                check=True,
            )
            subprocess.run(
                "git commit --all --allow-empty --message 'Initial change' --no-verify --no-gpg-sign",
                shell=True,
                check=True,
            )

    elif len(sys.argv) == 3:
        make_initial_change(sys.argv[1], sys.argv[2])

        common_ancestor = common_ancestor_to_head(sys.argv[1])
        remove_first(common_ancestor)

    else:
        print("Specify the target branch!", file=sys.stderr)
        exit(1)

    exit(0)
