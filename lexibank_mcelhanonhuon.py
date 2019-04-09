from clldutils.path import Path
from pylexibank.dataset import Dataset as BaseDataset


class CognateRenumber(object):
    def __init__(self):
        self.singleton_id = 0
        self.cognates = []
    
    def get_cogid(self, cogid):
        if not cogid:
            cogid = "singleton-%d" % self.singleton_id
            self.singleton_id += 1
        
        if cogid not in self.cognates:
            self.cognates.append(cogid)
        # print("cognate - %s => %s" % (cogid, self.cognates.index(cogid)))
        return self.cognates.index(cogid)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "mcelhanonhuon"

    def cmd_download(self, **kw):
        # data are already in raw/ --> NOOP
        pass

    def iter_raw_lexemes(self):
        for row in self.raw.read_tsv("mcelhanon-1967.tsv", dicts=True):
            yield self.clean_form(row, row['Gloss'])

    def cmd_install(self, **kw):
        """
        Convert the raw data to a CLDF dataset.
        """
        with self.cldf as ds:
            ds.add_sources()
            ds.add_languages()
            
            concepts = {}
            for c in self.conceptlist.concepts.values():
                ds.add_concept(
                    ID=c.concepticon_id,
                    Name=c.english,
                    Concepticon_ID=c.concepticon_id,
                    Concepticon_Gloss=c.concepticon_gloss
                )
                concepts[c.english] = c.concepticon_id
            
            cog = CognateRenumber()
            for row in self.raw.read_tsv("mcelhanon-1967.tsv", dicts=True):
                for o in ds.add_lexemes(
                    Local_ID=row['ID'],
                    Language_ID=row['Language'],
                    Parameter_ID=concepts[row['Word']],
                    Value=row['Gloss'],
                    Form=self.clean_form(row, row['Gloss']),
                    Source='McElhanon1967',
                    Comment=row['Annotation']
                ):
                    cognates = row['Cognacy'].split(",")
                    if len(cognates) == 0:
                        # singleton
                        c = ds.add_cognate(lexeme=o, Cognateset_ID=cog.get_cogid())
                    elif len(cognates) == 1:
                        c = ds.add_cognate(lexeme=o, Cognateset_ID=cog.get_cogid(cognates[0]))
                    else:
                        # check that we haven't left any cognates that are NOT from
                        # McElhanon in the raw data
                        raise ValueError("Multiple cognates per lexeme are not handled")
                    o['Cognacy'] = c['Cognateset_ID']
