def to_int(val):
    """convert an input string to int."""
    if isinstance(val, str):
        try:
            return int(val)
        except ValueError:
            pass
    return val

def to_float(val):
    """convert an input string to float."""
    if isinstance(val, str):
        try:
            return float(val)
        except ValueError:
            pass
    return val


def field_lookup(doc, field):
    ptr = doc
    try:
        if '.' in field:
            fields = field.split('.')
            for f in fields[:-1]:
                ptr = ptr[f]
            return ptr[fields[-1]]
        else:
            return ptr[field]   
    except KeyError:
        return None


def field_set(doc, field, val):
    ptr = doc
    try:
        if '.' in field:
            fields = field.split('.')
            for f in fields[:-1]:
                ptr = ptr[f]
            ptr[fields[-1]] = val
            return doc
        else:
            ptr[field] = val
    except KeyError:
        return doc


# def fn_convert(d, fn, convert_keys=[]):
#     ptr = d
#     for k in convert_keys:
#         field_set(d, k, fn(field_lookup(d, k)))
#     return d

# def fn_convert(d, fn, convert_keys=[], level=0):
#     """Explore document d and specified convert keys to fn().
#     Use dotfield notation for inner keys"""
#     for key, val in d.items():
#         if isinstance(val, dict):
#             d[key] = fn_convert(val, convert_keys)
#         if key in [ak.split(".")[level] for ak in convert_keys if len(ak.split(".")) > level]:
#             if isinstance(val, list) or isinstance(val, tuple):
#                 if val and isinstance(val[0],dict):
#                     d[key] = [fn_convert(v,convert_keys,level+1) for v in val]
#                 else:
#                     d[key] = [fn(x) for x in val]
#             elif isinstance(val, dict) or isinstance(val, collections.OrderedDict):
#                 d[key] = fn_convert(val, convert_keys, level+1)
#             else:
#                 d[key] = fn(val)
#     return d


# from biothings, originally
# closed to value_convert, could be refactored except this one
# is recursive for dict typed values
def fn_convert(d, fn, target_keys=[]):
    """convert string numbers into integers or floats
       skip converting certain keys in skipped_keys list"""

    for k in target_keys:
        if '.' == k[-1]:
            raise ValueError("invalid argument - target_key must not end in .")
        if '.' in k:
            idx = k.find('.')
            subfield = k[:idx]
            remaining = k[idx+1:]
            if subfield not in d.keys():
                break
            rec = d[subfield]
            if isinstance(rec, dict):
                fn_convert(rec, fn, [remaining])
            elif isinstance(rec, list):
                for r in rec:
                    fn_convert(rec, fn, [remaining])
            elif isinstance(rec, tuple):
                d[subfield] = [fn(x) if type(x) != dict else fn_convert(x, [remaining]) for x in val]
        else:
            key = k
            try:
                val = d[k]
            except KeyError:
                break
            except TypeError:
                break
            if isinstance(val, list):
                d[key] = [fn(x) for x in val]
            elif isinstance(val, tuple):
                d[key] = tuple([fn(x) for x in val])
            elif isinstance(val, str):
                d[key] = fn(val)
            else:
                pass # don't remove complex data types
    return d
