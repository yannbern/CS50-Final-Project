def format_currency(number):
    if number.is_integer():
        return f'{int(number):,}'
    else:
        return f'{number:,.2f}'