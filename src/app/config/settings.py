import os
from dotenv import load_dotenv
from src.contexts.ferrum_bot.domain.exceptions import ConfigurationException

load_dotenv()


class Settings:
    FERRUM_URL: str = os.getenv("FERRUM_URL", "")
    FERRUM_USERNAME: str = os.getenv("FERRUM_USERNAME", "")
    FERRUM_PASSWORD: str = os.getenv("FERRUM_PASSWORD", "")
    HEADLESS: bool = os.getenv("HEADLESS", "false").lower() == "true"
    SLOW_MO: int = int(os.getenv("SLOW_MO", "100"))

    # URLs derivadas
    @property
    def login_url(self) -> str:
        return f"{self.FERRUM_URL}/login/index.php"

    @property
    def dashboard_url(self) -> str:
        return f"{self.FERRUM_URL}/my/"

    def validate(self) -> None:
        """Valida que las credenciales estén configuradas."""
        if not self.FERRUM_USERNAME or not self.FERRUM_PASSWORD:
            raise ConfigurationException(
                "Faltan credenciales. Configura FERRUM_USERNAME y FERRUM_PASSWORD en el archivo .env"
            )
        if not self.FERRUM_URL:
            raise ConfigurationException("Falta FERRUM_URL en el archivo .env")


settings = Settings()
