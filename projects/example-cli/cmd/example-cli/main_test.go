package main

import (
	"os"
	"strings"
	"testing"
)

// TestMain_HelloCommand tests that the hello command produces expected output
func TestMain_HelloCommand(t *testing.T) {
	// Save original args
	originalArgs := os.Args
	defer func() { os.Args = originalArgs }()

	// Set test args
	os.Args = []string{"example-cli", "hello"}

	// Capture stdout
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	// Run main function
	main()

	// Clean up
	w.Close()
	os.Stdout = oldStdout

	// Read output
	buf := make([]byte, 1024)
	n, _ := r.Read(buf)
	output := strings.TrimSpace(string(buf[:n]))

	// Check output
	expected := "Hello, World! This is an example CLI built by the AI development team."
	if output != expected {
		t.Errorf("Expected '%s', got '%s'", expected, output)
	}
}

// TestMain_VersionCommand tests that the version command produces expected output
func TestMain_VersionCommand(t *testing.T) {
	// Save original args
	originalArgs := os.Args
	defer func() { os.Args = originalArgs }()

	// Set test args
	os.Args = []string{"example-cli", "version"}

	// Capture stdout
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	// Run main function
	main()

	// Clean up
	w.Close()
	os.Stdout = oldStdout

	// Read output
	buf := make([]byte, 1024)
	n, _ := r.Read(buf)
	output := strings.TrimSpace(string(buf[:n]))

	// Check output
	expected := "example-cli version 1.0.0"
	if output != expected {
		t.Errorf("Expected '%s', got '%s'", expected, output)
	}
}

// TestMain_InvalidCommand tests that invalid commands produce error exit
func TestMain_InvalidCommand(t *testing.T) {
	// Save original args
	originalArgs := os.Args
	defer func() { os.Args = originalArgs }()

	// Set test args
	os.Args = []string{"example-cli", "invalid"}

	// Capture stderr to prevent output during test
	oldStderr := os.Stderr
	r, w, _ := os.Pipe()
	os.Stderr = w

	// Run main function (should call os.Exit(1))
	defer func() {
		// Recover from panic caused by os.Exit
		if r := recover(); r != nil {
			// os.Exit causes panic with exit code
			if exitCode, ok := r.(int); ok && exitCode == 1 {
				return // Expected exit
			}
			panic(r) // Re-panic if it wasn't the expected exit
		}
		t.Error("Expected program to exit with code 1")
	}()

	main()

	// Clean up
	w.Close()
	os.Stderr = oldStderr
}