import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()

    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its mac adress")
    parser.add_option("-m", "--mac", dest="new_mac", help="New Mac Address ")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface or use --help for more info")
    elif not options.new_mac:
        parser.error("[-] Please specify a mac adress or use --help for more info")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing Mac Adress For " + interface + " to " + new_mac)

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result_bytes = subprocess.check_output(["ifconfig", interface])
    ifconfig_result = str(ifconfig_result_bytes, 'utf-8')

    captured_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if captured_mac:
        return captured_mac.group(0)
    else:
        print("[-] Could Not Read Mac Address")


options = get_arguments()
current_mac = get_current_mac(options.interface)
print("Current Mac = " + str(current_mac))

change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)


def mac_checking():
    if current_mac == options.new_mac:
        print("[+]Mac Changed Successfully to " + str(current_mac))
    else:
        print("Mac Address did not change")


mac_checking()
