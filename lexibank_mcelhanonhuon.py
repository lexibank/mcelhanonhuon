from clldutils.path import Path
from pylexibank.dataset import Dataset as BaseDataset


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "mcelhanonhuon"

    def cmd_download(self, **kw):
        # data are already in raw/ --> NOOP
        pass

    def cmd_install(self, **kw):
        """
        Convert the raw data to a CLDF dataset.
        """
        with self.cldf as ds:
            ds.add_sources()
            ds.add_languages()
            ds.add_concepts()
            # ds.add_lexemes(...)
            # lexeme.Word == concept.English
