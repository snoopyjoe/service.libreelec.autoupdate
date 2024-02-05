import xbmc, xbmcaddon, xbmcgui, json, urllib.request, subprocess

ADDON = xbmcaddon.Addon()
if __name__ == '__main__':
    Platform = ADDON.getSetting(id='platform')
    Enable = ADDON.getSetting(id='enable')


#Variables
dialog = xbmcgui.Dialog()
jdata = json.load(urllib.request.urlopen('https://releases.libreelec.tv/releases.json'))
Platform = int(Platform) #Convert Addon setting to integer


if Enable == "false":
    dialog.textviewer("LibreELEC Auto Update Service is Disabled","Please Enable Service in addon settings")
    ADDON.openSettings()
    exit()

#Determine platform path base on input from settings
if (Platform == 0):
#Platform Release Availabilty Check
    if '2' in jdata['LibreELEC-11.0']['project']['Generic-legacy.x86_64']['releases']:
        jpath = jdata['LibreELEC-11.0']['project']['Generic-legacy.x86_64']['releases']['2']['image']['name']
    elif '1' in jdata['LibreELEC-11.0']['project']['Generic-legacy.x86_64']['releases']:
        jpath = jdata['LibreELEC-11.0']['project']['Generic-legacy.x86_64']['releases']['1']['image']['name']
    else:
        jpath = jdata['LibreELEC-11.0']['project']['Generic-legacy.x86_64']['releases']['0']['image']['name']

if (Platform == 1):
#Platform Release Availabilty Check
    if '2' in jdata['LibreELEC-11.0']['project']['Generic.x86_64']['releases']:
        jpath = jdata['LibreELEC-11.0']['project']['Generic.x86_64']['releases']['2']['image']['name']
    elif '1' in jdata['LibreELEC-11.0']['project']['Generic.x86_64']['releases']:
        jpath = jdata['LibreELEC-11.0']['project']['Generic.x86_64']['releases']['1']['image']['name']
    else:
        jpath = jdata['LibreELEC-11.0']['project']['Generic.x86_64']['releases']['0']['image']['name']

#Compare Installed OS verions to Latest online version
xbmc.getInfoLabel('System.OSVersionInfo')
xbmc.sleep(100)
os_version = xbmc.getInfoLabel('System.OSVersionInfo')
replace_front_os = os_version.replace("LibreELEC (official): ", " ")
current_os = replace_front_os.replace("(kernel: Linux 6.1.74)", " ")

latest_ver = jpath
replace_front_latest = latest_ver.replace("LibreELEC-Generic-legacy.x86_64-", " ")
current_online = replace_front_latest.replace(".img.gz", " ")

#Used to run wget
def runcmd(cmd, verbose = False, *args, **kwargs):

    process = subprocess.Popen(
        cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True,
        shell = True
    )
    std_out, std_err = process.communicate()
    if verbose:
        print(std_out.strip(), std_err)
    pass

if current_os < current_online:
    xbmc.sleep(15000)
    dialog.notification("New Update Available", "Downloading..." + current_online, xbmcgui.NOTIFICATION_INFO, 10000)
    URL = ("https://releases.libreelec.tv/{}".format(latest_ver))
    runcmd("wget -P /storage/.update/ {}".format(URL), verbose = True)

else:
    xbmc.sleep(15000)
    dialog.notification("No updates available", "Current version:" + current_os, xbmcgui.NOTIFICATION_INFO, 10000)
#xbmc.log("CurrentOS" + current_os, level=xbmc.LOGINFO)
#xbmc.log("OnlineOS" + current_online, level=xbmc.LOGINFO)
