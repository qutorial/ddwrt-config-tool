return 0

if [[ -d venv ]];
then
  . venv/bin/activate
else
  echo "Could not activate the venv"
  exit 20
fi



