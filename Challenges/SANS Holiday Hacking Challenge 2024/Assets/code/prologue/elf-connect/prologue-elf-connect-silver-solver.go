package main

import (
	"fmt"
	"strings"
)

func main() {
	// Define wordSets as a map of int to string slice
	wordSets := map[int][]string{
		1: {"Tinsel", "Sleigh", "Belafonte", "Bag", "Comet", "Garland", "Jingle Bells", "Mittens", "Vixen", "Gifts", "Star", "Crosby", "White Christmas", "Prancer", "Lights", "Blitzen"},
		2: {"Nmap", "burp", "Frida", "OWASP Zap", "Metasploit", "netcat", "Cycript", "Nikto", "Cobalt Strike", "wfuzz", "Wireshark", "AppMon", "apktool", "HAVOC", "Nessus", "Empire"},
		3: {"AES", "WEP", "Symmetric", "WPA2", "Caesar", "RSA", "Asymmetric", "TKIP", "One-time Pad", "LEAP", "Blowfish", "hash", "hybrid", "Ottendorf", "3DES", "Scytale"},
		4: {"IGMP", "TLS", "Ethernet", "SSL", "HTTP", "IPX", "PPP", "IPSec", "FTP", "SSH", "IP", "IEEE 802.11", "ARP", "SMTP", "ICMP", "DNS"},
	}

	// Define correctSets as a slice of int slices
	correctSets := [][]int{
		{0, 5, 10, 14}, // Set 1
		{1, 3, 7, 9},   // Set 2
		{2, 6, 11, 12}, // Set 3
		{4, 8, 13, 15}, // Set 4
	}

	// Iterate through wordSets
	for round := 1; round <= len(wordSets); round++ {
		fmt.Printf("Set %d\n", round)
		fmt.Println(strings.Repeat("=", 80))

		// For each correctSet, print the corresponding words
		for _, indices := range correctSets {
			// Create a slice to hold the selected words
			selectedWords := make([]string, len(indices))

			// Get the words at the specified indices
			for i, idx := range indices {
				selectedWords[i] = wordSets[round][idx]
			}

			fmt.Println(selectedWords)
		}
		fmt.Println(strings.Repeat("=", 80))
	}
}
