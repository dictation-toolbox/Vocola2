### 
### Module Keys
###
# make it the default, instead of natlink.playString etc.


from dtactions.vocola_sendkeys import ExtendedSendDragonKeys
from dtactions.vocola_sendkeys import SendInput
# from vocola2.extensions import ExtendedSendDragonKeys
# from vocola2.extensions import SendInput

# Vocola procedure: Keys.SendInput
def send_input(specification):
    SendInput.send_input(
        ExtendedSendDragonKeys.senddragonkeys_to_events(specification))

sendkeys = send_input

if __name__ == "__main__":
    send_input("hello world")
    