from globalhotkeys import GlobalHotKeys


@GlobalHotKeys.register(GlobalHotKeys.VK_F1, GlobalHotKeys.MOD_SHIFT)
def hello_world():
    print("Hello World!")


@GlobalHotKeys.register(GlobalHotKeys.VK_F2)
def hello_world_2():
    print("Hello World again?")


# Q and ctrl will stop message loop
GlobalHotKeys.register(GlobalHotKeys.VK_Q, 0, False)
GlobalHotKeys.register(GlobalHotKeys.VK_C, GlobalHotKeys.MOD_CTRL, False)

# start main loop
GlobalHotKeys.listen()