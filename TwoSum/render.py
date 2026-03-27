import subprocess

command = f"manim -p main.py TwoSum -- --sound"
result = subprocess.run(command, shell=True)

print(f"Command finished with return code: {result.returncode}")
