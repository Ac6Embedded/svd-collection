#!/usr/bin/env python3
"""Bump every submodule gitlink to the latest upstream commit.

Does not clone or checkout any submodule. For each entry in .gitmodules the
remote head of its recorded branch (or the default branch as fallback) is
compared to the committed gitlink, and the index is updated when it moved.
Private submodules are checked with the token in GH_PAT if set, skipped
otherwise. Run from the repo root; changes are left staged for commit.
"""

import os
import subprocess
import sys


def run(*args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{' '.join(args)}: {r.stderr.strip()}")
    return r.stdout.strip()


def ls_remote(url, ref):
    r = subprocess.run(["git", "ls-remote", url, ref],
                       capture_output=True, text=True)
    out = r.stdout.strip()
    if r.returncode != 0 or not out:
        return None
    return out.split()[0]


def main():
    cfg = run("git", "config", "-f", ".gitmodules",
              "--get-regexp", r"^submodule\.")
    subs = {}
    for line in cfg.splitlines():
        key, _, val = line.partition(" ")
        _, name, prop = key.split(".", 2)
        subs.setdefault(name, {})[prop] = val

    token = os.environ.get("GH_PAT", "")
    changed = 0
    for name, s in sorted(subs.items()):
        if "path" not in s or "url" not in s:
            print(f"skip {name}: incomplete .gitmodules entry")
            continue
        path, url, branch = s["path"], s["url"], s.get("branch", "")
        auth_url = url
        if token and url.startswith("https://github.com/"):
            auth_url = url.replace("https://",
                                   f"https://x-access-token:{token}@")
        sha = None
        if branch:
            sha = ls_remote(auth_url, f"refs/heads/{branch}")
        if sha is None:
            # branch may have been renamed (nxp uses release/* branches),
            # fall back to whatever the remote default branch points at
            sha = ls_remote(auth_url, "HEAD")
        if sha is None:
            print(f"skip {path}: unreachable "
                  "(private without GH_PAT, or upstream gone)")
            continue
        parts = run("git", "ls-tree", "HEAD", path).split()
        cur = parts[2] if len(parts) >= 3 else ""
        if sha != cur:
            run("git", "update-index", "--add",
                "--cacheinfo", f"160000,{sha},{path}")
            print(f"bump {path}: {cur[:9] or 'none'} -> {sha[:9]}")
            changed += 1
        else:
            print(f"ok   {path}: {sha[:9]}")
    print(f"{changed} submodule(s) bumped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
