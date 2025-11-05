class Config:
    """Singleton de configuración (completar)."""
    _instance = None
    def __new__(cls, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
