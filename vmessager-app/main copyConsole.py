import asyncio
from pathlib import Path
from colorama import Fore, Style, init
from ic_connector import VMessageConnector

# Inicjalizacja Colorama
init(autoreset=True)

# Ścieżka do pliku tożsamości w tym samym katalogu co skrypt
IDENTITY_PEM_PATH = Path(__file__).parent / "identity.pem"

def print_header():
    """Wyświetla estetyczny nagłówek aplikacji."""
    print(Fore.CYAN + "=" * 50)
    print(Fore.CYAN + " V-MESSENGER - ZDECENTRALIZOWANY KOMUNIKATOR VOYAGER ")
    print(Fore.CYAN + "=" * 50)

def print_menu():
    """Wyświetla menu główne."""
    print(Fore.YELLOW + "--- MENU ---")
    print("1. Wyślij wiadomość")
    print("2. Sprawdź skrzynkę odbiorczą")
    print("3. Pokaż mój Principal ID")
    print("4. Pomoc")
    print("5. Sprawdź status połączenia")
    print("0. Zakończ")
    print(Fore.YELLOW + "------------")

async def main():
    """Główna funkcja aplikacji."""
    print_header()
    
    # Inicjalizacja konektora
    try:
        connector = VMessageConnector(IDENTITY_PEM_PATH)
        print(Fore.GREEN + "INFO: Pomyślnie połączono z siecią Internet Computer.")
    except Exception as e:
        print(Fore.RED + f"BŁĄD KRYTYCZNY: Nie udało się zainicjalizować konektora: {e}")
        return

    while True:
        print_menu()
        choice = input(f"{Fore.WHITE}Wybierz opcję: ")

        if choice == '1':
            print(Fore.CYAN + "-> Wysyłanie nowej wiadomości")
            recipient = input("Podaj Principal ID odbiorcy: ")
            message = input("Wpisz treść wiadomości: ")
            if not recipient or not message:
                print(Fore.RED + "BŁĄD: Odbiorca i treść wiadomości nie mogą być puste.")
                continue
            
            print("INFO: Wysyłanie w toku...")
            result = await connector.send_message(recipient, message)
            if isinstance(result, dict) and 'err' in result:
                print(Fore.RED + f"BŁĄD: {result['err']}")
            else:
                print(Fore.GREEN + f"SUKCES: Wiadomość wysłana! Odpowiedź serwera: {result}")

        elif choice == '2':
            print(Fore.CYAN + " -> Sprawdzanie skrzynki odbiorczej")
            print("INFO: Sprawdzanie...")
            result = await connector.check_messages()
            if isinstance(result, dict) and 'err' in result:
                print(Fore.RED + f"BŁĄD: {result['err']}")
            elif result == "Twoja skrzynka jest pusta":
                print(f"{Fore.YELLOW} {result}")
            else:
                print(Fore.GREEN + "--- NOWA WIADOMOŚĆ ---")
                print(result)
                print(Fore.GREEN + "----------------------")

        elif choice == '3':
            my_principal = connector.get_my_principal()
            print(Fore.CYAN + f"-> Twój Principal ID: {my_principal}")

        elif choice == '4':
            print(Fore.CYAN + "-> Pomoc kanistra vmessage")
            for i in range(3): # Zakładamy, że pomoc ma kilka stron
                help_text = await connector.get_help(i)
                if isinstance(help_text, dict) and 'err' in help_text:
                    print(Fore.RED + f"Błąd pobierania strony {i}: {help_text['err']}")
                    break
                if help_text and "NULL" not in help_text:
                    print(f"{Fore.YELLOW}--- Strona {i} ---")
                    print(help_text)
                else:
                    break

        elif choice == '5':
            print(Fore.CYAN + "-> Sprawdzanie statusu połączenia...")
            status = await connector.hwoisme()
            if isinstance(status, dict) and 'err' in status:
                print(Fore.RED + f"BŁĄD POŁĄCZENIA: {status['err']}")
            elif status is not None:
                print(Fore.GREEN + "Połączenie aktywne!")
                print(f"  Tytuł usługi: {status.get('title')}")
                print(f"  Canister ID: {status.get('conn')}")
                print(f"  Dostępne interfejsy: {status.get('conector')}")
            else:
                print(Fore.RED + "BŁĄD POŁĄCZENIA: Nie można uzyskać statusu (brak danych).")

        elif choice == '0':
            print(Fore.CYAN + "Do zobaczenia na szlaku Voyagera!")
            break

        else:
            print(Fore.RED + "Nieznana opcja, spróbuj ponownie.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("INFO: Przerwano działanie aplikacji.")
