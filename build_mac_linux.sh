#!/usr/bin/env bash

cd "$(dirname "$0")" || exit 1

fail() { echo; echo "Build failed: $1"; exit 1; }

OS="$(uname -s)"
ARCH="$(uname -m)"
case "$OS" in
  Darwin) PLATFORM="macos-$ARCH" ;;
  Linux)  PLATFORM="linux-$ARCH" ;;
  *)      fail "unsupported system '$OS' (use build_exe.bat on Windows)" ;;
esac
echo "Building for: $PLATFORM"

PY=""
for c in python3 python; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys; sys.exit(0 if sys.version_info[0]==3 else 1)' 2>/dev/null; then
    PY="$c"; break
  fi
done
[ -n "$PY" ] || fail "Python 3 neededuh. Install it first (macOS: python.org installer or 'brew install python'; Debian/Ubuntu: 'sudo apt install python3')."

if ! "$PY" -c 'import tkinter' 2>/dev/null; then
  if [ "$OS" = "Darwin" ]; then
    fail "this Python no has tkinter. Use the installer from python.org, or with Homebrew run: brew install python-tk"
  else
    fail "this Python no has tkinter. Install it: Debian/Ubuntu 'sudo apt install python3-tk', Fedora 'sudo dnf install python3-tkinter', Arch 'sudo pacman -S tk'"
  fi
fi

if [ ! -d .venv-build ]; then
  "$PY" -m venv .venv-build || fail "couldn't create a virtual environment (Debian/Ubuntu: 'sudo apt install python3-venv')."
fi
. .venv-build/bin/activate || fail "couldn't activate the virtual environment."
python -m pip install --upgrade pip pyinstaller || fail "pip install failed (are you online?)."

rm -rf build dist

if [ "$OS" = "Darwin" ]; then
  python -m PyInstaller --windowed --name MojibDehasher mojib_dehasher.py || fail "PyInstaller error (see above)."
  [ -d "dist/MojibDehasher.app" ] || fail "MojibDehasher.app was not created."
  ditto -c -k --keepParent dist/MojibDehasher.app "dist/MojibDehasher-$PLATFORM.zip"
  echo
  echo "Done."
  echo "  App: $(pwd)/dist/MojibDehasher.app"
  echo "  Zip: $(pwd)/dist/MojibDehasher-$PLATFORM.zip"
  echo
  echo "app is unsigned. first time you open it: right-click > Open > Open."
  echo "if its from the internet and no run, run:"
  echo "  xattr -dr com.apple.quarantine MojibDehasher.app"
else
  python -m PyInstaller --onefile --name MojibDehasher mojib_dehasher.py || fail "PyInstaller error (see above)."
  [ -f "dist/MojibDehasher" ] || fail "dist/MojibDehasher was not created."
  mv dist/MojibDehasher "dist/MojibDehasher-$PLATFORM"
  chmod +x "dist/MojibDehasher-$PLATFORM"
  echo
  echo "done! Your dehashifier: $(pwd)/dist/MojibDehasher-$PLATFORM"
fi
