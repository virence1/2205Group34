def aes_decrypt(encrypted_payload):
    """
    Decrypt ciphertext using AES decryption with a key retrieved from Azure Key Vault
    :param encrypted_payload: dict
    :return: dict
    """
    # Define the Azure AD tenant ID, client ID, and client secret
    tenant_id = "7fc78b60-eb18-4991-9d0b-1c06abe3f07e"
    client_id = "08477e2d-4d95-41c2-879f-06e0e1a05956"
    client_secret = "3HU8Q~zh9k7VHZA1NknQtEeeSEt7pumb_6MXwa3N"

    # Define the Azure Key Vault URL and secret name
    vault_url = "https://ddd-key-vault.vault.azure.net/"
    secret_name = "my-secret"

    # Create the credential object
    credential = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret
    )

    # Create the secret client object and retrieve the secret value
    client = SecretClient(vault_url=vault_url, credential=credential)
    key_bytes = client.get_secret(secret_name).value

    # Decrypt the ciphertext using AES decryption
    key = key_bytes[:32]  # Use only the first 32 bytes of the key
    iv = bytes.fromhex(encrypted_payload["iv"])
    ciphertext = bytes.fromhex(encrypted_payload["ciphertext"])
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    decrypted_payload = json.loads(plaintext.decode())

    return decrypted_payload
