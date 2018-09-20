from collections import defaultdict


def clean(form=None):
    result = defaultdict(lambda: None)
    for k, v in form.items():
        if v is None or v == "None":
            result[k] = None
            continue
        if v is True or v == "True":
            result[k] = True
            continue
        if v is False or v == "False":
            result[k] = False
            continue
        try:
            result[k] = int(v)
            continue
        except ValueError:
            try:
                result[k] = float(v)
                continue
            except ValueError:
                result[k] = v
    return result
