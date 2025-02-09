import requests
import matplotlib.pyplot as plt
from datetime import datetime
from PIL import Image
import matplotlib as mpl

def get_tide_data(station_id):

    base_url = "https://easytide.admiralty.co.uk/Home/GetPredictionData"

    
    params = {
        'stationId': station_id,
    }

    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: HTTP {response.status_code}")

    data = response.json()

    if not data["tidalEventList"]:
        raise Exception("No tide data found in the response")
    
    tide_data = []
    for entry in data["tidalEventList"]:
        # Convert timestamp to a readable format
        date = datetime.strptime(entry['dateTime'], "%Y-%m-%dT%H:%M:%S").strftime('%Y-%m-%d %H:%M')
        height = entry['height']
        tide_data.append({'date': date, 'height': height})

    return tide_data

def render_tide_chart(location_id, img_buf):
    tide_data = get_tide_data(location_id)
    
    from datetime import datetime
    dates = [datetime.strptime(d['date'], '%Y-%m-%d %H:%M') for d in tide_data]
    heights = [d['height'] for d in tide_data]
    
    
    mpl.rcParams["text.hinting_factor"] = "1"
    mpl.rcParams["text.hinting"] = "native"
    mpl.rcParams["text.antialiased"] = "False"
    mpl.rcParams["patch.antialiased"] = "False"
    mpl.rcParams["lines.antialiased"] = "False"
    mpl.rcParams["font.family"] = "sans-serif"
    mpl.rcParams["font.sans-serif"] = "basis33"
    mpl.rcParams["font.size"] = "11"
    mpl.rcParams["axes.linewidth"] = "0.5"

    plt.figure(figsize=(4, 3))
    plt.plot(dates, heights)
    plt.title('Next 7 Days')
    plt.grid(True)
    
    # Rotate and space out date labels
    import matplotlib.dates as mdates
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
    plt.gca().set_xlim(dates[0], dates[-1])
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(7))  # Exactly 7 labels
    
    # Find daily min and max 
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
            xytext=(-15, 0),
            textcoords='offset points',
            ha='center',
            fontsize=11,
            color='red'
        )
        # Label for maximum
        plt.annotate(
            f"{values['max'][0].strftime('%-I:%p')}",
            xy=(values['max'][0], values['max'][1]),
            xytext=(14, 0),
            textcoords='offset points',
            ha='center',
            fontsize=11,
            color='blue'
        )

    plt.tight_layout()

    plt.savefig(img_buf, format='png', dpi=100, bbox_inches='tight')
    plt.close()

    img = Image.open(img_buf)

    return img









