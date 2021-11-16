def getProgram(program: str):
    program = program.upper()
    if program in ['S1', 'S2', 'S3', 'D3', 'SP', 'SP1', 'SP2', 'SUBSPESIALIS', 'SPESIALIS 2']:
        PROGRAM = {
            'S1': 'Sarjana',
            'S2': 'Magister',
            'S3': 'Doktor',
            'D3': 'Diploma Tiga',
            'SP': 'Spesialis 1',
            'SP1': 'Spesialis 1',
            'SP2': 'Spesialis 2 (Subspesialis)',
            'SUBSPESIALIS': 'Spesialis 2 (Subspesialis)',
            'SPESIALIS 2': 'Spesialis 2 (Subspesialis)'
        }
        return PROGRAM.get(program, None)
    program = program.lower()
    if program in ['sarjana', 'magister', 'doktor', 'diploma tiga', 'spesialis 1', 'spesialis 2 (subspesialis)']:
        return program.capitalize()
    pass

print(getProgram('Subspesialis'))