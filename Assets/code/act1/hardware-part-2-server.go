package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
)

func handleText(w http.ResponseWriter, r *http.Request) {
	var text string

	switch r.Method {
	case http.MethodGet:
		// Get text from URL parameter
		text = r.URL.Query().Get("text")
		if text == "" {
			http.Error(w, "Please provide a 'text' parameter", http.StatusBadRequest)
			return
		}

	case http.MethodPost:

		// Read text from request body
		body, err := io.ReadAll(r.Body)
		if err != nil {
			http.Error(w, "Error reading request body", http.StatusInternalServerError)
			return
		}
		defer r.Body.Close()

		text = string(body)
		if text == "" {
			http.Error(w, "Request body cannot be empty", http.StatusBadRequest)
			return
		}

	default:
		http.Error(w, "Only GET and POST methods are supported", http.StatusMethodNotAllowed)
		return
	}

	// Print the text to server console
	fmt.Printf("Received text: %s\n", text)

	// Send response back to client
	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, "Successfully processed text: %s", text)
}

func main() {
	http.HandleFunc("/text", handleText)

	fmt.Println("Server starting on :52522...")
	if err := http.ListenAndServe(":52522", nil); err != nil {
		log.Fatal(err)
	}
}
