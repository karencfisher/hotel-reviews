from datetime import datetime
from collections import defaultdict


def build_where_clause(arguments):
    argument_list = [(key.strip(), value.strip()) for key, value in arguments.items()]
    if len(argument_list) == 0:
        return ''
    when_clauses = []
    date_range = {}
    for key, value in argument_list:
        if key == 'begin_date':
            date_range['begin'] = value
        elif key == 'end_date':
            date_range['end'] = value
        elif key == 'angry':
            when_clauses.append(f'r.angry = {value.lower() == "true"}')
        elif key == 'location':
            when_clauses.append(f'r.locations_location = \"{value}\"')
        else:
            when_clauses.append(f'r.{key} = \'{value}\'')

        if len(date_range) > 0:
            end = date_range.get('end', datetime.now().strftime('%Y-%m-%d'))
            begin = date_range.get('begin')

    if date_range.get('begin') is not None:
        when_clauses.append(f'raw.pub_date BETWEEN \'{begin}\' AND \'{end}\'')
    if len(when_clauses) > 0:
        when = f"WHERE {' AND '.join(when_clauses)} "
    else:
        when = ''
    return when


def make_review_report(result_set):
    sents = ['N/A', 'very bad', 'bad', 'neutral', 'good', 'very good']
    ordered_results = defaultdict(list)
    output = []
    for row in result_set:
        key = (row['place'], row['review_source'], row['review_id'])
        ordered_results[key].append((row['topic'], row['sentiment'], row['summary']))

    for key in ordered_results.keys():
        output.append (f'<p><b>{key[0]} ({key[1]} review {key[2]})</b><hr>')
        for item in ordered_results[key]:
            sentiment = sents[item[1]]
            output.append(f'<b>Topic:</b> {item[0]}<br><b>Sentiment:</b> {sentiment}<br><b>Summary:</b> {item[2]}<br><br>')
        output.append('</p>')
    return '\n'.join(output)
        