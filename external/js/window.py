from .navigator import *
from .document import *
from .screen import *

class Window:
    navigator: Navigator
    document: Document
    screen: Screen
    scrollX: int
    scrollY: int
    innerWidth: int
    innerHeight: int
    outerWidth: int
    outerHeight: int
    pageXOffset: int
    pageYOffset: int
    screenX: int
    screenY: int
    screenLeft: int
    screenTop: int
    devicePixelRatio: float
    location: object  # This can be expanded further.
    document: object  # For simplicity, assuming it's an object, can expand further.
    history: object  # Assuming it's an object (could expand for navigation methods).
    localStorage: object  # Simulating localStorage (could be further expanded for operations).
    sessionStorage: object  # Simulating sessionStorage (could be further expanded).
    alert: callable
    confirm: callable
    prompt: callable
    setTimeout: callable
    setInterval: callable
    clearTimeout: callable
    clearInterval: callable
    fetch: callable  # For fetching resources, though Python would need `requests` or similar.
    close: callable
    open: callable
    resizeTo: callable
    scrollTo: callable
    scrollBy: callable
    requestAnimationFrame: callable
    cancelAnimationFrame: callable
    origin: str
    name: str
    top: object  # The topmost window object
    self: object  # Reference to the current window object


    # Methods for event listeners (not implemented but for type hinting)
    addEventListener: callable
    removeEventListener: callable
    dispatchEvent: callable
