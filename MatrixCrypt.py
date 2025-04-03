import os
import sys
import pygame
import random
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MatrixCrypt - Encryption Tool")
clock = pygame.time.Clock()

# Colors (Blue and Green theme for Encrypter15)
BLUE = (0, 128, 255)
GREEN = (0, 255, 128)
BLACK = (0, 0, 0)

# Matrix rain effect setup
FONT_SIZE = 20
font = pygame.font.SysFont("monospace", FONT_SIZE)
columns = WIDTH // FONT_SIZE
drops = [random.randint(-HEIGHT, 0) for _ in range(columns)]
chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()"

# Encryption functions
def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return iv, ct

def decrypt_message(iv, ciphertext, key):
    iv = base64.b64decode(iv)
    ct = base64.b64decode(ciphertext)
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode('utf-8')

# Matrix rain effect
def draw_matrix_rain():
    screen.fill(BLACK)
    for i in range(len(drops)):
        char = random.choice(chars)
        text = font.render(char, True, GREEN if random.random() > 0.5 else BLUE)
        x = i * FONT_SIZE
        y = drops[i] * FONT_SIZE
        screen.blit(text, (x, y))
        drops[i] += 1
        if drops[i] * FONT_SIZE > HEIGHT:
            drops[i] = random.randint(-5, 0)

# Main loop
def main():
    key = get_random_bytes(16)  # 128-bit key for AES
    print("Generated AES Key (keep this safe!):", base64.b64encode(key).decode('utf-8'))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw Matrix rain effect
        draw_matrix_rain()

        # Display instructions
        instruction = font.render("Press 1 to Encrypt, 2 to Decrypt, Q to Quit", True, BLUE)
        screen.blit(instruction, (10, HEIGHT - 30))

        pygame.display.flip()
        clock.tick(30)

        # Handle keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            message = input("Enter message to encrypt: ")
            iv, ciphertext = encrypt_message(message, key)
            print(f"IV: {iv}")
            print(f"Encrypted: {ciphertext}")
        if keys[pygame.K_2]:
            iv = input("Enter IV: ")
            ciphertext = input("Enter encrypted message: ")
            try:
                decrypted = decrypt_message(iv, ciphertext, key)
                print(f"Decrypted: {decrypted}")
            except Exception as e:
                print(f"Decryption failed: {e}")
        if keys[pygame.K_q]:
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
