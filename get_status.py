import requests
from bs4 import BeautifulSoup

protected_url = 'https://midptf01.triumf.ca/pdu/outctrl.html'

headers = { # these need to be filled out, get from curl
}

def get_status():

    session = requests.Session()
    
    login_response = session.post(protected_url, headers=headers)
    soup = BeautifulSoup(login_response.content, 'html.parser')

    laser_row = soup.find('font', string=' Laser ')
    laser_status_td = laser_row.find_parent('td').find_next_sibling('td').find_next_sibling('td')
    laser_status = laser_status_td.find('font').get_text(strip=True)

    wiener_row = soup.find('font', string=' Wiener_Crate ')
    wiener_status_td = wiener_row.find_parent('td').find_next_sibling('td').find_next_sibling('td')
    wiener_status = wiener_status_td.find('font').get_text(strip=True)

    return laser_status, wiener_status