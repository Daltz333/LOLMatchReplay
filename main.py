import cassiopeia as cass
import arrow
from cassiopeia import Summoner

from lcu_driver import Connector

connector = Connector()

api_key = 'NO'

die = False

def init(region):
    cass.set_riot_api_key(api_key)
    cass.set_default_region(region)

async def flow(region, name, connection):
    summoner = Summoner(name=name, region=region)
    matches = summoner.match_history

    i = 0
    for match in matches:
        if i > 20:
            break

        print(i, match.participants[summoner].champion.name, match.creation.to('US/Eastern').format())

        i+=1

    while True:
        try:
            match_num = input("Please select a match number: ")
            break
        except:
            print("Invalid match number! Retry!")
            pass

    await connection.request('post', '/lol-replays/v1/rofls/' + str(matches[int(match_num)].id) + '/watch', data={'componentType': 'string'})

@connector.ready
async def connect(connection):
    print('LCU API is ready to be used!')

    while True:
        try:
            region = input("Please enter a region (NA, EU, JP): ")
            name = input("Please enter a summoner name (BobRoss): ")
            break
        except:
            print("Invalid! Please retry!")
            pass

    init(region)
    await flow(region, name, connection)

@connector.close
async def disconnect(connection):
    print('Finished!')


while not die:
    try:
        connector.start()
        die = True
    except Exception as e:
        print(e)
        input("There was an issue! Please ensure league is open and this is ran as administrator! Press enter to retry!")
        pass