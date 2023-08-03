import os
import json

APP_DIR = os.path.dirname(__file__)
MOONPAY_FILE = os.path.join(APP_DIR, "moonpay-availability.json")
STRIGA_FILE = os.path.join(APP_DIR, "striga-availability.json")
PHONES_FILE = os.path.join(APP_DIR, "phone-codes.json")
RESULT_FILE = os.path.join(os.path.dirname(APP_DIR), "country-list.json")

def main():
    with open(MOONPAY_FILE) as mp:
        moonpay = {
            item["alpha2"]: item for item in json.load(mp)
            }

    with open(STRIGA_FILE) as st:
        striga = set(json.load(st))

    with open(PHONES_FILE) as ph:
        phones = json.load(ph)

    output = {}
    
    for item in phones:
        output[item["name_code"]] = {
            "alpha2": item["name_code"],
            "alpha3": item["name_code_alpha3"],
            "flag_emoji": item["flag_emoji"],
            "is_striga_allowed": item["name_code"] in striga,
            "is_moonpay_allowed": item["name_code"] in moonpay,
        }

    for code, item in moonpay.items():
        if code not in output:
            output[code] = {
                "alpha2": item["alpha2"],
                "alpha3": item["alpha3"],
                "flag_emoji": None,
                "is_striga_allowed": item["alpha2"] in striga,
                "is_moonpay_allowed": True,
            }

    output = list(output.values())
    output.sort(key=lambda item: item["alpha2"])

    with open(RESULT_FILE, "w") as out:
        json.dump(output, out, indent=4)


if __name__ == '__main__':
    main()