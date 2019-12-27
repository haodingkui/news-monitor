from eventregistry import *
import time

# er = EventRegistry(apiKey = "a524dd31-3965-4696-bc5c-bc72a3361637")
er = EventRegistry(apiKey = "263326fd-0615-4a1b-8b51-945d6aa9fed8")


starttime = time.time()
while True:
    q = QueryEvents(
        lang = "zho",
        # keywords = "习近平",
        dateStart = "2019-12-23",
        dateEnd = "2019-12-25",
        minArticlesInEvent = 10,
        ignoreSourceUri = er.getSourceUri("epochtimes"),
        # sourceLocationUri = er.getLocationUri("China"),
        categoryUri = er.getCategoryUri("news:Business")
        )
    q.setRequestedResult(
        RequestEventsRecentActivity(
            # download at most 2000 events. if less of matching events were added/updated in last 10 minutes, less will be returned
            maxEventCount=2000,
            # consider articles that were published at most 10 minutes ago
            updatesAfterMinsAgo = 10
        ))
    q.setRequestedResult(RequestEventsInfo(sortBy = "date"))

    ret = er.execQuery(q)

    events = ret['events']['results']
    # for eventUri in activity:
    for event in events:
        if 'zho' in event['articleCounts'].keys():
            print(event['title']['zho'])
            print(event['eventDate'])
            if event['location']:
                print(event['location'])
            print(event['concepts'])
        print('-------------------------')

    # wait exactly a minute until next batch of new content is ready
    print("sleeping for 10 minutes...")
    time.sleep(10 * 60.0 - ((time.time() - starttime) % 60.0))