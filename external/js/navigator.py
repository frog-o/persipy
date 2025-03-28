from storage import *
class Navigator:
    userAgent: str
    platform: str
    language: str
    languages: list[str]
    cookieEnabled: bool
    hardwareConcurrency: int
    product: str
    vendor: str
    vendorSub: str
    appVersion: str
    appName: str
    geolocation: object  # For simplicity, assuming it's an object, can expand further.
    storage: StorageManager
