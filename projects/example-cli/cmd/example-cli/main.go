package main

import (
	"fmt"
	"os"
)

// main is the entry point for the example-cli application.
// It demonstrates a simple CLI structure that the AI dev team can extend.
func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: example-cli <command>")
		fmt.Println("Commands:")
		fmt.Println("  hello    - Print a greeting")
		fmt.Println("  version  - Show version information")
		os.Exit(1)
	}

	command := os.Args[1]
	switch command {
	case "hello":
		fmt.Println("Hello, World! This is an example CLI built by the AI development team.")
	case "version":
		fmt.Println("example-cli version 1.0.0")
	default:
		fmt.Printf("Unknown command: %s\n", command)
		os.Exit(1)
	}
}