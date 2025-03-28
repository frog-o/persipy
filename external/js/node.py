from .event import *
from .misc import *


class Node(EventTarget):
    # Instance Properties
    nodeName: str  # The name of the node (e.g., "DIV", "P").
    nodeType: int  # The type of the node (e.g., 1 for element, 3 for text).
    nodeValue: str  # The value of the node (may vary depending on node type).
    parentNode: "Node"  # The parent node of this node.
    parentElement: "Element"  # The parent element of this node (if it's an element).
    childNodes: list  # A list of child nodes of this node.
    firstChild: "Node"  # The first child node.
    lastChild: "Node"  # The last child node.
    previousSibling: "Node"  # The node's previous sibling.
    nextSibling: "Node"  # The node's next sibling.
    #attributes: "NamedNodeMap"  # A collection of attributes for element nodes.
    #ownerDocument: "Document"  # The document that owns this node.
    isConnected: bool  # Indicates whether the node is currently connected to the DOM.
    
    # Methods
    def appendChild(new_child: "Node") -> "Node":
        pass  # Adds a new child node to the current node.

    def cloneNode(deep: bool = False) -> "Node":
        pass  # Returns a clone of the node, optionally cloning its child nodes.

    def compareDocumentPosition(other_node: "Node") -> int:
        pass  # Compares the position of the current node with another node.

    def contains(other_node: "Node") -> bool:
        pass  # Checks if the node contains the specified child node.

    def getRootNode(options: dict = None) -> "Node":
        pass  # Returns the root node of the tree (document or shadow root).

    def hasChildNodes() -> bool:
        pass  # Returns whether the node has child nodes.

    def insertBefore(new_node: "Node", reference_node: "Node" = None) -> "Node":
        pass  # Inserts a new node before a specified reference node.

    def isDefaultNamespace(namespace: str) -> bool:
        pass  # Checks if a namespace is the default namespace for this node.

    def isEqualNode(other_node: "Node") -> bool:
        pass  # Compares the current node with another node for equality.

    def isSameNode(other_node: "Node") -> bool:
        pass  # Checks if the current node is the same as another node.

    def normalize() -> None:
        pass  # Normalizes the node, merging adjacent text nodes.

    def removeChild(child: "Node") -> "Node":
        pass  # Removes a specified child node.

    def replaceChild(new_child: "Node", old_child: "Node") -> "Node":
        pass  # Replaces an old child node with a new one.

class Style:
    fontSize:str
    color:str
    display:str
    flexDirection:str
    flexWrap:str
    fontFamily:str
    backgroundColor:str


    textAlign: str; 
    fontWeight: str; 
    fontStyle: str; 
    textSecoration: str; 

    border: str

    width:str
    height:str

class classList:
    def add(value:str):pass
    def remove(value:str):pass
    def replace(oldToken:str, newToken:str):pass
    def toggle(value:str):pass
    def contains(value:str):pass


class Dataset: # A dictionary of data attributes (data-*) of the element.
    pass

class Element(Node):
    # Instance Properties
    tagName: str  # The name of the element (e.g., "DIV", "P").
    id: str  # The ID of the element.
    className: str  # The class name(s) of the element.
    localName: str  # The local name of the element.
    namespaceURI: str  # The namespace URI of the element.
    prefix: str  # The namespace prefix for the element.
    dir: str  # The text direction of the element (e.g., "ltr", "rtl").
    lang: str  # The language of the element.
    hidden: bool  # Whether the element is hidden.
    scrollTop: int  # The vertical scroll position of the element.
    scrollLeft: int  # The horizontal scroll position of the element.
    scrollWidth: int  # The total scrollable width of the element.
    scrollHeight: int  # The total scrollable height of the element.
    offsetTop: int  # The distance from the top of the element to the top of its offset parent.
    offsetLeft: int  # The distance from the left of the element to the left of its offset parent.
    offsetWidth: int  # The width of the element including padding, border, and scrollbars.
    offsetHeight: int  # The height of the element including padding, border, and scrollbars.
    clientTop: int  # The distance from the top of the element to the top of the content area.
    clientLeft: int  # The distance from the left of the element to the left of the content area.
    clientWidth: int  # The width of the element's content area.
    clientHeight: int  # The height of the element's content area.


    textContent:str
    src:str
    dataset:Dataset
    onclick:callable
    classList:classList
    style:Style
    parentElement:'Element'
    children:list['Element']
    innerHTML:str
    title:str
    href:str
    value:str
    selectedIndex:str
    onresize:callable
    onclick:callable
    onpointerdown:callable
    onchange:callable
    onscroll:callable
    onkeydown:callable
    onkeyup:callable

    def append(element:'Element')->None:pass
    def prepend(element:'Element'):pass
    def hasOwnProperty(arg:str)->bool:pass
    def cloneNode(arg:bool)->'Element':pass
    def remove()->None:pass
    def getElementById(arg:str)->'Element':pass
    def replaceWith(element:'Element'):pass



    # Instance Methods
    def getAttribute(name: str) -> str:
        pass  # Returns the value of the specified attribute.

    def setAttribute(name: str, value: str) -> None:
        pass  # Sets the value of the specified attribute.

    def removeAttribute(name: str) -> None:
        pass  # Removes the specified attribute from the element.

    def hasAttribute(name: str) -> bool:
        pass  # Returns whether the element has the specified attribute.

    def getAttributeNS(namespace: str, local_name: str) -> str:
        pass  # Returns the value of the specified attribute within the given namespace.

    def setAttributeNS(namespace: str, qualified_name: str, value: str) -> None:
        pass  # Sets the value of the specified attribute within the given namespace.

    def removeAttributeNS(namespace: str, local_name: str) -> None:
        pass  # Removes the specified attribute from the element within the given namespace.

    def hasAttributeNS(namespace: str, local_name: str) -> bool:
        pass  # Returns whether the element has the specified attribute within the given namespace.

    def getBoundingClientRect() -> "DOMRect":
        pass  # Returns the size of an element and its position relative to the viewport.

    def getClientRects() -> list:
        pass  # Returns a list of DOMRect objects representing the element's bounds.

    def querySelector(selector: str) -> "Element":
        pass  # Returns the first element within the element that matches the specified CSS selector.

    def querySelectorAll(selector: str) -> list:
        pass  # Returns a list of all elements within the element that match the specified CSS selector.

    def getElementsByTagName(tag_name: str) -> list:
        pass  # Returns a list of elements with the specified tag name.

    def getElementsByClassName(class_name: str) -> list:
        pass  # Returns a list of elements with the specified class name.

    def getElementsByName(name: str) -> list:
        pass  # Returns a list of elements with the specified name attribute.
    
    def insertAdjacentHTML(position: str, text: str) -> None:
        pass  # Inserts HTML into the DOM at the specified position relative to the element.

    def scrollIntoView(options: dict = None) -> None:
        pass  # Scrolls the element into view.

    def scrollBy(x: int, y: int) -> None:
        pass  # Scrolls the element by the specified amount along the x and y axes.

    def scrollTo(x: int, y: int) -> None:
        pass  # Scrolls the element to the specified x and y coordinates.

    def focus() -> None:
        pass  # Gives focus to the element.

    def blur() -> None:
        pass  # Removes focus from the element.

    def setAttributeNode(attribute: "Attr") -> "Attr":
        pass  # Adds a new attribute node to the element.

    def removeAttributeNode(attribute: "Attr") -> "Attr":
        pass  # Removes an attribute node from the element.

    def getElementsByTagNameNS(namespace: str, local_name: str) -> list:
        pass  # Returns elements with the specified tag name and namespace.

    def getElementsByClassNameNS(namespace: str, class_name: str) -> list:
        pass  # Returns elements with the specified class name and namespace.

    def getAttributeNode(name: str) -> "Attr":
        pass  # Returns the attribute node with the specified name.

    def getAttributeNodeNS(namespace: str, local_name: str) -> "Attr":
        pass  # Returns the attribute node within the given namespace.

    def attachShadow(options: dict) -> "ShadowRoot":
        pass  # Attaches a shadow DOM tree to the element.

    def getShadowRoot() -> "ShadowRoot":
        pass  # Returns the shadow root associated with the element.
