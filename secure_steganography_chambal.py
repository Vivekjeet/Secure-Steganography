import os
from PIL import Image

def load_image_data(filename):
    img = Image.open(filename) 
    return (img.size, list(img.getdata()))

def save_image_to_file(filename, image_dimension, image_data):
    img = Image.new("RGB", image_dimension)
    img.putdata(image_data)
    img.save(filename, "PNG")
    
def key_check(secret_key):
    for letter in secret_key:
        if letter != "u" and letter != "d":
            return True
    return False

def message_check(message):
    word = [ord(x) for x in message]
    for character in word:
        if not 32 <= character <= 126:
            return True
    return False

def encryption_validation(secret_key, message):
    cond = not 3 <= len(secret_key) <= 20 or not 10 <= len(message) <= 1000 or key_check(secret_key) == True or message_check(message) == True
    return cond

def get_data_to_encrypt(image_size):
    secret_key = input("Enter Key:")                
    message = input("Enter Message:")
    size = image_size[0] * image_size[1]
    
    while size < (-(((len(message) + len(secret_key)) * 8) // -3) + 6) or encryption_validation(secret_key, message) == True:
        if encryption_validation(secret_key, message) == True:
            print("Invalid Key/Message. Please Try again.")
        else:
            print("Message and Key cannot fit in the image.")
    
        secret_key = input("Enter Key:")                
        message = input("Enter Message:")
    
    return (secret_key, message)

def encrypt_text(text, key):
    encrypted_text = ''
    word = [ord(x) for x in text]
       
    u = list(key)
    for a in range(len(word)):
        shift = len(u)
        if u[a % shift] == "d":
            shift *= -1
        word[a] = ((word[a] - 32 + shift) % 95) + 32
        
    word = [chr(y) for y in word]
        
    encrypted_text = encrypted_text.join(word)

    return encrypted_text

def char_to_ascii(word):
    ascii_values = [ord(x) for x in word]
    return ascii_values

def ascii_to_binary(ascii_values):
    binary_results = [(bin(y)[2:]).zfill(8) for y in ascii_values]
    return binary_results
    
def encode_message(image_data, binary_key, binary_encrypted_message):
    grouped_data = binary_key + ["11111111"] + binary_encrypted_message + ["11111111"]
    split_data = list("".join(grouped_data))
    unified_image_data = [y for x in image_data for y in x]
    
    for i, j in enumerate(split_data):
        if j == "0" and (unified_image_data[i])%2 == 1:
            unified_image_data[i] -= 1
        
        elif j == "1" and (unified_image_data[i])%2 == 0:
            unified_image_data[i] += 1
    
    modified_image_data = [tuple(unified_image_data[n:n+3]) for n in range (0, len(unified_image_data), 3)]
    return modified_image_data

def decode_message(image_data):
    unified_image_data = []
    
    for x in image_data:
        for y in x:
            if y%2 == 0:
                unified_image_data.append("0")
            else:
                unified_image_data.append("1")
    
    binary_message_data = ["".join(unified_image_data[n:n+8]) for n in range (0, len(unified_image_data), 8)]
    
    if binary_message_data.count("11111111") < 2:
        return (None, None)
    
    else:
        s = binary_message_data.index("11111111")
        binary_message_data[s] = "x"
        f = binary_message_data.index("11111111")
        binary_key = binary_message_data[:s]
        binary_encrypted_message = binary_message_data[s + 1 : f]
        return (binary_key, binary_encrypted_message)

def binary_to_ascii_string(binary_values):
    string_value = "".join([chr(int(binary_values[z], 2)) for z in range(len(binary_values))])
    return string_value

def decrypt_text(encrypted_text, key):
    if encryption_validation(key, encrypted_text) == True:
        print("Error: cannot decode message!")
    else:
        decrypted_text = ''
        word = [ord(x) for x in encrypted_text]
       
        u = list(key)
        for a in range(len(word)):
            shift = len(u)
            if u[a % shift] == "u":
                shift *= -1
            word[a] = ((word[a] - 32 + shift) % 95) + 32
        
        word = [chr(y) for y in word]
        
        decrypted_text = decrypted_text.join(word)

        return decrypted_text

def save_file(filename, text):
    decoded_text_file = open(filename, "w")
    decoded_text_file.write(text)
    decoded_text_file.close()
    

def main():
    
    action = input("Select program mode: (encrypt/decrypt/exit):")
    choices = ["encrypt", "decrypt", "exit"]
    
    while action != "exit":
        
        while action not in choices:
            print("Invalid input, choose a different item!")
            action = input("Select program mode: (encrypt/decrypt/exit):")
        
        if action in choices[:-1]: 
            
            filename = input("Enter image filename:")
           
            while os.path.isfile(filename) == False or (filename.endswith(".jpg") or filename.endswith(".jpeg")) == False:
                print("Invalid image file.")
                filename = input("Enter image filename:")
            
            size, image_data = load_image_data(filename)
            
            if action == "encrypt":
                secret_key, message = get_data_to_encrypt(size)
                encrypted_text = encrypt_text(message, secret_key)
                binary_key = ascii_to_binary(char_to_ascii(secret_key))
                binary_encrypted_message = ascii_to_binary(char_to_ascii(encrypted_text))
                modified_image_data = encode_message(image_data, binary_key, binary_encrypted_message)
                modified_filename = "output/modified_" + filename.split("/")[-1]
                save_image_to_file(modified_filename, size, modified_image_data)
            
            elif action == "decrypt":
                to_convert = decode_message(image_data)
                key_to_convert = to_convert[0]
                message_to_convert = to_convert[1]
                key = binary_to_ascii_string(key_to_convert)
                encrypted_text = binary_to_ascii_string(message_to_convert)
                decrypted_text = decrypt_text(encrypted_text, key)
                if decrypted_text != None:
                    lone_filename = filename.split("/")[-1]
                    new_filename = lone_filename.split(".")[0]
                    modified_filename = "output/" + new_filename + "_decoded_message.txt"
                    save_file(modified_filename, decrypted_text)
           
            action = input("Select program mode: (encrypt/decrypt/exit):")
        
    print("Thank you for using this program.")


if __name__ == "__main__":
    main()