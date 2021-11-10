def getFakultas(fakultas):
    fakultas = fakultas.lower()
    fakultas = fakultas.lstrip('fakultas').lstrip()

    if fakultas in ['hukum', 'kedokteran', 'teknik', 'pertanian', 'ekonomi']:
        return fakultas.capitalize()
    elif fakultas[0] == 'f':
        FAKULTAS = {
        'fh': 'Hukum',
        'fk': 'Kedokteran',
        'ft': 'Teknik',
        'fp': 'Pertanian',
        'fe': 'Ekonomi'
        }
        return FAKULTAS.get(fakultas, None)
    else:
        pass

print(getFakultas('fakultas teknik'))