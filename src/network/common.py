class JSON:
    """
    import Python-commands as JSON Javascript-commands
    """

    from json import dumps
    from json import loads


def encode_packet(_type: str, data: any or None = None) -> str:
    """
    encodes the given type & data to a packet
    :param _type:
    :param data:
    :return:
    """
    packet = JSON.dumps({"_type": _type, "data": data})
    return packet


def decode_packet(data: str) -> tuple:
    """
    decodes the given data to a tuple with key-value
    :param data:
    :return:
    """

    temp = JSON.loads(data)
    return temp["_type"], temp["data"]
