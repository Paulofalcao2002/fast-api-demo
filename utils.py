from enum import Enum


def get_by_id(items, id, key, is_list=False, is_index=False):
    items_list = []
    for n in range(len(items)):
        item = items[n]
        if item[key] == id:
            if not is_list:
                return n if is_index else item

            items_list.append(item)

    return items_list if is_list else None


class Tags(Enum):
    movies = "Movies"
    ratings = "Ratings"
