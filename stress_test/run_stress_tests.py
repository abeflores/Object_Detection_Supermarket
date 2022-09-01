from itertools import product
import subprocess as sp

# Config parameters

num_models_list = [1]
num_users_list = [100]
spawn_rate_list = [3]
run_time = "7m"
host = "http://localhost/"

# --------------------


def run_tests():
    """Run the tests with different combinations of config parameters, and save
    a html report for each one.
    """

    for num_models in num_models_list:

        for num_users, spawn_rate in product(num_users_list, spawn_rate_list):

            # Start containers

            args = [
                "docker",
                "compose",
                "up",
                "-d",
                "--build",
                "--scale",
                f"model={num_models}",
            ]

            sp.call(args)

            # Start locust test

            html_file = f"reports/report_{num_models}_{num_users}_{spawn_rate}.html"
            print("Started test with params: ")
            print(f"Number of model containers: {num_models}")
            print(f"Number of users: {num_users}")
            print(f"Spawn rate: {spawn_rate}")

            args = [
                "locust",
                "--headless",
                "-H",
                host,
                "-L",
                "ERROR",
                "-u",
                str(num_users),
                "-r",
                str(spawn_rate),
                "-t",
                run_time,
                "--html",
                html_file,
            ]

            sp.call(args)

            # Stop containers

            args = ["docker", "compose", "down"]

            sp.call(args)


if __name__ == "__main__":
    run_tests()
