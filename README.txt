To install this app:
  checkout it in a directory
  configure your app editing config.ini
  do "paster setup-app config.ini"
  paster --serve --reload config.ini

To demonize this app, you can use this kind of line
paster serve --daemon --pid-file /var/run/paster/yubico.pid --log-file /var/log/paster/yubico.log --user=nginx --group=nginx prod.ini

And to stop it:
paster serve --stop-daemon --pid-file /var/run/paster/yubico.pid
