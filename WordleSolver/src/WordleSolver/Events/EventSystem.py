import asyncio
from typing import cast, reveal_type

eventSubscribers = {}

def subscribe(eventType, fn):
     if not eventType in eventSubscribers:
         eventSubscribers[eventType] = []
     eventSubscribers[eventType].append(fn)

def unsubscribe(eventType, fn):
    if eventType in eventSubscribers:
        eventSubscribers[eventType].remove(fn)


#TODO: run all the events on the event loop thread (ln 26 & 34)
    #This isn't a calls though, so we can't just store the event loop...
def EventOccured(event):
    if type(event) not in eventSubscribers:
        #Look for it's super type
        if len(type(event).__bases__) > 0:
            if (_EventSuperclassSearch(event, type(event).__bases__[0])):
                return
        print("Couldn't find any fns for event of type:", type(event), "\nlooked in dict: ", eventSubscribers)
        return
    
    eventLoop = asyncio.get_event_loop()
    for fn in eventSubscribers[type(event)]:
        #This only works if function is async.
            #I think it's ok to enforce all subscribers be async
            #TODO: update all to be async. Currently jsut done screen manager.
            #This has caused soemthing to stop working. Moreover, the eventloop given here is not always going to be 
                #from the correct thread, so won't be able to get the correct event loop.
                #Need to do some re-thinking here
        asyncio.ensure_future(fn(event), loop=eventLoop)
        #fn(event)

def _EventSuperclassSearch(event, curType: type):
    if curType not in eventSubscribers:
        if len(curType.__bases__) > 0:
            return _EventSuperclassSearch(event, curType.__bases__[0])
        return False
    
    eventLoop = asyncio.get_event_loop()
    for fn in eventSubscribers[curType]:
        asyncio.ensure_future(fn(event), loop=eventLoop)
        #fn(event)
    return True

