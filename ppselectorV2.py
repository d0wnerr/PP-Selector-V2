import subprocess
import re

print("===PP SELECTOR V2===")

# current pp fetcher
getActivePP = subprocess.run(["powercfg", "/getactivescheme"], capture_output=True, text=True) # runs cmd for retreiving current pp
output = getActivePP.stdout
activePPut = output.strip()
match = re.search(r'\((.*?)\)', output) # extracts pp from cmd output
if match:
    activePP = match.group(1)
print()
print(f"Current PP: {activePP}")

# pp fetcher cmd
existingPP = subprocess.run(["powercfg", "/list"], capture_output=True, text=True) # gets pps using powercfg /list
output = existingPP.stdout

# pp analyzer
pattern = r"Power Scheme GUID: ([a-f0-9\-]+)\s+\((.*?)\)" # the method used to extract pp guids and names from cmd output
guids = re.findall(pattern, output)

# pp prompter
def ppPrompt():
    global selectedPP
    print()
    for i, (_, name) in enumerate(guids, start=1): 
        print(f"{i} - {name}")
    print("N - New Power Plan")
    print()
    selectedPP = input("Power mode: ")
    ppValidation()

# validates the selected pp
def ppValidation():
    global selectedPP
    if selectedPP == "":
        print()
    elif selectedPP == "N" or "n":
        ppNewPP()
    else:    
        try:
            selectedIndex = int(selectedPP) - 1
            if 0 <= selectedIndex < len(guids):
                selectedPP = guids[selectedIndex][0]
                ppExecutor()
            else:
                print()
                print("Invalid option.")
                ppPrompt()
        except ValueError:
            print()
            print("Invalid option.")
            ppPrompt()

# the pp executor
def ppExecutor():
    subprocess.run(["cmd", "/c", f"powercfg /S {selectedPP}"])
    print()
    print("Success")
    print()
    print(f"Current PP: {dict(guids).get(selectedPP)}")
    input()

def ppNewPP():
    print()
    print("Opening Power Plan Menu...")
    subprocess.run(["powercfg.cpl"], shell=True, )
    print("Success")
    input()

ppPrompt()