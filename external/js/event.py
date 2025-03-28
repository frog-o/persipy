class EventListener:
    # Instance Methods
    def handleEvent(event: "Event") -> None:
        pass  # This method is called when the event is dispatched to the target.




class EventTarget:
    # Instance Methods
    def addEventListener(event_type: str, callback: "EventListener", options: dict = None) -> None:
        pass  # Registers an event handler for a specific event type on the EventTarget.

    def removeEventListener(event_type: str, callback: "EventListener", options: dict = None) -> None:
        pass  # Removes an event listener from the EventTarget.

    def dispatchEvent(event: "Event") -> bool:
        pass  # Dispatches an event to the EventTarget.

class Event(EventTarget):
    # Instance Properties
    type: str  # The type of the event (e.g., "click", "keydown").
    target: "EventTarget"  # The target of the event (the object that triggered the event).
    currentTarget: "EventTarget"  # The current target of the event (the object to which the event handler is attached).
    eventPhase: int  # The phase of the event flow (capturing, at target, or bubbling).
    bubbles: bool  # Whether the event bubbles up through the DOM.
    cancelable: bool  # Whether the event can be canceled.
    defaultPrevented: bool  # Whether the event's default action has been prevented.
    isTrusted: bool  # Whether the event is trusted (e.g., initiated by the user).
    timeStamp: int  # The time at which the event was created.
    composed: bool  # Whether the event will trigger listeners outside of the shadow DOM.

    # Instance Methods
    def stopPropagation() -> None:
        pass  # Prevents the event from propagating to the next event listener.

    def stopImmediatePropagation() -> None:
        pass  # Prevents the event from propagating and stops other listeners from being called.

    def preventDefault() -> None:
        pass  # Prevents the event's default action (e.g., preventing a form submission).

    def initEvent(type: str, bubbles: bool, cancelable: bool) -> None:
        pass  # Initializes the event with the specified type, bubbling, and cancelable flags.

    def initEvent(type: str, bubbles: bool, cancelable: bool, detail: int = 0) -> None:
        pass  # Initializes the event with additional details for custom events (e.g., mouse click count).
