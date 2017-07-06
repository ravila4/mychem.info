import biothings.dataload.uploader as uploader

class DrugCentralUploader(uploader.DummySourceUploader):

    name = "drugcentral"
    __metadata__ = {
            "src_meta" : {
                "url" : "http://drugcentral.org/",
                "license_url" : "?",
                }
            }

    @classmethod
    def get_mapping(klass):
        mapping = {}

        return mapping
