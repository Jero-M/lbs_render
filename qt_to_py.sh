SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"

cd $SCRIPT_DIR
pyuic4 control_panel_qt_designer.ui -o control_panel_qt_ui.py
