def add_keyid_queryresult(result):
    array = []
    for item in result:
        obj = dict(item)
        #logging.debug(obj)
        obj["id"] = item.key.id
        #obj["importance"] = int(item.importance)
        #logging.debug(obj)
        array.append(obj)
    return array