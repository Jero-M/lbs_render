SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"

cd $SCRIPT_DIR
pyuic4 ifd_tool_qt.ui -o qt_ui.py
