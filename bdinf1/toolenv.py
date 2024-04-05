import os

def get_dbconf():
    conf = os.environ.get('DB_CONNECT_STRING')
    if conf == None:
        raise Exception("Переменные откружения не настроены")
    return conf

if __name__ == "__main__":
    print(get_dbconf())