from .node import *

class Document(Node, EventTarget):
    # Instance Properties
    activeElement: "Element"  # The Element that currently has focus.
    adoptedStyleSheets: list  # An array of constructed stylesheets to be used by the document.
    body: "Element"  # The <body> or <frameset> node of the current document.
    characterSet: str  # The character set being used by the document.
    childElementCount: int  # The number of child elements of the current document.
    children: list  # The child elements of the current document.
    compatMode: str  # Indicates whether the document is rendered in quirks or strict mode.
    contentType: str  # The Content-Type from the MIME Header of the current document.
    currentScript: "HTMLScriptElement"  # The <script> element currently being processed.
    doctype: "DocumentType"  # The Document Type Definition (DTD) of the current document.
    documentElement: "Element"  # The <html> element (for HTML documents).
    documentURI: str  # The document location as a string.
    embeds: list  # An HTMLCollection of the embedded <embed> elements in the document.
    featurePolicy: "FeaturePolicy"  # The FeaturePolicy interface with the feature policies applied to the document.
    firstElementChild: "Element"  # The first child element of the current document.
    fonts: "FontFaceSet"  # The FontFaceSet interface of the current document.
    forms: list  # An HTMLCollection of the <form> elements in the document.
    fragmentDirective: str  # The FragmentDirective for the current document.
    fullscreenElement: "Element"  # The element that's currently in full screen mode for this document.
    head: "Element"  # The <head> element of the current document.
    hidden: bool  # A Boolean indicating if the page is considered hidden or not.
    images: list  # An HTMLCollection of the images in the document.
    implementation: "DOMImplementation"  # The DOM implementation associated with the current document.
    lastElementChild: "Element"  # The last child element of the current document.
    links: list  # An HTMLCollection of the hyperlinks in the document.
    pictureInPictureElement: "Element"  # The element in picture-in-picture mode in this document.
    pictureInPictureEnabled: bool  # True if picture-in-picture feature is enabled.
    plugins: list  # An HTMLCollection of the available plugins.
    pointerLockElement: "Element"  # The element set as the target for mouse events while the pointer is locked.
    prerendering: bool  # Indicates if the document is in the process of prerendering.
    scripts: list  # An HTMLCollection of the <script> elements in the document.
    scrollingElement: "Element"  # The element that scrolls the document.
    styleSheets: list  # A StyleSheetList of CSSStyleSheet objects for stylesheets.
    timeline: "DocumentTimeline"  # A special instance of DocumentTimeline created on page load.
    visibilityState: str  # The visibility state of the document.

    # Methods
    def querySelector(selector: str) -> "Element":
        pass  # Returns the first element that matches the specified CSS selector.

    def querySelectorAll(selector: str) -> list:
        pass  # Returns a list of all elements that match the specified CSS selector.

    def getElementById(id: str) -> "Element":
        pass  # Returns the element with the specified ID.

    def getElementsByClassName(class_name: str) -> list:
        pass  # Returns a list of elements with the specified class name.

    def getElementsByTagName(tag_name: str) -> list:
        pass  # Returns a list of elements with the specified tag name.

    def createElement(tag:str)->Element:pass