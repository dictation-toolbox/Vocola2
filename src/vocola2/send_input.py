### 
### Module Keys
###
# make it the default, instead of natlink.playString etc.


from vocola2.extensions import ExtendedSendDragonKeys
from vocola2.extensions import SendInput

# Vocola procedure: Keys.SendInput
def send_input(specification):
    SendInput.send_input(
        ExtendedSendDragonKeys.senddragonkeys_to_events(specification))
