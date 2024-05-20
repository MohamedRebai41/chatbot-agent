class DataService:
    def get_department_competition_result(self,data, ranks):
        results = [entry for entry in data["departments"] if entry["place"] in ranks]
        return results
    def get_individual_competition_result(self,data, ranks):
        results = [entry for entry in data["individual"] if entry["place"] in ranks]
        return results 