class RepositoryFormatter(object):
    def json_format(input_obj):
        json = {}
        json["name"] = input_obj.name
        json["updated_at"] = input_obj.get_updated_at().isoformat()
        return json
