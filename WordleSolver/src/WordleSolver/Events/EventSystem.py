eventSubscribers = {}

def subscribe(eventType, fn):
     if not eventType in eventSubscribers:
         eventSubscribers[eventType] = []
     eventSubscribers[eventType].append(fn)

def unsubscribe(eventType, fn):
    if eventType in eventSubscribers:
        eventSubscribers[eventType].remove(fn)

def EventOccured(event):
    print("event!", event)
    if type(event) not in eventSubscribers:
        print("Couldn't find any fns for event of type:", type(event), "\nlooked in dict: ", eventSubscribers)
        return
    for fn in eventSubscribers[type(event)]:
        fn(event)