import requests
from art_data import ArtData

def search_wiki_commons(query, max_results=4, verbose=False):

    art_list =[]
    base_url = "https://commons.wikimedia.org/w/api.php"

    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query,
        "srnamespace": "6",  # Limit search to the "File" namespace
        "srprop": "timestamp|snippet",
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if "error" in data:
        print("Error occurred:", data["error"]["info"])
        return

    results = data["query"]["search"]

    for i in range(0, max_results):
        result = results[i]
        title = result["title"]
        snippet = result.get("snippet", "")
        timestamp = result["timestamp"]
        image_info = get_image_info(title)

        if image_info is not None:
            image_url = image_info["url"]
            thumb_url = image_info["thumb_url"]
            image_width = image_info["width"]
            image_height = image_info["height"]

            dimensions = [image_width, image_height]

            artwork = ArtData(title, image_url, thumb_url, dimensions)
            art_list.append(artwork)
            if verbose:
                print("Title:", artwork.title)
                print("Timestamp:", timestamp)
                print("Full Rez Image URL:", artwork.url)
                print("Thumb URL:", artwork.thumb_url)
                print(f"Image Size: {artwork.dimensions[0]} x {artwork.dimensions[1]}.")
                orientation = "Portrait" if artwork.is_portrait() else "Landscape"
                print("Orientation:", orientation)
                print("Closest Aspect Ratio:", artwork.get_closest_aspect_ratio())
                print()

    return art_list

def get_image_info(title):
    base_url = "https://commons.wikimedia.org/w/api.php"

    params = {
        "action": "query",
        "prop": "imageinfo",
        "format": "json",
        "titles": title,
        "iiprop": "url|size",
        "iiurlwidth": "606"
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    # print(data)

    page_id = list(data["query"]["pages"].keys())[0]
    if page_id == "-1":
        return None

    image_info = data["query"]["pages"][page_id]["imageinfo"][0]
    image_url = image_info["url"]
    thumb_url = image_info["thumburl"]
    image_width = image_info["width"]
    image_height = image_info["height"]

    return {
        "url": image_url,
        "thumb_url": thumb_url,
        "width": image_width,
        "height": image_height,
    }


# # Example usage
# search_query = "Van Gogh paintings"
# search_wiki_commons(search_query)