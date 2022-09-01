import base64
import wget
import settings

weights_path = settings.WEIGHTS_PATH


def from_onedrive(weights_path):

    data_bytes64 = base64.b64encode(bytes(settings.ONEDRIVE_LINK, "utf-8"))
    data_bytes64_String = (
        data_bytes64.decode("utf-8").replace("/", "_").replace("+", "-").rstrip("=")
    )

    resultUrl = (
        f"https://api.onedrive.com/v1.0/shares/u!{data_bytes64_String}/root/content"
    )

    wget.download(resultUrl, weights_path)
