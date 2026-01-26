import argparse
import hashlib

def get_option_by_name(first_name: str, last_name: str) -> str:
    """
    Возвращает один из трех сервисов на основе хеша имени и фамилии.
    
    Возможные варианты:
    1) "document check service"
    2) "antifraud service"
    3) "scoring service"
    """
    full_name = (first_name + last_name).strip().lower().replace(" ", "")
    hash_bytes = hashlib.md5(full_name.encode()).digest()
    hash_number = int.from_bytes(hash_bytes, byteorder='big')
    
    option = hash_number % 3
  
    services = {
        0: "document check service",
        1: "antifraud service", 
        2: "scoring service"
    }
    
    return services[option]

def main():
    parser = argparse.ArgumentParser(
        description='Выбор сервиса на основе имени и фамилии',
        epilog='Пример: uv run script.py --name Иван --surname Иванов'
    )
    parser.add_argument('-n', '--name', required=True, help='Имя пользователя')
    parser.add_argument('-s', '--surname', required=True, help='Фамилия пользователя')
    args = parser.parse_args()   
    result = get_option_by_name(args.name, args.surname)
    print(f"Вариант задания: {result}")

if __name__ == "__main__":
    main()
