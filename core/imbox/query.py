import datetime

def check_date(date_str):
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        return True
    except ValueError:
        return False

def return_date(date_str):
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None

def build_search_query(imap_attribute_lookup, **kwargs):
    query = []
    for name, value in kwargs.items():
        if str(name) != 'current_page' and str(name) != 'page_size' and value is not None:
            if str(name) == 'unread' and str(value) == 'True':
                query.append('(UNSEEN)')
            elif str(name) == 'unread' and str(value) == 'False':
                query.append('SEEN')
            elif str(name) == 'flagged' and str(value) == 'True':
                query.append('FLAGGED')
            elif str(name) == 'flagged' and str(value) == 'False':
                query.append('UNFLAGGED')
            elif isinstance(value, str) and check_date(value) and isinstance(return_date(value), datetime.date):
                query.append(imap_attribute_lookup[name].format(return_date(value).strftime('%d-%b-%Y')))
            elif isinstance(value, str) and not check_date(value) and '"' in value:
                query.append(imap_attribute_lookup[name].format(value.replace('"', "'")))
            else:
                query.append(imap_attribute_lookup[name].format(value))

    if query:
        return " ".join(query)

    return "(ALL)"
