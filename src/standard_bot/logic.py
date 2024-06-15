import random

#Data
words_accept = ['ja', 'auf jeden fall', 'j', 'klar']
words_decline = ['nein', 'ne', 'nicht', 'nichts', 'auf keinen fall']

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
        'margherita': {'price': 8.50, 'ingredients': ['käse']},
        'salami': {'price': 9.00, 'ingredients': ['salami']},
        'hawaii': {'price': 9.50, 'ingredients': ['schinken', 'ananas']},
        'veggie': {'price': 8.00, 'ingredients': ['paprika', 'pilze', 'zwiebeln']}
    },
    'drinks': {
        'cola': {'price':2.50},
        'wasser': {'price':1.50},
        'bier': {'price':3.00}
    }
}
valid_order = []
for a in menu:
    for b in menu[a]:
        valid_order.append(b)
# Der Bot muss für jeden Teil bestimmte Sachen schreiben, erst dann kann mit dem Programm weitergegangen werden.
outputs = {
    "greeting": [{
        "name": "welcome",
        "checked": False,
        "multiple" : False,
        "phrases": [f"Hallo und willkommen bei der Pizzeria _pizzeria-name! Was kann ich für sie tun?"
                    ]
    }, {
        "name": "name_q",
        "checked": False,
        "multiple" : False,
        "phrases": ["Okay. Was ist denn dein Name?", "Sehr gut. Aber wie heißt du eigentlich?"]
    }, {
        "name": 'order_general_q',
        "checked": False,
        "multiple": False,
        "phrases": [f"Freut mich _user-name. Möchtest du etwas bestellen?"]

    }],

    "ordering" : [{
        "name" : "ordering_default",
        "checked" : False,
        "multiple": False,
        "phrases" : ["Sehr schön. Um die Speisekarte zu sehen schreibe einfach 'Speisekarte'. Du kannst natürlich auch sofort bestellen (bspw. '3x Margherita und 2mal eine cola')"]
    }, {
        "name" : "show_menu",
        "checked" : False,
        "multiple": True,
        "phrases" : ["Natürlich.\n_menu"]
    }, {
        "name" : "new_order",
        "checked" : False,
        "multiple": True,
        "phrases" : ["Danke für die Aufnahme einer Bestellung _user-name! Folgendes hast du gerade bestellt: \n_show-last-order \nMöchtest du den gesamten Warenkorb ansehen oder bearbeiten, die Speisekarte begutachten, nochmehr bestellen oder bezahlen"]
    }, {
        "name" : "show_cart",
        "checked" : False,
        "multiple": True,
        "phrases" : ["Mit Vergnügen.\n_cart\nMöchtest du den Warenkorb bearbeiten? Du kannst natürlich auch schon bezahlen ('bezahlen') oder nochmehr bestellen."]
    }],

    "end_cancel" : [{
        "name" : "end",
        "checked" : False,
        "multiple": False,
        "phrases" : ["Schade. Ich wünsche dir noch einen schönen Tag _user-name, vielleicht möchtest du ja doch nochmal in Zukunft hier bestellen."]
    }]
}

# Warenkorb initialisieren
cart = {}
last_order = []

# Funktionen für das verarbeiten des inputs basierend auf dem Status der Unterhaltung
def process_input(input):
    global dialogue_state

    if dialogue_state == "greeting":
        process_input_greeting(input)
    elif dialogue_state == "ordering":
        process_input_ordering(input)



def process_input_greeting(input):
    global dialogue_state, user_name, last_output, allowed_outputs
    allowed_outputs = []
    if last_output == "welcome":
        allowed_outputs.append("name_q")
    elif last_output == "name_q":  # Gerade eben nach Name gefragt
        user_name = input
        allowed_outputs.append("order_general_q")
    elif last_output == "order_general_q":
        if did_accept(input):
            dialogue_state = "ordering"
            allowed_outputs.append("ordering_default")
        elif did_decline(input):
            dialogue_state = "end_cancel"
            allowed_outputs.append("end")



def process_input_ordering(input):
    global dialogue_state, user_name, last_output, allowed_outputs
    allowed_outputs = []
    if last_output in ["ordering_default", "show_menu"]:
        if analyse_order_and_add_to_cart(input):
            allowed_outputs.append("new_order")
    if last_output == "ordering_default":
        if "speisekarte" in input.lower():
            allowed_outputs.append("show_menu")

    elif last_output in ["new_order", "show_cart"]:
        if "warenkorb" in input.lower():
            allowed_outputs.append("show_cart")

# Funktionen für Ausgaben des Bots
def find_output(current_state):
    """Ausgabe herausfinden"""
    global outputs, allowed_outputs, last_output, user_name
    for dic in outputs[current_state]:
        if dic["checked"] == False or dic["multiple"] == True:
            if dic["name"] in allowed_outputs:
                dic["checked"] = True
                last_output = dic["name"]
                return random.choice(dic["phrases"])

    return "Ich habe keine Antwort für dich, tut mir leid."

#-----------------------------------------------------------------
def show_menu():
    """Zeigt das Menü mit Pizzen und Getränken an."""
    menu_output_string = ""

    menu_output_string += "Pizzen:"
    menu_output_string += "\n"
    for (pizza, attributes) in menu['pizzas'].items():
        menu_output_string += f"{pizza[0].capitalize() + pizza[1:]}: {attributes['price']}€"
        menu_output_string+="\n"

    menu_output_string += ("\nGetränke:")
    menu_output_string += "\n"
    for (drink, attributes) in menu['drinks'].items():
        menu_output_string += f"{drink[0].capitalize() + drink[1:]}: {attributes['price']}€"
        menu_output_string += "\n"
    return menu_output_string

def show_last_order():
    global last_order, menu
    output = ""
    for i in last_order:
        output += i
    return output

def show_cart():
    """Zeigt den aktuellen Inhalt des Warenkorbs an."""
    global cart
    if cart == {}:
        return "Dein Warenkorb ist leider noch leer."
    else:
        output = "\nWarenkorb:\n"
        price=0
        for (item, quantity) in cart.items():
            output += f"{quantity}x {item[0].capitalize() + item[1:]} - {get_item_price(item)}€ pro Stück, {get_item_price(item) * int(quantity)}€ gesamt.\n"
            price += calculate_total_cart()
        output += f"Gesamtpreis: {price}€"
        return output


#-----------------------------------------------------------------------------------------------------
def analyse_order_and_add_to_cart(input):
    """Prüft in einem Text, ob etwas bestellt worden ist, und fügt ggf. mit add_to_cart() zum Warenkorb hinzu."""
    global valid_order, last_order
    did_order = False
    input = input.replace('x',' ')
    text_list = input.split()
    for i in range(len(text_list)):
        if text_list[i].lower() not in valid_order:
            for j in range(len(text_list[i])):
                if text_list[i][j].isnumeric() == False:
                    text_list[i]=text_list[i][:j] +' '+ text_list[i][j + 1:]
        text_list[i] = text_list[i].replace(' ', '')

    currindex=-1
    for index in range(len(text_list)):
        currindex+=1
        i=text_list[currindex]
        if len(i) == 0:
            del text_list[currindex]
            currindex-=1
        elif i.lower() in valid_order:
            did_order = True

    if did_order:
        last_order=[]

    for i in range(len(text_list)):
        if text_list[i].lower() in valid_order:
            did_order = True
            if text_list[max(i-1,0)][0].isnumeric():
                add_to_cart(text_list[i].lower(), text_list[max(i-1,0)])
            else:
                add_to_cart(text_list[i].lower(), 1)
    return did_order


def add_to_cart(item, quantity):
    """Fügt einen Artikel in einer bestimmten Menge zum Warenkorb hinzu."""
    global cart, last_order, menu
    quantity = int(quantity)
    if item in menu['pizzas'] or item in menu['drinks']:
        if item in cart:
            cart[item] += quantity
        else:
            cart[item] = quantity
        last_order.append(f"{quantity}x {item}\n")

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




def checkout():
    """Gibt den Gesamtpreis aus und bedankt sich für die Bestellung."""
    total = calculate_total_cart()
    print(f"Your total is {total}€. Thank you for your order!")


def handle_order():
    """Platzhalter für Funktion zur Bearbeitung der Bestellung."""
    pass


# calc
def get_item_price(item):
    """Gibt den Preis eines Artikels zurück."""
    global menu
    if item in menu['pizzas']:
        return menu['pizzas'][item]['price']
    elif item in menu['drinks']:
        return menu['drinks'][item]['price']
    return 0


def calculate_total_cart():
    """Berechnet den Gesamtpreis des Warenkorbs."""
    global menu, cart
    total = 0
    for item, quantity in cart.items():
        total += get_item_price(item) * quantity
    return total


#--------------------------
def did_accept(input):
    global words_accept
    for phrase in words_accept:
        if phrase in input.lower():
            return True
    return False

def did_decline(input):
    global words_decline
    for phrase in words_decline:
        if phrase in input.lower():
            return True
    return False



def replace_vars(text):
    """Ersetzt Variablen im Text durch den entsprechenden Wert."""
    global user_name, PIZZERIA_NAME
    replace = {'_user-name' : user_name,
               '_pizzeria-name' : PIZZERIA_NAME,
               '_menu' : str(show_menu()),
               '_cart' : str(show_cart()),
               '_show-last-order':str(show_last_order())}

    for condition in replace:
        text = text.replace(condition, replace[condition])

    return text