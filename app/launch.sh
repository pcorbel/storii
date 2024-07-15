#!/bin/sh

echo -ne "\n\n"
echo --------------------------------------------------------------------
echo ":: PYTHON APP LAUNCH"
echo --------------------------------------------------------------------

AppDir="/mnt/SDCARD/App/Storii"
AppExecutable="main.py"
Arguments=""
KillAudioserver=0
PerformanceMode=0

echo --------------------------------------------------------------------
echo ":: APPLYING ADDITIONNAL CONFIGURATION"
echo --------------------------------------------------------------------

if [ "$KillAudioserver" = "1" ]; then . /mnt/SDCARD/.tmp_update/script/stop_audioserver.sh; fi
if [ "$PerformanceMode" = "1" ]; then echo performance > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor; fi

ParasytePath="/mnt/SDCARD/.tmp_update/lib/parasyte"
export PYTHONPATH=$ParasytePath/python2.7:$ParasytePath/python2.7/site-packages:$ParasytePath/python2.7/lib-dynload:$AppDir/res/site-packages
export PYTHONHOME=$ParasytePath/python2.7:$ParasytePath/python2.7/site-packages:$ParasytePath/python2.7/lib-dynload:$AppDir/res/site-packages
export LD_LIBRARY_PATH=$ParasytePath:$ParasytePath/python2.7/:$ParasytePath/python2.7/lib-dynload:$LD_LIBRARY_PATH
export STORIIES_PATH="/mnt/SDCARD/Media/Storiies"

mkdir -p "$STORIIES_PATH"
touch /tmp/disable_menu_button

echo --------------------------------------------------------------------
echo ":: RUNNING THE APP"
echo --------------------------------------------------------------------

cd "$AppDir"
HOME="$AppDir"

echo running "$AppDir/$AppExecutable" ...

eval echo -ne "Command line : \\\n\"$ParasytePath/python2\" \"$AppExecutable\" $Arguments \\\n\\\n\\\n"
eval /mnt/SDCARD/.tmp_update/bin/parasyte/python2 \"$AppExecutable\" $Arguments > /mnt/SDCARD/.tmp_update/logs/storii.log 2>&1
STATUS=$?

echo --------------------------------------------------------------------
echo ":: POST RUNNING TASKS"
echo --------------------------------------------------------------------

unset LD_PRELOAD
rm -f /tmp/disable_menu_button

echo -ne "\n\n"

if [ ${STATUS} -eq 128 ]; then
   /mnt/SDCARD/.tmp_update/bin/shutdown
fi
