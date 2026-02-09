from flask import flash
from algorithms.searching_sorting import SortingSearching

def parse_values(form):
    values = form.items.data.split(',')

    try:
        for i in range(len(values)):
            values[i] = float(values[i].strip())
            if values[i]%1 == 0:
                values[i] = int(values[i])
    except ValueError:
        pass
    
    return values

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

    item = form.item.data
    try:
        item = float(item)
        if item % 1 == 0:
            item = int(item)
    except ValueError:
        pass


    sorting_searching = SortingSearching(None, item, values)


    return sorting_searching.binary_search()