
def format_title_price(price):
    price_format = '{:,.0f}' if price > 100 else '{:,.2f}' if price > 10 else '{:,.3f}'
    return price_format.format(price) 

def format_scale_price(num, pos):

    if num < 1:
        return "{:.3f}".format(num).lstrip('0')
        
    if num < 10:
        return "{:.2f}".format(num)
        
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])
