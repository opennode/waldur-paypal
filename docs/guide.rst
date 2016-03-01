Configuration of integration with PayPal
++++++++++++++++++++++++++++++++++++++++++
First, you should obtain client_id and client_secret for PayPal REST API using `PayPal developer site <https://developer.paypal.com/webapps/developer/applications/myapps/>`_.

To setup a PayPal integration, add a block of configuration as shown in the example below.

.. code-block:: python

    # Example of settings for billing using PayPal API.
    NODECONDUCTOR_PAYPAL = {
        'BACKEND': {
            'mode': 'production',
            'client_id': '<CLIENT_ID>',
            'client_secret': '<CLIENT_SECRET>',
            'currency_name': 'USD'
        },
        'INVOICE': {
            'logo': 'robohare.png',
            'company': 'OpenNode',
            'bank': 'American Bank',
            'account': '123456789',
        }
    }
