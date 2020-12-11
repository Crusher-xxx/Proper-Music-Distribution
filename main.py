if __name__ == '__main__':
    import ListenerStorage

    listeners = ListenerStorage.ListenerStorage()
    listeners.load()

    for listener in listeners:
        print(listener.get_report())

    listeners[2].activate_subscription()
    print(listeners[2].get_report())