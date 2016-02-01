List payments
-------------

To get a list of payments, run GET against **/api/paypal-payments/** as an authenticated user.
You may filter payments by customer UUID using `customer` parameter.

Each payment object contains the following fields:

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
User can create payment only for owned customers or for any customer if user is staff.
Request should contain the following fields: amount, customer, return_url, cancel_url.

These URLs usually correspond to frontend application.
If payment is approved PayPal will redirect user to return_url appending fields paymentId, PayerID.
For example: http://example.com/api/return/?paymentId=PAY-9T203937VX119544XK2ONUWA&token=EC-39L024900R781241G&PayerID=LADSTLPRRPH3C
Then client-side script should issue new request for approving payment using provided fields.

Example request:

.. code-block:: javascript

    {
        "amount": "99.99",
        "customer": "http://example.com/api/customers/211ca3327de945899375749bd55dae4a/",
        "return_url": "http://frontend.example.com/return/",
        "cancel_url": "http://frontend.example.com/cancel/"
    }

Response contains dictionary with single field named "approval_url".
You should redirect to this URL in order to approve or cancel payment.

Approve pending payment
-----------------------

In order to approve payment, run POST against **/api/paypal-payments/approve/** as an authenticated user.
User can approve payment only for owned customers or for any customer if user is staff.
Request should contain the following fields: payment_id, payer_id.

Example request:

.. code-block:: javascript

    {
        "payment_id": "PAY-6RV70583SB702805EKEYSZ6Y",
        "payer_id": "7E7MGXCWTTKK2"
    }

Response contains dictionary with success or error message.
Example response:

.. code-block:: javascript

    {
        "detail": "Unable to approve payment because of invalid state."
    }


Cancel payment
--------------

In order to cancel payment, run POST against **/api/paypal-payments/cancel/** as an authenticated user.
User can cancel payment only for owned customers or for any customer if user is staff.

Request should contain payment_id only.
Response contains dictionary with success message.


List invoices
-------------

To get a list of invoices, run GET against **/api/paypal-invoices/** as an authenticated user.
You may filter payments by customer UUID using `customer` parameter.

Example response:

.. code-block:: javascript

    {
        "url": "http://example.com/api/paypal-invoices/8c791610f4194ef1b82b0bf472b6f20a/",
        "uuid": "8c791610f4194ef1b82b0bf472b6f20a",
        "total_amount": "90.00",
        "pdf": "http://example.com/api/paypal-invoices/8c791610f4194ef1b82b0bf472b6f20a/pdf/",
        "start_date": "2015-09-03",
        "end_date": "2015-10-03",
        "items": [
            {
                "amount": "90.00",
                "description": "Monthly fee for premium plan",
                "created_at": "2015-12-02T11:45:52.505Z"
            }
        ],
        "customer": "http://example.com/api/customers/91c7c956fa864cc2a909ca18d84e2dd0/",
        "customer_uuid": "91c7c956fa864cc2a909ca18d84e2dd0",
        "customer_name": "Walter Lebowski"
    }
]
