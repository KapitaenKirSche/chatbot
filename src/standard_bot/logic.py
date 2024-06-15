import random

#Data
words_accept = ['ja', 'auf jeden fall', 'j', 'klar']
words_decline = ['nein', 'ne', 'nicht', 'auf keinen fall']

# Consts
PIZZERIA_NAME = "Krustenkrach"

# Variabels
running = True
dialogue_state = "greeting"
user_input = "_init"
user_name = "Ingo Knito"

allowed_outputs = ["welcome"]
last_output = ""
# Menü mit Pizzen und Getränken
menu = {
    'pizzas': {
        'margherita': 8.50,
        'salami': 9.00,
        'hawaii': 9.50,
        'veggie': 8.00
    },
    'drinks': {
        'cola': 2.50,
        'wasser': 1.50,
        'bier': 3.00
    }
}

# Der Bot muss für jeden Teil bestimmte Sachen schreiben, erst dann kann mit dem Programm weitergegangen werden.
outputs = {
    "greeting": [{
        "name":
            "welcome",
        "checked":
            False,
        "phrases": [
            f"Hallo und willkommen bei der Pizzeria _pizzeria-name! Was kann ich für sie tun?"
        ]
    }, {
        "name": "name_q",
        "checked": False,
        "phrases": ["Okay. Was ist denn dein Name?", "Sehr gut. Aber wie heißt du eigentlich?"]
    }, {
        "name": 'order_q',
        "checked": False,
        "phrases": [f"Freut mich _user_name. Möchtest du etwas bestellen?"]

    }]
}

# Warenkorb initialisieren
cart = {}


# Funktionen für das verarbeiten des inputs basierend auf dem Status der Unterhaltung
def process_input(input):
    global dialogue_state
    if dialogue_state == "greeting":
        process_input_greeting(input)


def process_input_greeting(input):
    global dialogue_state, user_name, last_output, allowed_outputs
    allowed_outputs = []
    if last_output == "welcome":
        allowed_outputs.append("name_q")

    elif last_output == "name_q":  # Gerade eben nach Name gefragt
        user_name = input
        allowed_outputs.append("order_q")


# Funktionen für Ausgaben des Bots
def greetings():
    """Begrüßung"""
    global outputs, allowed_outputs, last_output, user_name
    for dic in outputs["greeting"]:
        if dic["checked"] == False:
            if dic["name"] in allowed_outputs:
                dic["checked"] = True
                last_output = dic["name"]
                return random.choice(dic["phrases"])

    return "Ich habe keine Antwort für Sie, tut mir leid."


def show_menu():
    """Zeigt das Menü mit Pizzen und Getränken an."""
    print("Pizzen:")
    for (pizza, price) in menu['pizzas'].items():
        print(f"{pizza[0].capitalize() + pizza[1:]}: {price}€")
    print("\nDrinks:")
    for drink, price in menu['drinks'].items():
        print(f"{drink[0].capitalize() + drink[1:]}: {price}€")


def add_to_cart(item, quantity):
    """Fügt einen Artikel in einer bestimmten Menge zum Warenkorb hinzu."""
    if item in menu['pizzas'] or item in menu['drinks']:
        if item in cart:
            cart[item] += quantity
        else:
            cart[item] = quantity
        print(f"{quantity}x {item} zum Warenkorb hinzugefügt.")
    else:
        print(f"Sorry, wir haben {item} nicht im Menü.")


def remove_from_cart(item, quantity):
    """Entfernt einen Artikel in einer bestimmten Menge aus dem Warenkorb."""
    if item in cart:
        if cart[item] > quantity:
            cart[item] -= quantity
            print(f"{quantity}x {item} entfernt.")
        elif cart[item] == quantity:
            del cart[item]
            print(f"{item} removed from your -cart.")
        else:
            print(f"Du hast nur {cart[item]}x {item} im Warenkorb.")
    else:
        print(f"{item} ist nicht in deinem Warenkorb.")


def view_cart():
    """Zeigt den aktuellen Inhalt des Warenkorbs an."""
    if not cart:
        print("Your cart is empty.")
    else:
        print("Your cart contains:")
        for item, quantity in cart.items():
            print(
                f"{quantity}x {item[0].capitalize() + item[1:]} - {get_item_price(item)}€ each"
            )


def checkout():
    """Gibt den Gesamtpreis aus und bedankt sich für die Bestellung."""
    total = calculate_total()
    print(f"Your total is {total}€. Thank you for your order!")


def handle_order():
    """Platzhalter für Funktion zur Bearbeitung der Bestellung."""
    pass


# calc
def get_item_price(item):
    """Gibt den Preis eines Artikels zurück."""
    if item in menu['pizzas']:
        return menu['pizzas'][item]
    elif item in menu['drinks']:
        return menu['drinks'][item]
    return 0


def calculate_total():
    """Berechnet den Gesamtpreis des Warenkorbs."""
    total = 0
    for item, quantity in cart.items():
        total += get_item_price(item) * quantity
    return total


def replace_vars(text):
    """Ersetzt Variablen im Text durch den entsprechenden Wert."""
    global user_name, PIZZERIA_NAME
    replace = {'_user_name' : user_name,
               '_pizzeria-name' : PIZZERIA_NAME}

    for (condition, new) in replace:
        text = text.replace(condition, new)

    return text