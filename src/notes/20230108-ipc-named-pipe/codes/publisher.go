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
