class DOMTokenList:
    # Instance Properties
    length: int  # The number of tokens in the list.

    # Instance Methods
    def item(index: int) -> str:
        pass  # Returns the token at the specified index.

    def contains(token: str) -> bool:
        pass  # Returns true if the list contains the specified token.

    def add(*tokens: str) -> None:
        pass  # Adds one or more tokens to the list.

    def remove(*tokens: str) -> None:
        pass  # Removes one or more tokens from the list.

    def toggle(token: str, force: bool = None) -> bool:
        pass  # Toggles the presence of the token in the list.

    def replace(old_token: str, new_token: str) -> bool:
        pass  # Replaces an old token with a new token in the list.

    def supports(token: str) -> bool:
        pass  # Returns whether the list supports the specified token.

    def toString() -> str:
        pass  # Returns a string representing all tokens in the list, separated by spaces.


class Attr:
    # Instance Properties
    name: str  # The name of the attribute.
    value: str  # The value of the attribute.
    specified: bool  # Returns true if the attribute was explicitly set on the element.

    # Instance Methods
    def valueOf() -> str:
        pass  # Returns the value of the attribute.

    def isId() -> bool:
        pass  # Returns true if the attribute is an ID attribute.

class DOMRect:
    # Instance Properties
    x: float  # The x-coordinate of the DOMRect's top-left corner.
    y: float  # The y-coordinate of the DOMRect's top-left corner.
    width: float  # The width of the DOMRect.
    height: float  # The height of the DOMRect.
    top: float  # The y-coordinate of the DOMRect's top edge.
    right: float  # The x-coordinate of the DOMRect's right edge.
    bottom: float  # The y-coordinate of the DOMRect's bottom edge.
    left: float  # The x-coordinate of the DOMRect's left edge.

    # Instance Methods
    def toJSON() -> dict:
        pass  # Returns a JSON representation of the DOMRect (often used for serialization).


class ArrayBuffer:
    @classmethod
    def new()->'ArrayBuffer': #pyscropt constructor of js objects
        return ArrayBuffer()


class Uint8Array:
    @classmethod
    def new()->'Uint8Array': #pyscropt constructor of js objects
        return Uint8Array()

class TextEncoder:

    encoding: str #Always returns utf-8.

    @classmethod
    def new()->'TextEncoder': #pyscropt constructor of js objects
        return TextEncoder()
    

    def encode(self, string:str)->Uint8Array:
        #Takes a string as input, and returns a Uint8Array containing UTF-8 encoded text.
        pass

    def encodeInto(self, string:str, uint8Array:Uint8Array)->tuple[int,int]:
        #Takes a string to encode and a destination Uint8Array to put resulting UTF-8 encoded text into, and returns an object indicating the progress of the encoding. This is potentially more performant than the older encode() method.
        pass

