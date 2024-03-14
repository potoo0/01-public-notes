#!/usr/bin/env bash
set -euo pipefail

# remove pkgs installed by snap
echo '>>> remove pkgs installed by snap...'

MAX_TRIES=30
for try in $(seq 1 $MAX_TRIES); do
  INSTALLED_SNAPS=$(snap list 2> /dev/null | grep -c  ^Name || true)
  if (( $INSTALLED_SNAPS == 0 )); then
    echo "all snaps removed"
    break
  fi
  echo "Attempt $try of $MAX_TRIES to remove $INSTALLED_SNAPS snaps."

  # we ignore error during uninstall as we are retrying in the loop
  snap list 2> /dev/null | grep -v ^Name |  awk '{ print $1 }'  | xargs -r -n1  snap remove || true
done

# stop process
echo '>>> systemctl disable --now...'
systemctl disable --now snapd.socket || true
systemctl disable --now snapd || true

# remove snap system package
echo '>>> remove snap system package...'
apt autoremove --purge snapd gnome-software-plugin-snap
# prohibit snap https://manpages.ubuntu.com/manpages/focal/man5/apt_preferences.5.html
cat > /etc/apt/preferences.d/99-prohibit-snapd << EOL
Package: snapd
Pin: release a=*
Pin-Priority: -10
EOL

# remove snap files
echo '>>> remove snap files...'
rm -rf ~/snap
rm -rf /snap
rm -rf /var/snap
rm -rf /var/lib/snapd
rm -rf /var/cache/snapd
