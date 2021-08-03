import bs4
import concurrent.futures as cf
import requests

MAIN_URL = 'https://mycar.kz'
PAGE_URL = f'{MAIN_URL}/cars/?page='
ANNOUNCEMENT_URL = f'{MAIN_URL}/announcement/'
NUMBER_OF_PAGES = 10
FIELDS = ['ИД', 'Марка', 'Модель', 'Год', 'Пробег', 'Двигатель', 'Коробка',
          'Кузов', 'Привод', 'Цвет', 'Цена']
MODEL_FIELDS = ['id', 'make', 'model', 'year', 'mileage', 'engine', 'transmission',
                'body', 'drive', 'color', 'price']


def get_announcement_ids(url):
    html_content = requests.get(url).content
    soup = bs4.BeautifulSoup(html_content, 'html.parser')
    return {
        a['href'].split('/')[-2]
        for a in soup.find_all('a', href=True) if '/announcement/' in a['href']
    }


def get_car_dict(url, id_):
    html_content = requests.get(url).content
    soup = bs4.BeautifulSoup(html_content, 'html.parser')
    make, model = [
        a.strip()
        for breadcrumb in soup.find_all('div', {'class': 'breadcrumbs__link'})
        for a in breadcrumb.find('a', href=True)
    ][1:3]
    price = soup.find(
        'div', {'class': 'right-side__price'}
    ).find('span').text.strip().replace('"', '').replace(',', '')
    params_dict = {
        'ИД': id_,
        'Марка': make,
        'Модель': model,
        'Цена': price
    }
    for row in soup.find_all('div', {'class': 'params-row'}):
        name = row.find('div', {'class': 'params-row__name'}).text.strip()
        value = row.find('div', {'class': 'params-row__value'}).text.strip() \
            .replace('"', '').replace(',', '')
        if name == 'Пробег' and value.endswith(' км'):
            value = value[:-3]
        params_dict[name] = value
    return params_dict


def scrape(number_of_pages=NUMBER_OF_PAGES):
    announcement_ids = set()
    car_dicts = []
    with cf.ThreadPoolExecutor(max_workers=10) as executor:
        future_announcement_ids = {
            executor.submit(get_announcement_ids, f'{PAGE_URL}{i}')
            for i in range(1, number_of_pages + 1)
        }
        done, _ = cf.wait(future_announcement_ids, timeout=30)
        for future in done:
            try:
                announcement_ids.update(future.result())
            except cf.TimeoutError or cf.CancelledError:
                pass
            except RuntimeError as error:
                raise error
        future_car_dicts = {
            executor.submit(get_car_dict, f'{ANNOUNCEMENT_URL}{id__}', id__)
            for id__ in announcement_ids
        }
        done, _ = cf.wait(future_car_dicts, timeout=30)
        for future in done:
            try:
                car_dicts.append(future.result())
            except cf.TimeoutError or cf.CancelledError:
                pass
            except RuntimeError as error:
                raise error
    return car_dicts
