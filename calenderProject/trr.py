events= [('2023-1-2', '222222222222222222', 'admin'), ('2023-1-4', '4444444444444444', 'admin'), ('2023-1-6', 'jnk', 'admin'), (' 2023-1-08', 'trypostman', 'admin'), ('2023-1-12', '1222221112222212121', 'admin'), ('2023-1-11', '1111111111111111111111111', 'admin'), (' 2023-1-09', 'trypostman1', 'admin'), ('2023-1-15', '15151515', 'admin'), ('2023-1-17', '171717171717 ', 'admin'), ('2023-1-19', '1911919191  ', 'admin'), ('2023-1-5', '55555555555', 'admin'), ('2023-1-9', '9999999999999999999999999999999999', 'admin'), ('2023-1-18', '1818181 ', 'admin'), ('2023-1-3', '333333333333333333333333333333', 'admin'), ('2023-1-10', '101010101010', 'admin'), ('2023-1-10', '101010', 'admin'), ('2023-1-23', '11123232323', 'admin')]
event_data = {}
event_dataT = {}
for row in events:
    date = row[0]
    event = row[1]
    print("date 261   ", date)
    
    print("date 263   ", event)
    username= row[2]
    print("username 265   ", username)
    if date in event_data:
        print("event line 263::::             ")#, event_data[date])
        event_data[date].append(event)
        #event_data[date].append(username)
        event_dataT[date].append(event)
        event_dataT[date].append(username)
    else:
        print("event line 266::::             ")#, event_data[date])
        event_data[date] = [event]
        event_dataT[date] = [event]
        event_dataT[date].append(username)
print("event_data line 269::::             ",event_dataT)