import requests
import sys
from config import configFile

config = configFile()
print(config)

sys.exit()
s = requests.session()

session = s.get('https://cannonkeys.com/cart.js').json()
sessionID = session['token']


print('sessionID')
print(sessionID
        )
payload = {
    'form_type': 'product',
    'id': '31916657377391'
}


response = s.post('https://cannonkeys.com/cart/add.js', data=payload)
print(response.cookies)
print('-------------------')
shopid = response.headers['x-shopid']
print('-------------------')

checkout_payload = {
        'checkout': 'Check out'
}


checkout = s.post('https://cannonkeys.com/cart', data=checkout_payload)
print(checkout.cookies)

for key, val in checkout.cookies.items():
    print(key, val)
    print('\n')


checkout_token = checkout.cookies['tracked_start_checkout']
start_session = {
    'checkout_token': checkout_token,
    'email': "benkwokdev@gmail.com",
    'origin': "modal",
    'shopify_domain': "cannon-keys.myshopify.com"
}

sesh = s.post('https://pay.shopify.com/session/start', data=start_session)

print(sesh)

print( checkout.cookies['tracked_start_checkout'])
shipping_url = 'https://cannonkeys.com/' + shopid + '/checkouts/' + checkout.cookies['tracked_start_checkout']
print(shipping_url)
shipping = s.post(shipping_url)

print(shipping)

