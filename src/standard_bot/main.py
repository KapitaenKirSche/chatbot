import logic as bot


def main():
    """Hauptfunktion zum Ausführen des Chatbots."""
    return_text = ""

    if bot.user_input != "_init":
        bot.process_input(bot.user_input)

    if bot.dialogue_state == "greeting":
        return_text = bot.greetings()

    print(bot.replace_vars(return_text))
    bot.user_input = input()


while bot.running:
    main()