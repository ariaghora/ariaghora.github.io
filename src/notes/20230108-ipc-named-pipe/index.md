# Communication between programs (in any languages) with named pipes

Imagine you are building a system to monitor the temperature in a warehouse.
You have multiple sensors scattered throughout the warehouse that are constantly measuring the temperature, and you want to display the temperature data on a dashboard.
One way you could do this is by using the publish-subscribe pattern: each sensor would publish its temperature data to a *message broker*, which would then forward the data to the dashboard program.
The dashboard program would be subscribed to the message broker and would receive the temperature data when it is forwarded.

<pre class="mermaid">
    graph LR 
        A[Publisher] --> B[Message broker]
        B --> C[Subscriber] 
</pre>

This allows the sensor programs and the dashboard program to operate independently and asynchronously, making the system more efficient and scalable.
This pattern is common in distributed systems, where the publisher and subscriber may be running on different machines.

> Now, what if you want to implement this pattern in a local system, where the publisher and subscriber are running on the same machine?

## Local communication with named pipes

It is not counterintuitive to use a message broker in this case.
In fact, it is pretty common to use a message broker in a local system.
Especially when the publisher and subscriber are written in different languages, it is easier to use a message broker to communicate between them.
In this case, the message broker can be implemented using a *named pipe*.

Named pipe can be created using the `mkfifo` command:

```bash
$ mkfifo /tmp/mypipe
```

The `/tmp/mypipe` pipe will be created.
Note that it looks like a file, but it is **actually** not a file: it is a *pseudo-file*.
We can find pseudo-files in unix systems like `/dev/null`, `/proc`, or `/sys` ([more example](https://en.wikipedia.org/wiki/Synthetic_file_system#Examples)).

Consider following example, where left pane is the publisher and right pane is the subscriber. 
The publisher writes to the named pipe (using `echo`) and the subscriber reads from the named pipe (using `cat`).


<div id="player1"></div>

Named pipe is a standard, and most of programming languages support it, so we can use it programmaticaly.

Next, we will look at how to implement a publisher and subscriber using Go and Python.
Named pipe will serve as the message broker in this case.

> **Objective:** implement the publisher in Go and the subscriber in Python. The publisher can accept user input and write it to the named pipe. The subscriber can read from the named pipe and print the message to the console. When the user enters the word "exit", the subscriber should end its process.

## Go program as the publisher

We will use Go as the publisher.
A publisher writes messages to a named pipe and a subscriber that reads messages from the same named pipe.
To begin, let's take a look at the Go program that acts as the publisher.
This program prompts the user for a message and then writes the message to a named pipe:

```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"syscall"
)

const pipeName = "/tmp/mypipe"

func WriteMessage(message, pipeName string) error {
	// check if the named pipe exists. If not, create it. Otherwise, assume
	// it's already created beforehand.
	_, err := os.Stat(pipeName)
	if err != nil {
		if os.IsNotExist(err) {
			err = syscall.Mkfifo(pipeName, 0666)
			if err != nil {
				return err
			}
		} else {
			return err
		}
	}

	// open the named pipe for writing
	pipe, err := os.OpenFile(pipeName, os.O_WRONLY, 0666)
	if err != nil {
		panic(err)
	}
	defer pipe.Close()

	// write the message to the named pipe
	_, err = pipe.WriteString(message)

	return err
}

func main() {
	for {
		// Get user input
		fmt.Print("Enter message to send: ")
		reader := bufio.NewReader(os.Stdin)
		message, _ := reader.ReadString('\n')
		message = message[:len(message)-1] // trim trailing newline

		// send the message to the named pipe
		if err := WriteMessage(message, pipeName); err != nil {
			panic(err)
		}
	}
}
```

The `WriteMessage` function is responsible for writing the message to the named pipe.
It first checks if the named pipe exists and creates it if it does not. It then opens the named pipe for writing and writes the message to it using the `WriteString` method.

In the main function, the program enters an infinite loop that prompts the user for a message and then writes the message to the named pipe using the WriteMessage function.
The program will continue to run until it is interrupted or terminated.


## Python program as the subscriber

Now, let's take a look at the Python program that acts as the subscriber. This program reads messages from the named pipe and processes them:

```python
PIPE_NAME = "/tmp/mypipe"

def handle_message(message: str) -> None:
    if message == "exit":
        print("Exiting...")
        exit(0)
    print(f"Received: {data}")

if __name__ == "__main__":
    while True:
        with open(PIPE_NAME, "r") as pipe:
            # Read data from the pipe
            data = pipe.read().strip()

            # Print the data from the pipe
            if data:
                handle_message(data)
```

This is the result:

<div id="player2"></div>

### Named pipes vs regular files

-  Like regular files, named pipes have a name and are stored on the file system. However, they have some differences from regular files. One key difference is that named pipes have a "buffer" that stores the data being exchanged between processes. When a process writes data to a named pipe, the data is stored in the buffer until another process reads it.
-  Another difference between named pipes and regular files is that named pipes can only be opened for reading or writing, not both. This means that a process that opens a named pipe for writing can only write to the pipe, and a process that opens the pipe for reading can only read from it.

> You might ask, "why should I use named pipes instead of regular files?"

Regular files are slower than named pipes for interprocess communication because they are not optimized for messaging purpose.
When data is written to a regular file, it is stored on the file system and the file system must update its metadata to reflect the new data.
This can be slower than using a named pipe's buffer, especially if the data is being written to the file system frequently.

In addition, regular files have a more complex API than named pipes, as they can be opened for reading, writing, or both.
This can make them slower to use in certain situations, as more code may be required to perform file operations.

<script>
AsciinemaPlayer.create(
	'/casts/named-pipe-example.cast',
	document.getElementById('player1'),
	{ cols: 110, rows: 30, theme: 'monokai' }
);

AsciinemaPlayer.create(
	'/casts/named-pipe-result.cast',
	document.getElementById('player2'),
	{ cols: 110, rows: 20, theme: 'monokai' }
);
</script>
