import subprocess

# audio = "TwoSum.mp3"
# command = f"start {audio} && manim -p main.py TwoSum"

command = f"manim -p main.py TwoSum"
result = subprocess.run(command, shell=True)

print(f"Command finished with return code: {result.returncode}")
