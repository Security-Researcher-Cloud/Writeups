package main

import (
	"crypto/aes"
	"crypto/cipher"
	"encoding/base64"
	"fmt"
	"strings"
)

// addBase64Padding ensures the Base64 string is properly padded
func addBase64Padding(data string) string {
	return data + strings.Repeat("=", (4-len(data)%4)%4)
}

// decryptAESGCMNoPadding decrypts data using AES-GCM mode with no padding
func decryptAESGCMNoPadding(keyB64, ivB64, ciphertextB64 string) (string, error) {
	// Add padding to Base64 strings
	keyB64 = addBase64Padding(keyB64)
	ivB64 = addBase64Padding(ivB64)
	ciphertextB64 = addBase64Padding(ciphertextB64)

	// Decode Base64 inputs
	key, err := base64.StdEncoding.DecodeString(keyB64)
	if err != nil {
		return "", fmt.Errorf("failed to decode key: %w", err)
	}

	iv, err := base64.StdEncoding.DecodeString(ivB64)
	if err != nil {
		return "", fmt.Errorf("failed to decode IV: %w", err)
	}

	ciphertext, err := base64.StdEncoding.DecodeString(ciphertextB64)
	if err != nil {
		return "", fmt.Errorf("failed to decode ciphertext: %w", err)
	}

	// Validate input lengths
	if len(key) != 16 && len(key) != 24 && len(key) != 32 {
		return "", fmt.Errorf("invalid key length: %d. Must be 16, 24, or 32 bytes", len(key))
	}
	if len(iv) != 12 {
		return "", fmt.Errorf("invalid IV length: %d. Must be 12 bytes", len(iv))
	}
	if len(ciphertext) < 16 {
		return "", fmt.Errorf("ciphertext too short to contain authentication tag")
	}

	// Split ciphertext and tag
	tagLength := 16 // GCM tag is always 16 bytes
	actualCiphertext := ciphertext[:len(ciphertext)-tagLength]
	tag := ciphertext[len(ciphertext)-tagLength:]

	// Create cipher block
	block, err := aes.NewCipher(key)
	if err != nil {
		return "", fmt.Errorf("failed to create cipher: %w", err)
	}

	// Create GCM mode
	aesGCM, err := cipher.NewGCM(block)
	if err != nil {
		return "", fmt.Errorf("failed to create GCM: %w", err)
	}

	// Combine the actual ciphertext and tag back together as Go's GCM implementation
	// expects them together
	fullCiphertext := append(actualCiphertext, tag...)

	// Decrypt
	plaintext, err := aesGCM.Open(nil, iv, fullCiphertext, nil)
	if err != nil {
		return "", fmt.Errorf("failed to decrypt: %w", err)
	}

	return string(plaintext), nil
}

func main() {
	// Test inputs
	base64Key := "rmDJ1wJ7ZtKy3lkLs6X9bZ2Jvpt6jL6YWiDsXtgjkXw"
	base64IV := "Q2hlY2tNYXRlcml4"

	// Get input from user
	fmt.Print("Enter base64 encoded value: ")
	var base64Ciphertext string
	fmt.Scanln(&base64Ciphertext)

	// Decrypt
	decrypted, err := decryptAESGCMNoPadding(base64Key, base64IV, base64Ciphertext)
	if err != nil {
		fmt.Printf("Decryption failed: %v\n", err)
		return
	}

	fmt.Printf("Decrypted text: %s\n", decrypted)
}
