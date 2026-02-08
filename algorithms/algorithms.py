from flask import flash
from algorithms.searching_sorting import SortingSearching

def bubble_sort_handler(form):
    if not form.validate():
        last_error = None

        for field, errors in form.errors.items():
            for error in errors:
                last_error = error
        
        if last_error:
            flash(last_error, "warning")
            return None, "", [], []
    
    values = form.items.data.split(',')

    try:
        for i in range(len(values)):
            values[i] = float(values[i].strip())
            if values[i]%1 == 0:
                values[i] = int(values[i])
    except ValueError:
        pass

    sorting_searching = SortingSearching(form.is_ascending.data, None, values)


    return sorting_searching.bubble_sort()