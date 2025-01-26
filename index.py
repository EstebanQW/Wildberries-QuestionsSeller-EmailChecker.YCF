from mail_read import start_checking_mail


def handler(event, context):

    return {
        "statusCode": 200,
        "body": start_checking_mail(),
    }
