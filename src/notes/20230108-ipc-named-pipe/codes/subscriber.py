PIPE_NAME = "/tmp/mypipe"


def handle_message(message: str) -> None:
    if message == "exit":
        print("Exiting...")
        exit(0)
    print(f"Received: {data}")


if __name__ == "__main__":
    with open(PIPE_NAME, "r") as pipe:
        while True:
            # Read data from the pipe
            data = pipe.read().strip()

            # Print the data from the pipe
            if data:
                handle_message(data)
