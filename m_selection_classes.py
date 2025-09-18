import db

def create_where_condition(params):
    where = ""

    for i in range(len(params)):
        if i == 0:
            where += "WHERE selection_classes.class_key=?"
        else:
            where += " OR selection_classes.class_key=?"

    return where

def get_selection_items(searchtypes):
    where = create_where_condition(searchtypes)
    params = [str(t) for t in searchtypes]
    sql = "SELECT selection_class_items.id AS id, class_key, item_key " \
            "FROM selection_class_items " \
            "LEFT JOIN selection_classes ON selection_class_items.class_id=selection_classes.id " \
            + where
    result = db.query_db(sql, params, resp_type = db.RespType.DICT)

    return create_selection_dict(result) if result else result

def create_selection_dict(result):
    selections = {}
    for row in result:
        class_key = row["class_key"]
        item = (row["id"], row["item_key"])

        if class_key in selections:
            selections[class_key].append(item)
        else:
            selections[class_key] = [item]

    return selections