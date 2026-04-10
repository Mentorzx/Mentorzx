import subprocess
with open('git_pull.txt', 'w') as f:
    res = subprocess.run(['git', 'pull', '--rebase'], capture_output=True, text=True)
    f.write(res.stdout + '\n' + res.stderr)
