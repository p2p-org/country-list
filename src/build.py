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
        phones = {
            item["name_code"]: item for item in json.load(ph)
        }

    codes = { *moonpay.keys(), *phones.keys() }

    output = []
    
    for code in sorted(codes):
        mp = moonpay.get(code) or {}
        ph = phones.get(code) or {}
        name = decode(mp.get("name") or ph.get("name"))

        if 'states' in mp and not all(s.get('isAllowed') for s in mp['states']):
            output.extend({
                'name': f"{name} ({state['name']})",
                'alpha2': code,
                'alpha3': mp.get("alpha3") or ph.get("name_code_alpha3"),
                'flag_emoji': ph.get("flag_emoji"),
                'is_striga_allowed': code in striga,
                'is_moonpay_allowed': state.get("isAllowed") or False,
            } for state in mp['states'])
        else:
            output.append({
                'name': name,
                'alpha2': code,
                'alpha3': mp.get("alpha3") or ph.get("name_code_alpha3"),
                'flag_emoji': ph.get("flag_emoji"),
                'is_striga_allowed': code in striga,
                'is_moonpay_allowed': mp.get("isAllowed") or False,
            })

    with open(RESULT_FILE, "w") as out:
        json.dump(output, out, indent=4)

def decode(value: str) -> str:
    return value.replace("&amp;", "&")

if __name__ == '__main__':
    main()
