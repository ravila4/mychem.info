from hub.dataload.sources.drugbank.dotstring import remove_key


class ExcludeFieldsById(object):

    def __init__(self, exclusion_ids, field_lst):
        """
        Fields to truncate are specified by field_lst.  The
        dot-notation is accepted.
        """
        self.exclusion_ids = exclusion_ids
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
                if doc['_id'] in self.exclusion_ids:
                    for field in self.field_lst:
                        remove_key(doc, field)
                yield doc
        return wrapped_f
