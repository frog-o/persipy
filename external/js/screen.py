class ScreenOrientation:
    # Instance Properties
    angle: float  # The current rotation angle of the screen (in degrees).
    type: str  # The orientation type. Can be "portrait-primary", "landscape-primary", "portrait-secondary", or "landscape-secondary".

    # Instance Methods
    def lock(orientation: str) -> None:
        pass  # Locks the screen orientation to the specified value (e.g., 'portrait', 'landscape').

    def unlock() -> None:
        pass  # Unlocks the screen orientation, allowing it to change based on the device's physical orientation.


class Screen:
    # Instance Properties
    width: int  # The width of the screen in pixels.
    height: int  # The height of the screen in pixels.
    availWidth: int  # The width of the screen, excluding taskbars and other interface elements.
    availHeight: int  # The height of the screen, excluding taskbars and other interface elements.
    colorDepth: int  # The color depth of the screen (in bits).
    pixelDepth: int  # The pixel depth of the screen (in bits).
    orientation: "ScreenOrientation"  # The current orientation of the screen (landscape or portrait).

    # Instance Methods
    def lockOrientation(orientation: str) -> None:
        pass  # Locks the orientation of the screen to the specified orientation (e.g., 'landscape', 'portrait').

    def unlockOrientation() -> None:
        pass  # Unlocks the screen orientation.
