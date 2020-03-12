from pathlib import Path
from clldutils.misc import slug
from pylexibank import Dataset as BaseDataset
from pylexibank import FormSpec


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

    form_spec = FormSpec(missing_data=("-", ""))

    def cmd_makecldf(self, args):
        """
        Convert the raw data to a CLDF dataset.
        """
        args.writer.add_sources()
        languages = args.writer.add_languages(
            lookup_factory=lambda l: l[
                "ID"
            ].lower()  # lower case in raw data, so title case
        )
        concepts = args.writer.add_concepts(
            id_factory=lambda c: c.id.split("-")[-1] + "_" + slug(c.english),
            lookup_factory="Name",
        )

        cog = CognateRenumber()

        for row in self.raw_dir.read_csv(
            "mcelhanon-1967.tsv", dicts=True, delimiter="\t"
        ):
            lex = args.writer.add_forms_from_value(
                Local_ID=row["ID"],
                Language_ID=languages[row["Language"]],
                Parameter_ID=concepts[row["Word"]],
                Value=row["Gloss"],
                Comment=row["Annotation"],
                Source="McElhanon1967",
            )

            cognates = row["Cognacy"].split(",")

            if len(cognates) == 0:
                # singleton
                cog_id = cog.get_cogid()
            elif len(cognates) == 1:
                cog_id = cog.get_cogid(cognates[0])
            else:
                raise ValueError("Multiple cognates per lexeme are not handled")

            assert len(lex) == 1, "Should only have one lexeme"
            args.writer.add_cognate(
                lexeme=lex[0], Cognateset_ID=cog_id, Source="McElhanon1967"
            )
