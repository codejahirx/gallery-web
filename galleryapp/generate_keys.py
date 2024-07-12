import rsa


def generate_rsa_keys():
    # Generate RSA keys
    public_key, private_key = rsa.newkeys(1024)
    print(public_key)

    # Save the public key
    with open('public_key.pem', 'wb') as f:
        f.write(public_key.save_pkcs1("PEM"))

    with open('private_key.pem', 'wb') as f:
        f.write(private_key.save_pkcs1("PEM"))

    print("RSA keys have been generated and saved to 'public_key.pem' and 'private_key.pem'.")


if __name__ == "__main__":
    generate_rsa_keys()
