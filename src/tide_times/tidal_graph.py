
import io
import inky
import requests
import matplotlib.pyplot as plt
from datetime import datetime

def get_tide_data():
    # Using NOAA Tides & Currents API
    station_id = '9414290'  # Example station ID for San Francisco
    url = f'https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date={datetime.now().strftime("%Y%m%d")}&range=168&datum=MLLW&station={station_id}&time_zone=lst_ldt&units=metric&interval=h&format=json'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        tide_data = []
        for prediction in data['predictions']:
            tide_data.append({
                'date': prediction['t'],
                'height': float(prediction['v'])
            })
        return tide_data
    except Exception as e:
        print(f"Error fetching tide data: {e}")
        return []

def save_tide_data():

    inky_display = inky.auto()    
    tide_data = get_tide_data()
    
    from datetime import datetime
    dates = [datetime.strptime(d['date'], '%Y-%m-%d %H:%M') for d in tide_data]
    heights = [d['height'] for d in tide_data]
    
    plt.figure(figsize=(4, 3))
    plt.plot(dates, heights)
    plt.title('Next 7 Days')
    
    # plt.grid(True)
    
    # Rotate and space out date labels
    import matplotlib.dates as mdates
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
    plt.gca().set_xlim(dates[0], dates[-1])
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(7))  # Exactly 7 labels
    
    # Find daily min and max only for days with full 24 hours of data
    daily_min_max = {}
    day_counts = {}
    for date, height in zip(dates, heights):
        day = date.strftime('%Y-%m-%d')
        if day not in day_counts:
            day_counts[day] = 1
        else:
            day_counts[day] += 1

    for date, height in zip(dates, heights):
        day = date.strftime('%Y-%m-%d')
        if day_counts[day] == 24:  # Only consider days with 24 data points
            if day not in daily_min_max:
                daily_min_max[day] = {'min': (date, height), 'max': (date, height)}
            else:
                if height < daily_min_max[day]['min'][1]:
                    daily_min_max[day]['min'] = (date, height)
                if height > daily_min_max[day]['max'][1]:
                    daily_min_max[day]['max'] = (date, height)

    # Add labels for min and max
    for day, values in daily_min_max.items():
        # Label for minimum
        plt.annotate(
            f"{values['min'][0].strftime('%-I:%p')}",
            xy=(values['min'][0], values['min'][1]),
            xytext=(0, -8),
            textcoords='offset points',
            ha='center',
            fontsize=8,
            color='red'
        )
        # Label for maximum
        plt.annotate(
            f"{values['max'][0].strftime('%-I:%p')}",
            xy=(values['max'][0], values['max'][1]),
            xytext=(0, 5),
            textcoords='offset points',
            ha='center',
            fontsize=8,
            color='blue'
        )

    plt.tight_layout()
    plt.savefig('/workspace/tide_plot.png', dpi=100, bbox_inches='tight')

    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')

    im = Image.open(img_buf)
    im.show(title="My Image")

    inky_display.set_image(img)
    inky_display.show()
    img_buf.close()

    plt.close()


if __name__ == '__main__':
    save_tide_data()








