# TR : Hugging Face model indirme aracı
# EN : Hugging Face model download tool
# Developed by Gokhan Ozgezer
# github : gokhanozgezer

import os
import sys
import json
import locale
import signal
from huggingface_hub import login, list_models, snapshot_download

# TR : İptal durumunu takip etmek için global bayrak
# EN : Global flag to track cancellation
cancelled = False

def signal_handler(sig, frame):
    """ TR : CTRL + C'yi kullanarak iptali düzgün bir şekilde ele alın. / EN : Handle cancellation gracefully. """
    global cancelled
    cancelled = True
    print(get_message("download_cancel"))
    exit(0)

# TR : Sinyal işleyiciyi kaydet
# EN : Register the signal handler
if sys.platform == 'win32':
    signal.signal(signal.SIGINT, signal_handler)  # Windows'ta
else:
    signal.signal(signal.SIGINT, signal_handler)  # macOS/Linux'ta

def load_translations():
    """ TR : Çevirileri JSON dosyasından yükle. / EN: Load translations from the JSON file. """
    with open("messages.json", "r", encoding="utf-8") as f:
        return json.load(f)

def get_language():
    """ TR : Sistem dilini belirle. / EN : Detect the system language. """
    lang_code = os.getenv("LANG") or locale.getdefaultlocale()[0] or "en"
    
    if not lang_code:  # TR : Eğer lang_code None dönerse / EN : If lang_code returns None
        return "en"
    
    if lang_code.startswith("tr"):
        return "tr"
    return "en"

# TR : Çevirileri yükle ve geçerli dil belirle
# EN : Load translations and determine the current language
translations = load_translations()
language = get_language()

def get_message(key, **kwargs):
    """ TR : Geçerli dil için uygun mesajı al. / EN : Retrieve the appropriate message for the current language. """
    message = translations[language].get(key, "")
    return message.format(**kwargs)
def load_cached_token():
    """ TR : Mevcut Hugging Face API token'ını önbellekten yükle. / EN : Load cached Hugging Face API token if available. """
    token_path = os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "token")
    if os.path.exists(token_path):
        with open(token_path, "r", encoding="utf-8") as f:
            token = f.read().strip()
            if token:
                return token
    return None
def authenticate_huggingface():
    """ TR : Hugging Face API token'ı kullanarak kimlik doğrulaması yap. / EN : Authenticate using Hugging Face API token. """
    token = load_cached_token()

    if token:
        print(get_message("cached_token"))
    else:
        try:
            token = input(get_message("enter_api")).strip()
            if token.lower() == 'q':
                print(get_message("exit_message"))
                exit(0)
        except EOFError:
            print(get_message("input_interrupted"))
            exit(0)

    try:
        login(token, add_to_git_credential=True)
        print(get_message("success_login"))
        return True
    except Exception as e:
        print(f"Login error: {str(e)}")
        print(get_message("invalid_token"))
        return False

def download_model(model_id):
    """ TR : Modeli indir ve sadece eksik dosyaları tamamla. / EN : Download the model and only complete missing files. """
    global cancelled

    download_path = os.path.join(os.getcwd(), "models", model_id.replace("/", "_"))
    os.makedirs(download_path, exist_ok=True)

    print(get_message("download_start", model_id=model_id))

    try:
        snapshot_download(repo_id=model_id, local_dir=download_path, force_download=False)
        if not cancelled:
            if os.name == 'posix':
                os.system('clear')  # macOS ve Linux
            else:
                os.system('cls')  # Windows
            print(get_message("download_success", model_id=model_id))
    except Exception as e:
        if cancelled:
            print(get_message("download_cancel"))
        else:
            print(f"Error: {str(e)}")
    finally:
        exit(0)

def main():
    """ TR : Ana program döngüsü. / EN : Ana program döngüsü. """
    print(get_message("welcome"))

    try:
        if not authenticate_huggingface():
            return

        while True:
            try:
                # TR : Kullanıcıdan arama sorgusu al
                # EN : Get the search query from the user
                query = input(get_message("search_prompt")).strip()
                if query.lower() == 'q':
                    print(get_message("exit_message"))
                    break

                # TR : Modelleri ara ve sonuçları göster
                # EN : Search for models and show the results
                results = list(list_models(search=query, limit=10))
                if not results:
                    print(get_message("model_not_found", query=query))
                    continue

                # TR : Modelleri listele ve iptal seçeneği ekle
                # EN : List the models and add a cancel option
                for idx, model in enumerate(results):
                    print(f"{idx}. {model.modelId}")
                print(f"{len(results)}. {get_message('cancel_option')}")  # TR : İptal seçeneği / EN : Cancel option

                # TR : Kullanıcıdan model numarası seçmesini iste
                # EN : Ask the user to choose a model number
                choice = input(get_message("prompt_choice", max=len(results))).strip()

                # TR : 'q' ile çıkış yapma veya iptal seçeneğini kontrol et
                # EN : Check for 'q' to exit or the cancel option
                if choice.lower() == 'q':
                    print(get_message("exit_message"))
                    break
                elif choice == str(len(results)):  # TR : Eğer iptal seçeneği seçildiyse / EN : If the cancel option is selected
                    print(get_message("cancel_search"))
                    continue  # TR : Yeni arama yapabilmesi için döngüye dön / EN : Return to the loop to make a new search

                # TR : Seçimi sayıya dönüştür ve geçerli olup olmadığını kontrol et
                # EN : Convert the choice to a number and check if it is valid
                choice = int(choice)
                if 0 <= choice < len(results):
                    download_model(results[choice].modelId)
                else:
                    print(get_message("invalid_choice"))
            except ValueError:
                print(get_message("invalid_choice"))
    except KeyboardInterrupt:
        print(get_message("exit_message"))
        exit(0)

if __name__ == "__main__":
    main()
