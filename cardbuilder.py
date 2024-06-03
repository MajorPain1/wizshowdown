import PySimpleGUI as sg
import json

sg.theme("DarkBlue17")

layout = [
    [sg.Text('Quick Card Builder')],
    [sg.Text('Name'), sg.InputText(key='name')],
    [sg.Text("ObjectName"), sg.InputText(key='objectName')],
    [sg.Text("School"), sg.OptionMenu(['Fire', 'Ice', 'Storm', 'Myth', 'Life', 'Death', 'Balance', 'Shadow', 'Star', 'Sun', 'Moon'], key='school')],
    [sg.Text("Accuracy"), sg.OptionMenu(['100%', 'Regular', 'Lore'], key='accuracy')],
    [sg.Text("Rank"), sg.Input(key='Rank')],
    [sg.Text("Card Type"), sg.OptionMenu(['Damage', 'Heal','Ward','Charm','Drain','AOE','Aura','Global','Enchant'], default_value='Damage', key='cardType')],
    [sg.Text("Is Treasure Card"), sg.OptionMenu(['True', 'False'], default_value='False', key='istc')],
    [sg.Text("No Reshuffle"), sg.OptionMenu(['True', 'False'], default_value='False',key='noreshuf')],
    [sg.Text("Discardable"), sg.OptionMenu(['True', 'False'], default_value='True',key='discardable')],
    [sg.Text("Trainable"), sg.OptionMenu(['True', 'False'], default_value='True',key='trainable')],
    [sg.Text("Copy Limit"), sg.Input(key='copyLimit', default_text=6)],
    [sg.Text("Level Requirement"), sg.Input(key='levelreq', default_text=0)],
    [sg.Submit(), sg.Cancel(), sg.Button("Open")]
]


def main():
    window = sg.Window('Card Builder', layout)
    event, values = window.read()
    print(event, values)

    if event == 'Submit':
        if values['istc'] == 'True':
            filename = f"cards/{values['school']}/tc/{values['objectName']}.json"
        else:
            filename = f"cards/{values['school']}/{values['objectName']}.json"

        with open(filename, 'w') as outfile:
            json.dump(values, outfile)


if __name__ == "__main__":
    main()

