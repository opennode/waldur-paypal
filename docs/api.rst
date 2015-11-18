List payments
-------------

To get a list of payments, run GET against **/api/paypal-payments/** as an authenticated user.
It contains the following fields:

- amount: specify total amount of money; the currency is specified in application's settings
- customer: URL of customer, because balance is related to particular customer

Example response:

.. code-block:: javascript

    [
        {
            "url": "http://example.com/api/paypal-payments/f85d62886e2d4947a9276d517f9516f3/",
            "uuid": "f85d62886e2d4947a9276d517f9516f3",
            "created": "2015-07-17T14:42:32.348Z",
            "modified": "2015-07-17T14:42:37.168Z",
            "state": "Created",
            "amount": "99.99",
            "customer": "http://example.com/api/customers/211ca3327de945899375749bd55dae4a/",
            "approval_url": "https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_express-checkout&token=EC-7YY98098HC144311S"
        }
    ]

Create new payment
------------------

In order to create new payment, run POST against **/api/paypal-payments/** as an authenticated user.
Request should contain the following fields: amount, customer. Example request:

.. code-block:: javascript

    {
        "amount": "99.99",
        "customer": "http://example.com/api/customers/211ca3327de945899375749bd55dae4a/"
    }

Response contains dictionary with single field named "approval_url". You should redirect to this URL in order to approve or cancel payment.
