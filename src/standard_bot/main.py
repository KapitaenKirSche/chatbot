import random

#Consts
PIZZERIA_NAME = "Krustenkrach"

#Variabels
running = True
dialogue_state = "greeting"
user_input = "init"
user_name = "Ingo Knito"
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

#Der Bot muss für jeden Teil bestimmte Sachen schreiben, erst dann kann mit dem Programm weitergegangen werden.
checkpoints = {
    "greeting": [{
        "name":
        "welcome",
        "checked":
        False,
        "phrases": [
            f"Hallo und willkommen bei der Pizzeria {PIZZERIA_NAME}! Was kann ich für dich tun?"
        ]
    }, {
        "name": "name_q",
        "checked": False,
        "phrases": [f"Was ist dein Name?", "Wie heißt du?"]
    }, {
        "name": "name_a",
        "checked": False,
        "phrases": [f"Freut mich {user_name}. Möchtest du etwas bestellen"]
    }]
}

# Warenkorb initialisieren
cart = {}


#Funktionen für das verarbeiten des inputs basierend auf dem Status der Unterhaltung
def process_input(input):
    global dialogue_state
    if dialogue_state == "greeting":
        process_input_greeting(input)


def process_input_greeting(input):
    global dialogue_state
    if "menu" in input.lower():
        show_menu()
        dialogue_state = "ordering"
    else:
        print("Bitte sagen Sie 'menu', um das Menü zu sehen.")


#Funktionen für Ausgaben des Bots
def greetings():
    """Begrüßung"""
    for dic in checkpoints["greeting"]:
        if dic["checked"] == False:
            dic["checked"] = True
            return random.choice(dic["phrases"])


def show_menu():
    """Zeigt das Menü mit Pizzen und Getränken an."""
    print("Pizzen:")
    for (pizza, price) in menu['pizzas'].items():
        print(f"{pizza[0].capitalize()+pizza[1:]}: {price}€")
    print("\nDrinks:")
    for drink, price in menu['drinks'].items():
        print(f"{drink[0].capitalize()+drink[1:]}: {price}€")


def add_to_cart(item, quantity):
    """Fügt einen Artikel in einer bestimmten Menge zum Warenkorb hinzu."""
    if item in menu['pizzas'] or item in menu['drinks']:
        if item in cart:
            cart[item] += quantity
        else:
            cart[item] = quantity
        print(f"{quantity}x {item} added to your cart.")
    else:
        print(f"Sorry, we don't have {item} on the menu.")


def remove_from_cart(item, quantity):
    """Entfernt einen Artikel in einer bestimmten Menge aus dem Warenkorb."""
    if item in cart:
        if cart[item] > quantity:
            cart[item] -= quantity
            print(f"{quantity}x {item} removed from your cart.")
        elif cart[item] == quantity:
            del cart[item]
            print(f"{item} removed from your cart.")
        else:
            print(f"You only have {cart[item]}x {item} in your cart.")
    else:
        print(f"{item} is not in your cart.")


def view_cart():
    """Zeigt den aktuellen Inhalt des Warenkorbs an."""
    if not cart:
        print("Your cart is empty.")
    else:
        print("Your cart contains:")
        for item, quantity in cart.items():
            print(
                f"{quantity}x {item[0].capitalize()+item[1:]} - {get_item_price(item)}€ each"
            )


def checkout():
    """Gibt den Gesamtpreis aus und bedankt sich für die Bestellung."""
    total = calculate_total()
    print(f"Your total is {total}€. Thank you for your order!")


def handle_order():
    """Platzhalter für Funktion zur Bearbeitung der Bestellung."""
    pass


#calc
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


def main():
    """Hauptfunktion zum Ausführen des Chatbots."""
    if dialogue_state == "greeting":
        user_input = input(greetings())


while running:
    main()
