import logic as bot


def main():
    """Hauptfunktion zum Ausführen des Chatbots."""
    return_text = ""

    if bot.user_input != "_init":
        bot.process_input(bot.user_input)

    return_text = bot.find_output(bot.dialogue_state)

    print("\n")
    print(bot.replace_vars(return_text))
    if bot.running:
        print("\n")
        bot.user_input = input(" >> ")


while bot.running:
    main()