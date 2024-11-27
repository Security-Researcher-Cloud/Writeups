package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"time"
)

// Payload represents the JSON structure to send to the API
type Payload struct {
	RequestID string    `json:"requestID"`
	Serial    []int     `json:"serial"`
	Voltage   int       `json:"voltage"`
}

// ValueMaps stores the mapping arrays for different parameters
type ValueMaps struct {
	BaudMap   []int
	ParityMap []string
	DataMap   []int
	StopMap   []int
	FlowMap   []string
	PortMap   []string
}

func main() {
	fmt.Println("UART Parameter Bruteforce Script")
	fmt.Println("-------------------------------")
	
	if combo := tryUARTCombinations(); combo != nil {
		fmt.Println("\nSuccessful combination found!")
		jsonData, _ := json.MarshalIndent(combo, "", "  ")
		fmt.Println(string(jsonData))
	} else {
		fmt.Println("\nNo working combination found")
	}
}

func tryUARTCombinations() *Payload {
	// API endpoint
	url := "https://hhc24-hardwarehacking.holidayhackchallenge.com/api/v1/complete"

	// Define value mappings
	maps := ValueMaps{
		BaudMap:   []int{115200},
		ParityMap: []string{"even"},
		DataMap:   []int{7},
		StopMap:   []int{1},
		FlowMap:   []string{"RTS"},
		PortMap:   []string{"USB0"},
	}

	// Create ranges for each parameter
	ports := makeRange(0, 3)      // [0,1,2,3]
	baudRates := makeRange(0, 9)  // [0-9]
	parity := makeRange(0, 2)     // [0,1,2]
	dataBits := makeRange(0, 3)   // [0,1,2,3]
	stopBits := makeRange(0, 1)   // [0,1]
	flowControl := makeRange(0, 3) // [0,1,2,3]

	// Create log file
	logFileName := fmt.Sprintf("uart_attempts_%s.txt", time.Now().Format("20060102_150405"))
	logFile, err := os.Create(logFileName)
	if err != nil {
		fmt.Printf("Error creating log file: %v\n", err)
		return nil
	}
	defer logFile.Close()

	fmt.Println("Starting UART parameter bruteforce...")
	fmt.Printf("Logging results to: %s\n", logFileName)

	attemptCount := 0
	client := &http.Client{}

	// Try all possible combinations
	for _, port := range ports {
		for _, baud := range baudRates {
			for _, par := range parity {
				for _, data := range dataBits {
					for _, stop := range stopBits {
						for _, flow := range flowControl {
							attemptCount++
							serialParams := []int{port, baud, par, data, stop, flow}

							payload := &Payload{
								RequestID: "3931cf5e-c22e-42a0-bf52-0952ab0df1b8",
								Serial:    serialParams,
								Voltage:   3,
							}

							// Log attempt details
							logMessage := fmt.Sprintf("\nAttempt #%d\nPort: %s, Baud: %d, Parity: %s, Data: %d, Stop: %d, Flow: %s",
								attemptCount,
								maps.PortMap[port],
								maps.BaudMap[baud],
								maps.ParityMap[par],
								maps.DataMap[data],
								maps.StopMap[stop],
								maps.FlowMap[flow])

							fmt.Println(logMessage)
							logFile.WriteString(logMessage + "\n")

							if result := tryCombination(client, url, payload); result != nil {
								successMessage := fmt.Sprintf("\nSUCCESS! Working combination found:\n%+v", payload)
								fmt.Println(successMessage)
								logFile.WriteString(successMessage)
								return payload
							}

							// Add a small delay to avoid overwhelming the server
							time.Sleep(500 * time.Millisecond)
						}
					}
				}
			}
		}
	}

	return nil
}

func tryCombination(client *http.Client, url string, payload *Payload) error {
	jsonData, err := json.Marshal(payload)
	if err != nil {
		return fmt.Errorf("error marshaling JSON: %v", err)
	}

	req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
	if err != nil {
		return fmt.Errorf("error creating request: %v", err)
	}

	req.Header.Set("Content-Type", "application/json")

	resp, err := client.Do(req)
	if err != nil {
		return fmt.Errorf("error making request: %v", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return fmt.Errorf("error reading response: %v", err)
	}

	// Check for success response
	if resp.StatusCode == 200 && bytes.Contains(bytes.ToLower(body), []byte("true")) {
		return nil
	}

	return fmt.Errorf("unsuccessful attempt")
}

func makeRange(min, max int) []int {
	result := make([]int, max-min+1)
	for i := range result {
		result[i] = min + i
	}
	return result
}