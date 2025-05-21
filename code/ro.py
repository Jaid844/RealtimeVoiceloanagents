import subprocess


def find_envs_with_package(pkg, version):
    envs = subprocess.check_output(["conda", "env", "list"]).decode()
    env_names = [line.split()[0] for line in envs.splitlines() if line and not line.startswith("#")]

    for env in env_names:
        try:
            output = subprocess.check_output(["conda", "list", "-n", env]).decode()
            if f"{pkg}" in output and f"{version}" in output:
                print(f"Found {pkg}=={version} in: {env}")
        except subprocess.CalledProcessError:
            continue


find_envs_with_package("langgraph", "0.3")
