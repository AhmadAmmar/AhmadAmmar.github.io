"""Run the commands the beginner guides teach, in a throwaway folder, and save what they print.

    python make_outputs.py

The guides include these files, so a change in git's behaviour or in a command reaches every guide at the next build.
A local bare repository stands in for GitHub, so the address is replaced by a sample one in the saved text.
"""
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

OUT = Path(__file__).parent / "outputs"
OUT.mkdir(exist_ok=True)
tmp = Path(tempfile.mkdtemp())
ENV = ["-c", "user.name=Your Name", "-c", "user.email=you@example.org", "-c", "init.defaultBranch=main", "-c", "advice.detachedHead=false", "-c", "color.ui=false"]


def clean(text):
    text = text.replace("\r\n", "\n").replace(tmp.as_posix(), "").replace(str(tmp), "")
    text = re.sub(r"(file://)?/?(remote_site|upstream|fork)\.git", lambda m: {"remote_site": "https://github.com/your-name/your-name.github.io.git", "upstream": "https://github.com/their-name/their-project.git", "fork": "https://github.com/your-name/their-project.git"}[m[2]], text)
    text = text.replace("From /upstream", "From https://github.com/their-name/their-project")
    return re.sub(r"\b[0-9a-f]{7}\.\.[0-9a-f]{7}\b", "1a2b3c4..5d6e7f8", text)


def git(cwd, *args):
    r = subprocess.run(["git", *ENV, *args], cwd=cwd, capture_output=True, text=True, encoding="utf8")
    return r.stdout + r.stderr


def record(name, steps, cwd):
    """steps: list of argument lists. Saves each command with its output, as on a screen."""
    lines = []
    for args in steps:
        lines.append("$ git " + " ".join(f'"{a}"' if " " in a else a for a in args))
        lines.append(git(cwd, *args).rstrip())
    (OUT / f"{name}.txt").write_text(clean("\n".join(x for x in lines if x)) + "\n", encoding="utf8", newline="\n")


# A first site, committed and pushed
(tmp / "remote_site.git").mkdir()
git(tmp / "remote_site.git", "init", "--bare", "-q")
git(tmp, "clone", "-q", (tmp / "remote_site.git").as_posix(), "site")
site = tmp / "site"
(site / "index.html").write_text("<h1>Your Name</h1>\n", encoding="utf8")
record("git_status_new", [["status"]], site)
record("git_add_commit", [["add", "index.html"], ["commit", "-m", "Add my first page"]], site)
record("git_push", [["push", "-u", "origin", "main"]], site)
record("git_log", [["log", "--oneline"]], site)
(site / "index.html").write_text("<h1>Your Name</h1>\n<p>I study rivers.</p>\n", encoding="utf8")
record("git_diff", [["diff"]], site)

# A contribution: a project, your copy of it, a branch
(tmp / "upstream.git").mkdir()
git(tmp / "upstream.git", "init", "--bare", "-q")
git(tmp, "clone", "-q", (tmp / "upstream.git").as_posix(), "maker")
maker = tmp / "maker"
(maker / "README.md").write_text("# Their project\n\nThis tool reads a CVS file.\n", encoding="utf8")
(maker / "areas.py").write_text("def circle_area(radius):\n    return 3.14 * radius * radius\n", encoding="utf8")
git(maker, "add", ".")
git(maker, "commit", "-qm", "First version")
git(maker, "push", "-q", "origin", "main")
shutil.copytree(tmp / "upstream.git", tmp / "fork.git")
mine = tmp / "mine"
r = git(tmp, "clone", (tmp / "fork.git").as_posix(), "mine")
(OUT / "oss_clone.txt").write_text(clean("$ git clone https://github.com/your-name/their-project.git\n" + r.replace("'mine'", "'their-project'")), encoding="utf8", newline="\n")
record("oss_remote", [["remote", "add", "upstream", (tmp / "upstream.git").as_posix()], ["remote", "-v"]], mine)
record("oss_branch", [["switch", "-c", "fix-readme-spelling"]], mine)
(mine / "README.md").write_text("# Their project\n\nThis tool reads a CSV file.\n", encoding="utf8")
record("oss_diff", [["diff"]], mine)
record("oss_commit", [["add", "README.md"], ["commit", "-m", "Fix spelling of CSV in the README"]], mine)
record("oss_push", [["push", "-u", "origin", "fix-readme-spelling"]], mine)
git(maker, "pull", "-q")
(maker / "CHANGES.md").write_text("Notes\n", encoding="utf8")
git(maker, "add", ".")
git(maker, "commit", "-qm", "Add notes")
git(maker, "push", "-q", "origin", "main")
record("oss_sync", [["switch", "main"], ["fetch", "upstream"], ["merge", "upstream/main"], ["push", "origin", "main"]], mine)

# A code change with a test, run for real
(tmp / "code").mkdir()
print("wrote", len(list(OUT.glob("*.txt"))), "files")
shutil.rmtree(tmp, ignore_errors=True)
