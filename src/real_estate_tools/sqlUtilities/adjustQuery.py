def adjustQuery(query: dict):
    for key in query:
        q = query[key]
        if type(q) == str:
            if q.find("-") >= 0:
                qsplit = q.split("-")
                qsplit = [s.strip() for s in qsplit]
                lbound = f'{qsplit[0]} <= {key}'
                ubound = f'{qsplit[1]} >= {key}'
                query[key] = f'{lbound} AND {ubound}'
            elif q.find(">") or q.find("<"):
                query[key] = f'{key} {q}'
            else:
                query[key] = f'{key} = "{q}"'
        elif type(q) == list:
            query[key] = f'{key} IN ({",".join(str(x) for x in q)})'
        else:
            query[key] = f'{key} = {q}'
    return(query)