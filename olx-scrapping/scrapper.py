try:
    import requests
    from config import cookies, headers
    import json
    import math
except:
    print("\n[!] You need to install requirements.txt [!]\n[$] pip install -r requirements.txt [$]")
    
url = "https://www.olx.uz/api/v1/offers/"

offsetPage = 0

searchItem = input("\n[~] What do you want to search: ")
page_counter = 1

total_result = []

def scrapper(offsetPage,page_counter):

    params = {
        'offset': f'{str(offsetPage)}',
        'limit': '40',
        'query': f'{searchItem.strip()}',
        'filter_refiners': '',
        'facets': '[{"field":"region","fetchLabel":true,"fetchUrl":true,"limit":30}]',
        'sl': '18480db98a0x4faed76e',
    }

    try:
        response = requests.get(url, params=params, cookies=cookies, headers=headers)

        json_file = response.json()
        json_data = json_file.get('data')

        if not json_data:
            return total_result

        json_result = json_file.get('metadata').get('total_elements')

        pages_result = math.ceil(json_result/41)

        if json_result >= 1000:
            pages_result = 25

        response_result = []

        if json_result == 0:
            print("[!!!] Nothing found [!!]")
            return

        if page_counter == 1:
            print(f'[+] Total Result: {json_result} | Pages: {pages_result}\n')

        for i in json_data:
            item_url = i.get('url')
            item_title = i.get('title')
            item_description = i.get('description')
            item_created_time = i.get('created_time')
            item_author_name = i.get('user').get('name')
            item_city = i.get('location').get('city').get('name')
            item_params = i.get('params')

            item_price = 'none'

            for key in item_params:
                if key.get('key') == 'price':
                    item_value = key.get('value')
                    item_price = item_value.get('label')

            response_result.append({'title': item_title, 'description': item_description,'price': item_price, 'url': item_url, 'created_time': item_created_time, 'author_name': item_author_name, 'city': item_city}) 
        
        total_result.append(response_result)

        page_counter+=1
        offsetPage = offsetPage + 40

        print(f'[INFO] Page {page_counter - 1} is complete! [INFO]')

        # return
        return scrapper(offsetPage,page_counter)

    except ValueError:
        print(ValueError)
        print("[!] Something going wrong [!]")

def main():
    total_json = scrapper(offsetPage,page_counter)

    with open(f"./result/{searchItem}.json", "w", encoding='utf8') as file:
        json.dump(total_json, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()