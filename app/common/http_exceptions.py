from fastapi import HTTPException, status


def raise_http_404(uuid):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Crawler with UUID: {} was not found".format(uuid),
    )


def raise_http_409(contact, name):
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Combination of Crawler Contact ({}) and Crawler Name ({}) already "
        "exists, please choose another name for your crawler".format(contact, name),
    )


def raise_http_400(value1, value2):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Value {} is larger than {}".format(value1, value2),
    )
