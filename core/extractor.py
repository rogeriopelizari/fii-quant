def deep_extract(data, keys):
    values = []

    def walk(obj):
        if isinstance(obj, dict):

            key = obj.get("key") or obj.get("name") or obj.get("indicator")

            if key in keys and "value" in obj:
                try:
                    values.append(float(obj["value"]))
                except:
                    pass

            if "items" in obj:
                walk(obj["items"])

            for v in obj.values():
                walk(v)

        elif isinstance(obj, list):
            for i in obj:
                walk(i)

    walk(data)
    return values