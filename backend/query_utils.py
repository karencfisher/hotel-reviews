import datetime



def build_where_clause(arguments):
    argument_list = [(key.strip(), value.strip()) for key, value in arguments.items()]
    if len(argument_list) == 0:
        return '', ''
    when_clauses = []
    limit_clause = ''
    date_range = {}
    for key, value in argument_list:
        if key == 'begin_date':
            date_range['begin'] = value
        elif key == 'end_date':
            date_range['end'] = value
        elif key == 'angry':
            when_clauses.append(f'r.angry = {value.lower() == "true"}')
        elif key == 'location':
            when_clauses.append(f'r.locations_location = \'{value}\'')
        elif key == 'count':
            limit_clause = f'LIMIT {value}'
        else:
            when_clauses.append(f'r.{key} = \'{value}\'')

        if len(date_range) > 0:
            end = date_range.get('end', datetime.today().strftime('%Y-%m-%d'))
            begin = date_range.get('begin')
            if begin is not None:
                when_clauses.append(f'WHERE r.pub_date BETWEEN \'{end}\' AND \'{begin}')
    
        if len(when_clauses) > 0:
            when = f"WHEN {' AND '.join(when_clauses)} "
        else:
            when = ''
        return when, limit_clause

