from .views import CSVDescribe, CSVGroup, LongestSequence, SequenceElements


def init_resources(api):
    print(" * Initializing resources...")
    api.add_resource(SequenceElements,
                     "/sequence/elem/<int:n>/", endpoint="elem")
    api.add_resource(
        LongestSequence, "/sequence/longest/<int:n>/", endpoint="longest")
    api.add_resource(CSVDescribe, "/iris/describe/", endpoint="describe")
    api.add_resource(
        CSVGroup, "/iris/<string:column_name>/<string:maximum>/", endpoint="group"
    )
