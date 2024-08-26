"""
    Clasa settings este necesara pentru a putea muta intre doua configuratii
    de stocare a conexiunii catre baza de date, una bazata pe credentiale stocate local
    si cealalta pe credentiale stocate in Azure key vault. 

"""

import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

class Settings:
    def __init__(self):
        self.STORAGE_MODE = os.getenv("STORAGE_MODE", "localfile").lower()
        
        if self.STORAGE_MODE == "azurekeyvault" and self._azure_env_vars_available():
            self.load_from_azure_keyvault()
        else:
            self.load_from_localfile()

        self.load_logging_config()    

    def _azure_env_vars_available(self):
        return all([
            os.getenv("KEY_VAULT_NAME"),
            os.getenv("DATABASE_SECRET_NAME")
        ])

    def load_from_localfile(self):
        load_dotenv()  # Load variables from .env file
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_USERNAME = os.getenv("DB_USERNAME")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")
        self.DB_NAME = os.getenv("DB_NAME")
        self.DATABASE_URL = f"mysql+pymysql://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}"

    def load_from_azure_keyvault(self):
        key_vault_name = os.getenv("KEY_VAULT_NAME")
        kv_uri = f"https://{key_vault_name}.vault.azure.net"

        # Authenticate to Azure Key Vault
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=kv_uri, credential=credential)

        # Fetch each database component from Key Vault
        self.DB_HOST = client.get_secret(os.getenv("DB_HOST_SECRET_NAME")).value
        self.DB_USERNAME = client.get_secret(os.getenv("DB_USERNAME_SECRET_NAME")).value
        self.DB_PASSWORD = client.get_secret(os.getenv("DB_PASSWORD_SECRET_NAME")).value
        self.DB_NAME = client.get_secret(os.getenv("DB_NAME_SECRET_NAME")).value

        self.DATABASE_URL = f"mysql+pymysql://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}"

    def load_logging_config(self):
        self.LOG_FILE = os.getenv("LOG_FILE", "")
        self.LOG_STREAM = os.getenv("LOG_STREAM").lower()  
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()  

settings = Settings()
