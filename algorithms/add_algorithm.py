from extensions import db
from models.algorithm import Algorithm

def add_algorithm():
    new_algorithm = Algorithm(
        url_for = "binary_search",
        name = "Binary Search",
        image_location = "/static/uploads/Binary-Search.png",
        category = "Searching",
        description = "An algorithm which looks for an item by dividing the number of items to search in half each time until the specified item is found.",
        time_complexity = "O(logn)",
        difficulty_level = "Medium",
        spec_ref = "COMPSCI"
    )

    db.session.add(new_algorithm)
    db.session.commit()