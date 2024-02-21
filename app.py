def app():
    print("Hello world")

    api_key = get_api_key()

    print("Your key is:", api_key)


def get_api_key():
    file = open("config.txt", "r")

    return file.readline().split("=")[1]


if __name__ == "__main__":
    app()
