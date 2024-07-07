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

    # append icon of full stars to result
    for _ in range(full_stars):
        result.append('<i class="fa-solid fa-star"></i>')
    
    # append icon for decimal part ie half star
    if decimal_part == 0.5:
        result.append('<i class="fa-solid fa-star-half"></i>')

    # convert the list into a single string and return
    return ''.join(result)



    