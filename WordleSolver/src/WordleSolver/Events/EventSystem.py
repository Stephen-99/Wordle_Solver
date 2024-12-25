import asyncio

eventSubscribers = {}
eventLoop = None

def subscribe(eventType, fn):
     if not eventType in eventSubscribers:
         eventSubscribers[eventType] = []
     eventSubscribers[eventType].append(fn)

def unsubscribe(eventType, fn):
    if eventType in eventSubscribers:
        eventSubscribers[eventType].remove(fn)

def EventOccured(event):
    #Can't init eventLoop earlier since toga event loop not setup yet
    global eventLoop
    if not eventLoop:
        eventLoop = asyncio.get_event_loop()

    if type(event) not in eventSubscribers:
        #Look for it's super type
        if len(type(event).__bases__) > 0:
            if (_EventSuperclassSearch(event, type(event).__bases__[0])):
                return
        print("Couldn't find any fns for event of type:", type(event), "\nlooked in dict: ", eventSubscribers)
        return
    
    for fn in eventSubscribers[type(event)]:
        asyncio.ensure_future(fn(event), loop=eventLoop)

def _EventSuperclassSearch(event, curType: type):
    if curType not in eventSubscribers:
        if len(curType.__bases__) > 0:
            return _EventSuperclassSearch(event, curType.__bases__[0])
        return False
    
    for fn in eventSubscribers[curType]:
        asyncio.ensure_future(fn(event), loop=eventLoop)
    return True

