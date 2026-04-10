import os, subprocess
with open('git_log_history.txt', 'w') as f:
    res = subprocess.run(['git', 'log', '-n', '5', '--oneline'], capture_output=True, text=True)
    f.write(res.stdout + '\n')
    res2 = subprocess.run(['git', 'log', 'origin/main', '-n', '5', '--oneline'], capture_output=True, text=True)
    f.write(res2.stdout + '\n')
