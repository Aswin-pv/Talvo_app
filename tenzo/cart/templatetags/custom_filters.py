from django import template
from decimal import Decimal

register = template.Library()

@register.filter(name='quantity_filter')
def quantity_filter(value, arg):
    try:
        # Check if the value is a Decimal
        price = Decimal(value)
        quantity = int(arg)
        total = price * quantity
        return total
    except (ValueError, TypeError):
        return value


@register.filter(name='session_quantity')    
def session_quantity(dict, arg):
    new_dict = dict
    return new_dict[str(arg)] 


# filter to print stars , which shows the review rating
@register.filter(name='stars')
def stars(value):

    result = []     #empty list created for storing svg of stars
    full_stars = int(value)     # stores the integer part of the input value, representing the number of full stars
    decimal_part = Decimal(str(value)) % 1 #calculates the decimal part of the input value using the Decimal class to avoid floating-point precision issues

    # append svg of full stars to result
    for _ in range(full_stars):
        result.append('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-star-fill" viewBox="0 0 16 16">'
                      '<path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>'
                      '</svg>')
    
    # append svg for decimal part ie half star
    if decimal_part == 0.5:
        result.append('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-star-half" viewBox="0 0 16 16">'
                                '<path d="M5.354 5.119 7.538.792A.52.52 0 0 1 8 .5c.183 0 .366.097.465.292l2.184 4.327 4.898.696A.54.54 0 0 1 16 6.32a.55.55 0 0 1-.17.445l-3.523 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256a.5.5 0 0 1-.146.05c-.342.06-.668-.254-.6-.642l.83-4.73L.173 6.765a.55.55 0 0 1-.172-.403.6.6 0 0 1 .085-.302.51.51 0 0 1 .37-.245zM8 12.027a.5.5 0 0 1 .232.056l3.686 1.894-.694-3.957a.56.56 0 0 1 .162-.505l2.907-2.77-4.052-.576a.53.53 0 0 1-.393-.288L8.001 2.223 8 2.226z"/>'
                              '</svg>')

    # convert the list into a single string and return
    return ''.join(result)



    