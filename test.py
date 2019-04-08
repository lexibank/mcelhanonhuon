
def test_valid(cldf_dataset, cldf_logger):
    assert cldf_dataset.validate(log=cldf_logger)


def test_languages(cldf_dataset, cldf_logger):
    assert len(list(cldf_dataset['LanguageTable'])) == 14


def test_sources(cldf_dataset, cldf_logger):
    assert len(cldf_dataset.sources) == 1


def test_parameters(cldf_dataset, cldf_logger):
    assert len(list(cldf_dataset['ParameterTable'])) == 140


def test_forms(cldf_dataset, cldf_logger):
    assert len(list(cldf_dataset['FormTable'])) == 1960
    # 90829	komba	sun	mirâsiŋ	sun	
    assert len([
        f for f in cldf_dataset['FormTable'] if f['Form'] == 'mirâsiŋ'
    ]) == 1


def test_cognates(cldf_dataset, cldf_logger):
    cogsets = {c['Cognateset_ID'] for c in cldf_dataset['CognateTable']}
    assert len(cogsets) == 949

