from datetime import datetime



def build_where_clause(arguments):
    argument_list = [(key.strip(), value.strip()) for key, value in arguments.items()]
    print(argument_list)
    if len(argument_list) == 0:
        return '', ''
    when_clauses = []
    limit_clause = ''
    date_range = {}
    for key, value in argument_list:
        print(key, value)
        if key == 'begin_date':
            date_range['begin'] = value
        elif key == 'end_date':
            date_range['end'] = value
        elif key == 'angry':
            when_clauses.append(f'r.angry = {value.lower() == "true"}')
        elif key == 'location':
            when_clauses.append(f'r.locations_location = \"{value}\"')
        elif key == 'count':
            limit_clause = f'LIMIT {value}'
        elif key == 'place':
            when_clauses.append(f'l.location_description = \"{value}\"')
        else:
            when_clauses.append(f'r.{key} = \'{value}\'')

        if len(date_range) > 0:
            end = date_range.get('end', datetime.now().strftime('%Y-%m-%d'))
            begin = date_range.get('begin')
            if begin is not None:
                when_clauses.append(f'raw.pub_date BETWEEN \'{begin}\' AND \'{end}\'')

        print(when_clauses)
        if len(when_clauses) > 0:
            when = f"WHERE {' AND '.join(when_clauses)} "
        else:
            when = ''
    return when, limit_clause

