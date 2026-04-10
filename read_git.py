import subprocess

with open("git_log.txt", "w") as f:
    res = subprocess.run(["git", "status"], capture_output=True, text=True)
    f.write(res.stdout + "\n" + res.stderr)
