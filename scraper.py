import asyncio
from pyppeteer import launch
import re

from db import create_event, search_event, update_event, Event

async def scrape_events():
    args = [
        '--user-data-dir=/home/arlf0/.config/chromium/test',
        '--profile-directory=Default'
    ]
    browser = await launch(headless=False, args=args)

    page = await browser.newPage()
    await page.goto('https://outlook.office365.com/calendar/view/workweek')
    # TODO: login winth sso aws

    # Espera a que se cargue el calendario
    await page.waitForSelector('[aria-label^="event"]')
    events = await page.querySelectorAll('[aria-label^="event"]')
    eventos = []
    len(events)
    for event in events:
        event_text = await page.evaluate('(element) => element.getAttribute("aria-label")', event)

        regex = r'event\s+from\s+(.+?)\s+(\d{1,2}:\d{2}\s+[AP]M)\s+to\s+(\d{1,2}:\d{2}\s+[AP]M)\s+(.+?)\s+organizer\s+(.+?)\s?(recurring)?\s+event\s+shown\s+as\s+(.+)'
        match = re.match(regex, event_text)

        if match:
            day = match.group(1)
            start_hour = match.group(2)
            end_hour = match.group(3)
            description = match.group(4).split(' location ')
            name = description[0]
            link = description[1] if len(description) > 1 else None
            organizer = match.group(5)
            recurring = True if match.group(6) else False
            status = match.group(7)

            evento = {
                'day': day,
                'startHour': start_hour,
                'endHour': end_hour,
                'name': name,
                'link': link,
                'recurring': recurring,
                'organizer': organizer,
                'status': status
            }
            eventos.append(Event(**evento))
        else:
            print('No se pudo extraer información del evento')

    await browser.close()
    return eventos

async def main():
    eventos = await scrape_events()
    for evento in eventos:
        if search_event(evento.name, evento.day):
            update_event(evento)
        else:
            create_event(evento)


asyncio.get_event_loop().run_until_complete(main())

