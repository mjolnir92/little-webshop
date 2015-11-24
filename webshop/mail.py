from flask_mail import Message
from flask import g


def sendBasketMail(basket, user):
    msg = Message("New purchase",
                  sender="dazieGh3@gmail.com",
                  recipients=["j.sjolund@gmail.com"])
    msg.body = "New purchase from:\n\n" \
               "Name:\n {} {}\n" \
               "Address:\n {}\n {} {}\n" \
               "Phone:\n {}\n" \
               "Email:\n {}\n\n".format(user.first_name, user.last_name, user.street_address,
                                        user.postal_code, user.postal_town, user.phone, user.email)
    msg.body += "Products:\n  id, amount, name\n"
    for row in basket.rows:
        msg.body += "  {}, {} pcs, {}\n".format(row['asset']['idAsset'], row['amount'], row['asset']['name'])
    mail = getattr(g, 'mail', None)
    mail.send(msg)
