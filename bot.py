import requests
from bs4 import BeautifulSoup

class Bot: 
    def __init__(self, config, url, product_id):
        self.product_id = product_id
        self.url = url
        self.config = config

        self.session = None 
        self.checkout_url = ""

    def start(self):
        self.session = requests.session()
        s = self.session

        self.start_session()

        shop_id = self.add_to_cart().headers['x-shopid']
        if shop_id == "":
            raise RuntimError('[ERR] shop_id not found. cart_response:\n', cart)

        checkout = self.checkout()
        
        checkout_token = checkout.cookies['tracked_start_checkout']

        if checkout_token == "":
            raise RuntimError('[ERR] checkout_token not found. checkout_response:\n', checkout)

        self.checkout_url = self.url + '/' + shop_id + '/checkouts/' + checkout_token

        contact_info = self.contact_info(checkout)

        shipping = self.shipping(contact_info)

        print(shipping.text)
        print(shipping)


    def start_session(self):
        print('starting session.')
        return self.session.get(self.url + '/cart.js')

    def add_to_cart(self):
        print('adding product_id ' + self.product_id + ' to cart.')
        return self.session.post(self.url + '/cart/add.js', data={ 'form_type': 'product', 'id': self.product_id }) # add product to cart

    def checkout(self):
        print('initiating checkout.')
        return self.session.post(self.url + '/cart', data={ 'checkout': 'Check out' })

    def start_pay_session(self):
        pay_session_data = {
            'checkout_token': self.checkout_token,
            'email': self.config.email,
            'origin': "modal",
            'shopify_domain': self.config['shopify_domain']
        }

        return self.session.post(self.urls.pay_session_url, data=pay_session_data)

    def contact_info(self, checkout):
        soup = BeautifulSoup(checkout.text, 'html.parser')
        forms = soup.find_all('form')

        found = None
        for form in forms:
            if form.get('data-customer-information-form') is not None:
                found = form

        inputs = found.findAll('input')
        authenticity_token = ""
        for input in inputs:
            if input.get('name') == 'authenticity_token':
                authenticity_token = input.get('value')
                break

        config = self.config

        formData = {
          "_method": "patch",
          "authenticity_token": authenticity_token,
          "previous_step": "contact_information",
          "step": "shipping_method",

          "checkout[email]": config['email'],
          "checkout[buyer_accepts_marketing]": "0",
          "checkout[shipping_address][first_name]": config['firstName'],
          "checkout[shipping_address][last_name]": config['lastName'], 
          "checkout[shipping_address][company]": "",
          "checkout[shipping_address][address1]": config['address'],
          "checkout[shipping_address][address2]": "",
          "checkout[shipping_address][city]": config['city'],
          "checkout[shipping_address][country]": config['country'],
          "checkout[shipping_address][province]": config['state'],
          "checkout[shipping_address][zip]": config['zip'],
          "checkout[shipping_address][phone]": config['phone'],

          "checkout[client_details][browser_width]": "1905",
          "checkout[client_details][browser_height]": "363",
          "checkout[client_details][javascript_enabled]": "1",
          "checkout[client_details][color_depth]": "24",
          "checkout[client_details][java_enabled]": "false",
          "checkout[client_details][browser_tz]": "600"
        }

        return self.session.post(self.checkout_url, data=formData)

    def shipping(self, contact_info):
        soup = BeautifulSoup(contact_info.text, 'html.parser')
        forms = soup.find_all('form')

        found = None
        for form in forms:
            if form.get('data-shipping-method-form') is not None:
                found = form
                break

        inputs = found.findAll('input')
        authenticity_token = ""
        for input in inputs:
            if input.get('name') == 'authenticity_token':
                authenticity_token = input.get('value')
                break

        formData = {
            '_method': 'patch',
            'authenticity_token': authenticity_token,
            'previous_step': 'shipping_method',
            'step': 'payment_method',
            'checkout[shipping_rate][id]': 'usps-Priority-16.46'
        }

        return self.session.post(self.checkout_url, data=formData)

