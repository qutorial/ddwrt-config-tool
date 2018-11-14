from nvramio import writeSettingsToFile
settings = {'foo' : 'bar'}
writeSettingsToFile(settings, 'settings.enc', "123")

