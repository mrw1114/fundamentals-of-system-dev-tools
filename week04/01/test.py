import subprocess
a = subprocess.Popen
b = True
a('echo test', shell=b)
