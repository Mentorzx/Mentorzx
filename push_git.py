import subprocess

with open("git_push_log.txt", "w") as f:
    res = subprocess.run(["git", "push"], capture_output=True, text=True)
    f.write(res.stdout + "\n" + res.stderr)
