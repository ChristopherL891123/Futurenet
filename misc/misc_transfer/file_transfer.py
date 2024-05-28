import subprocess
import sys

"""
Arguments:

        1. Who is recieving (username)
        2. File to scp 

"""

reciever = sys.argv[1]
filesToScp = sys.argv[2]
print("in file")
subprocess.run(["scp", filesToScp, f"picocluster@{reciever}:~/Desktop/Capstone/update"], check=True)
print("finished file")

