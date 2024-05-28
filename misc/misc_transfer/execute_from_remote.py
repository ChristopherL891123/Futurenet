import subprocess
cdCapstone = "~/Desktop/Capstone/update"

subprocess.run(f"ssh pc0 'python3 ~/Desktop/Capstone/update/file_transfer.py pc1 ~/Desktop/Capstone/update/test.txt'",shell=True)



