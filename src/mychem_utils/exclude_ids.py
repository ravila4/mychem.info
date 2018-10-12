from vconvert import remove_key

import biothings, config
biothings.config_for_app(config)


class ExcludeFieldsById(object):

    def __init__(self, field_lst):
        """
        Fields to truncte are specified by field_lst.  The
        dot-notation is accepted.
        """
        self.field_lst = field_lst

    def __call__(self, f):
        """
        Truncate specified fields for on all documents on call.
        :param f: function to apply to
        :return:
        """
        def wrapped_f(*args):
            input_docs = f(*args)
            for doc in input_docs:
                if doc['_id'] in config.EXCLUSION_IDS:
                    for field in self.field_lst:
                        remove_key(doc, field)
                yield doc
        return wrapped_f
