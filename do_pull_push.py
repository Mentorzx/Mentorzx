import subprocess
with open('git_pull.txt', 'w') as f:
    subprocess.run(['git', 'add', '-A'])
    subprocess.run(['git', 'commit', '-m', "Update SVGs locally"])
    res = subprocess.run(['git', 'pull', '--rebase'], capture_output=True, text=True)
    f.write("PULL RESULT:\n" + res.stdout + '\n' + res.stderr)
    res_push = subprocess.run(['git', 'push'], capture_output=True, text=True)
    f.write("\nPUSH RESULT:\n" + res_push.stdout + '\n' + res_push.stderr)
