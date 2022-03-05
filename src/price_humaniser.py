
two_dp = '{:,.2f}'
three_dp = '{:,.3f}'
no_dp = '{:,.0f}'


def format_title_price(price):
    price_format = no_dp if price > 100 else two_dp if price > 10 else three_dp
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
    magnitude_char = ['', 'K', 'M', 'B', 'T'][magnitude]
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), magnitude_char)
