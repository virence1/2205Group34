# Key vault config. Do not touch.

from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

def keyVault(mode, secret_name, secret_value_to_store=None):
    tenant_id = "7fc78b60-eb18-4991-9d0b-1c06abe3f07e"
    client_id = "08477e2d-4d95-41c2-879f-06e0e1a05956"
    client_secret = "3HU8Q~zh9k7VHZA1NknQtEeeSEt7pumb_6MXwa3N"

    vault_url = "https://ddd-key-vault.vault.azure.net/"

    credential = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret
    )

    client = SecretClient(vault_url=vault_url, credential=credential)

    if mode == 'set':
        client.set_secret(secret_name, secret_value_to_store)
        return f"Secret {secret_name} stored successfully."

    elif mode == 'get':
        secret_value = client.get_secret(secret_name).value
        return secret_value

    else:
        return "Invalid mode. Use 'set' or 'get'."