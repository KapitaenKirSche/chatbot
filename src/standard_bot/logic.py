import random

# Consts
PIZZERIA_NAME = "Krustenkrach"
PIZZERIA_ADRESS = "Adenauerallee 50, 53332 Bornheim"
sales_big_order = [(50, 0.05), (100, 0.1), (200, 0.2)]
words_number_replace = {
    'eins': 1,
    'zwei': 2,
    'drei': 3,
    'vier': 4,
    'fünf': 5,
    'sechs': 6,
    'sieben': 7,
    'acht': 8,
    'neun': 9,
    'zehn': 10,
    'elf': 11,
    'zwölf': 12,
    'dreizehn': 13,
    'vierzehn': 14,
    'fünfzehn': 15,
    'sechzehn': 16,
    'siebzehn': 17,
    'achtzehn': 18,
    'neunzehn': 19,
    'zwanzig': 20,
    'einundzwanzig': 21,
    'zweiundzwanzig': 22,
    'dreiundzwanzig': 23,
    'vierundzwanzig': 24,
    'fünfundzwanzig': 25}

# Variables
running = True
dialogue_state = "greeting"
user_input = "_init"
user_name = "Ingo Knito"
adress = ''

allowed_outputs = ["welcome"]
last_output = ""

edit_cart_response = ""
total_after_tip = 0

last_order = []
valid_order = []

# Warenkorb initialisieren
cart = {}
ordered_cart = []

# Data
words_accept = ['ja', 'auf jeden fall', 'j', 'klar', 'yes', 'y']
words_decline = ['nein', 'ne', 'no', 'n', 'nicht', 'nichts', 'auf keinen fall']

# Menü mit Pizzen und Getränken
menu = {
    'pizzas': {
        'margherita': {'price': 8.50, 'ingredients': ['tomatensauce', 'käse']},
        'salami': {'price': 9.00, 'ingredients': ['tomatensauce', 'käse', 'salami']},
        'hawaii': {'price': 9.50, 'ingredients': ['tomatensauce', 'käse', 'schinken', 'ananas']},
        'veggie': {'price': 8.00, 'ingredients': ['tomatensauce', 'käse', 'paprika', 'pilze', 'zwiebeln']},
        'diavolo': {'price': 10.00, 'ingredients': ['tomatensauce', 'käse', 'scharfe salami', 'peperoni']},
        'calzone': {'price': 10.00, 'ingredients': ['tomatensauce', 'käse', 'schinken', 'salami', 'pilze']},
        'funghi': {'price': 8.50, 'ingredients': ['tomatensauce', 'käse', 'pilze']},
        'tonno': {'price': 9.50, 'ingredients': ['tomatensauce', 'käse', 'thunfisch', 'zwiebeln']},
        'capricciosa': {'price': 10.00, 'ingredients': ['tomatensauce', 'käse', 'schinken', 'artischocken', 'pilze', 'oliven']}
    },
    'drinks': {
        'cola': {'price': 2.50},
        'fanta': {'price': 2.50},
        'sprite': {'price': 2.50},
        'wasser': {'price': 1.00},
        'bier': {'price': 3.00},
        'wein': {'price': 4.00},
        'espresso': {'price': 1.50},
        'cappuccino': {'price': 2.00},
        'macchiato': {'price': 2.50},
        'flatwhite': {'price': 2.50},
        'latte': {'price': 3.00}
    },
    'sides': {
        'pommes': {'price': 2.50},
        'salat': {'price': 3.50},
        'oliven': {'price': 2.00},
        'knoblauchbrot': {'price': 3.00}
    }
}

# Der Bot muss für jeden Teil bestimmte Sachen schreiben, erst dann kann mit dem Programm weitergegangen werden.
outputs = {
    "greeting": [{
        "name": "welcome",
        "checked": False,
        "multiple": False,
        "phrases": [f"Hallo und willkommen bei der Pizzeria _pizzeria-name! Wie darf ich Sie nennen?"
                    ]
    }, {
        "name": 'order_general_q',
        "checked": False,
        "multiple": False,
        "phrases": [f"Freut mich _user-name. Möchtest du etwas bestellen?"]

    }],

    "ordering": [{
        "name": "ordering_innit",
        "checked": False,
        "multiple": False,
        "phrases": [
            "Sehr schön. Um die Speisekarte zu sehen schreibe einfach 'Speisekarte'. Du kannst natürlich auch sofort bestellen (bspw. '3x Margherita und 2mal eine cola'). \nTipp: du kannst mit dem Schlüsselwort 'help' oder 'info' immer Hilfe bekommen."]
    }, {
        "name": "ordering_default",
        "checked": False,
        "multiple": True,
        "phrases": [
            "Um die Speisekarte zu sehen schreibe einfach 'Speisekarte'. Du kannst natürlich auch sofort bestellen (bspw. '3x Margherita und 2mal eine cola'), den Warenkorb anschauen & bearbeiten oder schon bezahlen."]
    }, {
        "name": "show_menu",
        "checked": False,
        "multiple": True,
        "phrases": ["Natürlich.\n_menu"]
    }, {
        "name": "new_order",
        "checked": False,
        "multiple": True,
        "phrases": [
            "Danke für die Aufnahme einer Bestellung _user-name! Folgendes hast du gerade bestellt: \n_show-last-order \nMöchtest du den gesamten Warenkorb ansehen oder bearbeiten, die Speisekarte begutachten, nochmehr bestellen('z.B. 2 mal magherita) oder bezahlen?"]
    }, {
        "name": "show_cart",
        "checked": False,
        "multiple": True,
        "phrases": [
            "Gerne.\nWarenkorb:\n_cart\nMöchtest du den Warenkorb bearbeiten? Du kannst natürlich auch schon bezahlen ('bezahlen'), nochmehr bestellen ('z.B. 2xCola) oder die Speisekarte anschauen."]
    }, {
        "name": "warenkorb_bearbeiten_innit",
        "checked": False,
        "multiple": True,
        "phrases": ["Natürlich.\n_edit-cart"]
    }, {
        "name": "warenkorb_bearbeiten",
        "checked": False,
        "multiple": True,
        "phrases": [
            "_analyse-edit-cart\n\n_edit-cart\nWenn du den Warenkorb nicht mehr bearbeiten möchtest, schreibe einfach 'abbbrechen'. Du kannst natürlich auch wie immer noch mehr bestellen, die Speisekarte begutachten, etc."]
    }, {
        "name": "help",
        "checked": False,
        "multiple": True,
        "phrases": ["Du bist gerade beim bestellmodus. Du kannst meistens folgende Aktionen ausführen:"
                    "\nBestellen: Dafür einfach schreiben was du auf den Warenkorb hinzufügen möchtest (Bsp.: 'dreimal Cola und 2xSalami')"
                    "\nWarenkorb ansehen: Alle bestellten Sachen aufgelistet haben (Bsp.: 'Ich würde gerne den Warenkorb sehen.')"
                    "\nSpeisekarte: Um die ganze Speisekarte mitsamt Preisen zu sehen schreibe einfach soetwas wie ('Darf ich die Speisekarte anschauen?)"
                    "\nBezahlen: Wenn du deine Bestellung beenden möchtest kannst du dies mit beispielsweise 'Ich möchte bezahlen' tun."
                    "\nWarenkorb bearbeiten: Wenn du schreibst das du den Warenkorb bearbeiten möchtest, werden dir alle Gerichte auf deinem Warenkorb nummeriert aufgelistet."
                    "\n    Möchtest du eins der Gerichte entfernen musst du 3 Bestandteile angeben."
                    "\n        1. Die Nummer, die vor dem Gericht steht. Der Punkt nach der Nummer ist sehr wichtig (bspw. '5.')."
                    "\n        2. Das Schlüsselwort 'löschen'"
                    "\n        3. Die Anzahl, wieviel vom jeweiligen Artikel entfernt werden soll."
                    "\n         Bsp.: 'Ich möchte gerne 5 mal Nummer 3. löschen'"]
    }],

    "checkout": [{
        "name": "checkout_default",
        "checked": False,
        "multiple": True,
        "phrases": ["Deine Bestellung:\n_cart\n\n_rabatt-berechnen\n\nMöchtest du die Bestellung beenden?"]
    }, {
        "name": "adresse_q",
        "checked": False,
        "multiple": True,
        "phrases": ["Sehr schön. Dann verrat mir doch bitte noch deine Adresse, damit wir dorthin liefern können. Unsere Pizzeria befindet sich an der _pizzeria-adress"]
    }, {
        "name": "checkout_summary",
        "checked": False,
        "multiple": True,
        "phrases": ["Okay _user-name. Wir liefern in 30 Minuten deine Bestellung an die Adresse '_user-adress'. \nDeine Bestellung:\n_cart\n\nDer Gesamtpreis beträgt Nach Rabatten _gesamt-price-after-sale, bis gleich.\nMöchtest du Trinkgeld geben? Wenn ja schreib doch den Prozentsatz, dann kann ich dir die Summe berechnen"]
    }, {
        "name": "checkout_final",
        "checked": False,
        "multiple": True,
        "phrases": ["Vielen Dank für deine Bestellung _user-name. Dein Gesamtpreis nach Trinkgeld beträgt _total-after-tip€, und wir sind in ca. 30 Minuten da. Bis nächstes mal!"]
    }],

    "end_cancel": [{
        "name": "end",
        "checked": False,
        "multiple": False,
        "phrases": [
            "Schade. Ich wünsche dir noch einen schönen Tag _user-name, vielleicht möchtest du ja doch nochmal in Zukunft hier bestellen."]
    }]
}

for a in menu:
    for b in menu[a]:
        valid_order.append(b)


# Funktionen für das verarbeiten des inputs basierend auf dem Status der Unterhaltung
def process_input(input):
    global dialogue_state

    if dialogue_state == "greeting":
        process_input_greeting(input)
    elif dialogue_state == "ordering":
        process_input_ordering(input)
    elif dialogue_state == "checkout":
        process_input_checkout(input)


def process_input_greeting(input):
    global dialogue_state, user_name, last_output, allowed_outputs, running
    allowed_outputs = []

    if input.lower() in ['help', 'hilfe', 'info']:
        allowed_outputs.append("help")

    if last_output == "welcome":  # Gerade eben nach Name gefragt
        user_name = input
        allowed_outputs.append("order_general_q")
    elif last_output == "order_general_q":
        if did_accept(input):
            dialogue_state = "ordering"
            allowed_outputs.append("ordering_innit")
        elif did_decline(input):
            dialogue_state = "end_cancel"
            allowed_outputs.append("end")
            running = False



def process_input_ordering(input):
    global dialogue_state, user_name, last_output, allowed_outputs, edit_cart_response

    edit_cart_response = ""
    allowed_outputs = []

    if input.lower() in ['help', 'hilfe', 'info']:
        allowed_outputs.append("help")

    if last_output in ["ordering_innit", "ordering_default", "show_menu", "new_order", "show_cart", "help"]:
        if analyse_order_and_add_to_cart(input):
            allowed_outputs.append("new_order")

    if last_output == "ordering_innit":
        if "speisekarte" in input.lower():
            allowed_outputs.append("show_menu")


    elif last_output in ["ordering_default", "new_order", "show_cart", 'warenkorb_bearbeiten_innit',
                         'warenkorb_bearbeiten', "help"]:
        if last_output == "show_cart" and did_accept(input):
            allowed_outputs.append("warenkorb_bearbeiten_innit")

        if "bezahl" in input.lower():
            dialogue_state = "checkout"
            allowed_outputs.append("checkout_default")
        elif "speisekarte" in input.lower():
            allowed_outputs.append("show_menu")
        elif "bearbeit" in input.lower() or "edit" in input.lower():
            allowed_outputs.append("warenkorb_bearbeiten_innit")
        elif "warenkorb" in input.lower():
            allowed_outputs.append("show_cart")

        if last_output == "warenkorb_bearbeiten_innit" or last_output == "warenkorb_bearbeiten":
            if input.lower() in ["abbrechen", "abbruch", "stop"] or "bestell" in input.lower():
                allowed_outputs.append("ordering_default")
            else:
                edit_cart_response = analyse_edit_cart(input)
                allowed_outputs.append("warenkorb_bearbeiten")


def process_input_checkout(input):
    global dialogue_state, user_name, last_output, allowed_outputs, running, adress, total_after_tip
    allowed_outputs = []
    total_after_tip = 0

    if input.lower() in ['help', 'hilfe', 'info']:
        allowed_outputs.append("help")

    if last_output == 'checkout_default':
        if did_accept(input):
            allowed_outputs.append('adresse_q')
        elif did_decline(input):
            dialogue_state = 'ordering'
            allowed_outputs.append('ordering_default')
    elif last_output == 'adresse_q':
        allowed_outputs.append('checkout_summary')
        adress = input
    elif last_output == 'checkout_summary':
        allowed_outputs.append('checkout_final')
        total_after_tip = analyse_and_calc_after_tip(input)
        running = False



# Funktionen für Ausgaben des Bots
def find_output(current_state):
    """Ausgabe herausfinden"""
    global outputs, allowed_outputs, last_output, user_name, running

    for dic in outputs[current_state]:
        if dic["checked"] == False or dic["multiple"] == True:
            if dic["name"] in allowed_outputs:
                dic["checked"] = True
                if dic["name"] not in []:
                    last_output = dic["name"]
                return random.choice(dic["phrases"])

    for state in outputs:
        if last_output in state:
            if 'default' in state[last_output]:
                return state[last_output]['default']

    return "Ich habe keine Antwort für dich, tut mir leid."


# -----------------------------------------------------------------
def show_menu(with_ingredients=False):
    """Zeigt das Menü mit Pizzen und Getränken an."""
    menu_output_string = ""

    menu_output_string += "Pizzen:"
    menu_output_string += "\n"
    for (pizza, attributes) in menu['pizzas'].items():
        menu_output_string += f"  {pizza[0].capitalize() + pizza[1:]}: {attributes['price']:.2f}€"
        menu_output_string += "\n"

    menu_output_string += ("\nGetränke:")
    for (drink, attributes) in menu['drinks'].items():
        menu_output_string += f"  {drink[0].capitalize() + drink[1:]}: {attributes['price']:.2f}€"
        menu_output_string += "\n"

    menu_output_string += ("\nBeilagen:")
    menu_output_string += "\n"
    for (drink, attributes) in menu['sides'].items():
        menu_output_string += f"  {drink[0].capitalize() + drink[1:]}: {attributes['price']:.2f}€"
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
        output = ""
        price = 0
        for (item, quantity) in cart.items():
            output += f"{quantity}x {item[0].capitalize() + item[1:]} - {get_item_price(item):.2f}€ pro Stück, {get_item_price(item) * int(quantity):.2f}€ gesamt.\n"
        price = calculate_total_cart()
        output += f"Gesamtpreis: {price:.2f}€"
        return output


def show_edit_cart():
    """Zeigt den bearbeitungsmodus des Warenkorbs an."""
    global cart, ordered_cart
    ordered_cart = []
    output = "Warenkorb:\n"
    price = 0
    i = 0
    for (item, quantity) in cart.items():
        i += 1
        ordered_cart.append((item, quantity))
        output += f"{i}. {quantity}x {item[0].capitalize() + item[1:]}\n"
    price = calculate_total_cart()
    output += f"Wenn du eine bestimmte Sache bearbeiten willst, schreibe die Nummer und einen Punkt 'bschw. 3.'. Um zu löschen schreibe zum Beispiel '5x 2. löschen'."
    return output

def show_calculate_sale():
    """Formuliert den Preis des gesamten Warenkorbs nach Rabatten"""
    global menu, cart, sales_big_order
    output = ""
    total = calculate_total_cart()
    sale = calculate_sale()
    sale_factor = sale[1]
    sale_checkpoint = sale[0]

    output = f"Der Gesamtwert deines Warenkorbs beträgt {total:.2f}€. "
    if sale_factor != 0:
        output += f"Da dies über {sale_checkpoint:.2f}€ liegt bekommmst du einen Rabatt von {sale_factor * 100:.0f}%." \
                  f"\nDein zu zahlender Gesamtpreis beträgt also {(1 - sale_factor) * total:.2f}€"
    return output



# -----------------------------------------------------------------------------------------------------
def analyse_order_and_add_to_cart(input):
    """Prüft in einem Text, ob etwas bestellt worden ist, und fügt ggf. mit add_to_cart() zum Warenkorb hinzu."""
    global valid_order, last_order, words_number_replace
    did_order = False
    input = input.replace('x', ' ')
    input = input.replace('mal', ' ')
    text_list = input.split()
    for i in range(len(text_list)):
        if text_list[i].lower() in words_number_replace:
            text_list[i] = str(words_number_replace[text_list[i]])
        if text_list[i].lower() not in valid_order:
            for j in range(len(text_list[i])):
                if text_list[i][j].isnumeric() == False:
                    text_list[i] = text_list[i][:j] + ' ' + text_list[i][j + 1:]
        text_list[i] = text_list[i].replace(' ', '')

    currindex = -1
    for index in range(len(text_list)):
        currindex += 1
        i = text_list[currindex]
        if len(i) == 0:
            del text_list[currindex]
            currindex -= 1
        elif i.lower() in valid_order:
            did_order = True

    if did_order:
        last_order = []

    for i in range(len(text_list)):
        if text_list[i].lower() in valid_order:
            did_order = True
            if text_list[max(i - 1, 0)][0].isnumeric():
                add_to_cart(text_list[i].lower(), text_list[max(i - 1, 0)])
            else:
                add_to_cart(text_list[i].lower(), 1)
    return did_order


def add_to_cart(item, quantity):
    """Fügt einen Artikel in einer bestimmten Menge zum Warenkorb hinzu."""
    global cart, last_order, menu
    quantity = int(quantity)
    if item in menu['pizzas'] or item in menu['drinks'] or item in menu['sides']:
        if item in cart:
            cart[item] += quantity
        else:
            cart[item] = quantity
        last_order.append(f"{quantity}x {item}\n")


def analyse_edit_cart(input):
    """Analysiert einen Text darauf ob der Benutzer etwas im Warenkorb bearbeiten möchte"""
    global ordered_cart, words_number_replace

    input = input.lower()
    text = input.split()
    number = 0
    ints_in_text = []
    delete = False

    i = -1
    for k in range(len(text)):
        i += 1
        word = text[i]
        if word.lower() in words_number_replace:
            text[i] = str(words_number_replace[word])
            word = str(words_number_replace[word])
        if word[-1] == ".":
            is_number = True
            for letter in word[:-1]:
                if letter.isnumeric() == False:
                    is_number = False
            if is_number:
                number = int(word.replace(".", ""))
                del text[i]
                i -= 1
            else:
                text[i] = word.replace(".", "")
        else:
            text[i] = word.replace("x", "")

    i = -1
    for k in range(len(text)):
        i += 1
        word = text[i]
        is_number = True
        if "lösch" in word:
            delete = True
        for letter in word:
            if letter.isnumeric() == False:
                is_number = False
        if is_number:
            ints_in_text.append(int(word))

    number_valid = False
    item_in_cart = ""
    if number != 0:
        if number <= len(ordered_cart):
            number_valid = True
            item_in_cart = ordered_cart[number - 1][0]

    if number == 0:
        return "Tut mir Leid, du musst noch eine Nummer zum bearbeiten eingeben. (z. B. '2. löschen.')"
    elif number_valid == False:
        return f"Tut mir Leid, dein Warenkorb ist zu klein. Die Nummer {number}. ist nicht drauf."
    elif delete:
        if len(ints_in_text) == 1:
            remove_from_cart(item_in_cart, ints_in_text[0])
            if ordered_cart[number - 1][1] < ints_in_text[0]:
                return f"Du hast {item_in_cart} nicht {ints_in_text[0]} mal im Warenkorb. {ordered_cart[number - 1][1]}x {item_in_cart} ({number}.) gelöscht."
            else:
                return f"{ints_in_text[0]}x {item_in_cart} ({number}.) gelöscht."
        elif len(ints_in_text) >= 1:
            return f"Ich weiß nicht wie häufig du die Nummer {number}. löschen möchtest. Du hast mehr als eine Zahl geschrieben, versuche noch einmal."
        else:
            remove_from_cart(item_in_cart, ordered_cart[number - 1][1])
            return f"{ordered_cart[number - 1][1]}x {item_in_cart} ({number}.) gelöscht."
    else:
        return "Du musst dazu schreiben, was du mit dem Artikel machen möchtest, versuche noch einmal."


def remove_from_cart(item, quantity):
    """Entfernt einen Artikel in einer bestimmten Menge aus dem Warenkorb."""
    global cart

    if item in cart:
        if cart[item] > quantity:
            cart[item] -= quantity
        elif cart[item] == quantity:
            del cart[item]
        else:
            del cart[item]


def analyse_and_calc_after_tip(input):
    '''Analysiert den input, ob ein Trinkgeld gegeben wurde, und gibt den gesamtpreis aus.'''

    total = calculate_sale()[-1]
    if did_decline(input): #kein tip
        return total
    input = input.replace('%', ' ')
    input = input.split()

    for word in input:
        isnumb = True
        for numb in word:
            if numb.isnumeric() == False:
                isnumb = False
        if isnumb:
            print((1 + int(word)/100) * total)
            return (1 + int(word)/100) * total

    return total


# calc
def get_item_price(item):
    """Gibt den Preis eines Artikels zurück."""
    global menu
    if item in menu['pizzas']:
        return menu['pizzas'][item]['price']
    elif item in menu['drinks']:
        return menu['drinks'][item]['price']
    elif item in menu['sides']:
        return menu['sides'][item]['price']
    return 0


def calculate_total_cart():
    """Berechnet den Gesamtpreis des Warenkorbs."""
    global menu, cart
    total = 0
    for item, quantity in cart.items():
        total += get_item_price(item) * quantity
    return total


def calculate_sale():
    """Errechnet den Preis nach sale."""
    global menu, cart, sales_big_order

    total = calculate_total_cart()
    sale_factor = 0
    sale_checkpoint = 0
    for i in sales_big_order:
        if total >= i[0]:
            sale_factor = i[1]
            sale_checkpoint = i[0]
    output = [sale_checkpoint, (sale_factor), ((1 - sale_factor) * total)]
    return output


# --------------------------
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


def capitalize_first(text):
    return text[0].capitalize() + text[1:]


def replace_vars(text):
    """Ersetzt Variablen im Text durch den entsprechenden Wert."""
    global user_name, PIZZERIA_NAME, edit_cart_response, PIZZERIA_ADRESS, adress, total_after_tip
    replace = {'_user-name': user_name,
               '_pizzeria-name': PIZZERIA_NAME,
               '_menu': str(show_menu()),
               '_cart': str(show_cart()),
               '_show-last-order': str(show_last_order()),
               '_analyse-edit-cart': edit_cart_response,
               '_edit-cart': str(show_edit_cart()),
               '_rabatt-berechnen': str(show_calculate_sale()),
               '_pizzeria-adress' : PIZZERIA_ADRESS,
               '_user-adress' : adress,
               '_gesamt-price-after-sale' : str(calculate_sale()[-1]),
               '_total-after-tip' : str(total_after_tip)
               }

    for condition in replace:
        text = text.replace(condition, replace[condition])

    return text
