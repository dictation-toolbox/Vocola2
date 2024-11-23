### 
### Module Keys
### 
from dtactions.vocola_sendkeys import ExtendedSendDragonKeys, SendInput
# import ExtendedSendDragonKeys
# import SendInput



# Vocola procedure: Keys.SendInput
def send_input(specification):
    # print(f'vocola send_input: {specification}')
    SendInput.send_input(
        ExtendedSendDragonKeys.senddragonkeys_to_events(specification))

if __name__ == "__main__":
    send_input("hello world")
    