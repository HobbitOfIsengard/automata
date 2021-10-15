def handle(automata, result):
    """
    This is a simple handler
    :param automata: the automata which yielded the result
    :type automata: :class:`Automata`
    :param result: the result of the automata
    :type result: bool
    """
    print(result)
    if not result:
        automata.switch("ask m: try again: f: handle")
