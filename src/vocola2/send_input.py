### 
### Module Keys
###
# make it the default, instead of natlink.playString etc.


from dtactions.vocola_sendkeys import ExtendedSendDragonKeys
from dtactions.vocola_sendkeys import SendInput

# Vocola procedure: Keys.SendInput
def send_input(specification):
    SendInput.send_input(
        ExtendedSendDragonKeys.senddragonkeys_to_events(specification))


if __name__ == "__main__":
    send_input("hello world")
    