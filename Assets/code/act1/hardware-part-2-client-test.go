package main

import (
	"fmt"
	"io"
	"net/http"
	"strings"
)

func main() {
	// Server URL
	serverURL := "http://70.106.246.123:52522/text"

	// Try both GET and POST requests

	// GET request
	resp, err := http.Get(serverURL + "?text=test")
	if err != nil {
		fmt.Printf("Error making GET request: %v\n", err)
	} else {
		defer resp.Body.Close()
		body, _ := io.ReadAll(resp.Body)
		fmt.Printf("GET Response: %s\n", string(body))
	}

	// POST request
	resp, err = http.Post(serverURL,
		"text/plain",
		strings.NewReader("test"))
	if err != nil {
		fmt.Printf("Error making POST request: %v\n", err)
	} else {
		defer resp.Body.Close()
		body, _ := io.ReadAll(resp.Body)
		fmt.Printf("POST Response: %s\n", string(body))
	}
}
