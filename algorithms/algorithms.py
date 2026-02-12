from flask import flash
from algorithms.searching_sorting import SortingSearching

def parse_values(form):
    raw_values = form.items.data.split(',')
    
    for i in range(len(raw_values)):
        raw_values[i] = raw_values[i].strip()

        try:
            if float(raw_values[i]) % 1 == 0:
                raw_values[i] = int(raw_values[i])
            else:
                raw_values[i] = float(raw_values[i])
        except:
            pass
    
    return raw_values


def bubble_sort_handler(form):
    if not form.validate():
        last_error = None

        for field, errors in form.errors.items():
            for error in errors:
                last_error = error
        
        if last_error:
            flash(last_error, "warning")
            return None, "", [], []
    values = parse_values(form)

    sorting_searching = SortingSearching(form.is_ascending.data, None, values)


    return sorting_searching.bubble_sort()

def binary_search_handler(form):
    if not form.validate():
        last_error = None

        for field, errors in form.errors.items():
            for error in errors:
                last_error = error
        
        if last_error:
            flash(last_error, "warning")
            return None, "", [], [], None
        
    


    values = parse_values(form)

    item = form.item.data.strip()
    try:
        item = float(item)
        if item % 1 == 0:
            item = int(item)
    except ValueError:
        pass


    sorting_searching = SortingSearching(None, item, values)


    return sorting_searching.binary_search()