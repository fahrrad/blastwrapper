import os
from uuid import UUID
import uuid
import settings

__author__ = 'wardcoessens'


BLAST_OPTIONS="-db={db} -out={outfile} -outfmt={format} -query={fasta_file}"

class BlastTypes:
    PROT=1
    NUCL=2


class InvalidSubsetException(BaseException):
    pass


class BlastRun:
    def __init__(self, sequence, subset, blast_type=BlastTypes.NUCL):
        """
        :param sequence: The sequence to blast
        :param subset: the subset to blast against

        """
        self.sequence = sequence
        self.db = subset
        self.blast_type = blast_type

    def run(self):
        """
        Runs the blast
        :return: a list of alignments
        """

        blast_db = settings.BLAST_DB + self.db + '.nhr'

        if not os.path.exists(settings.BLAST_DB + '/' + self.db + '.nhr'):
            print("not a valid blastdb %s, expected to find %s" % (self.db, blast_db))
            raise InvalidSubsetException

        if self.blast_type == BlastTypes.NUCL:
            return self.__run_nucl_blast()
        elif self.blast_type == BlastTypes.PROT:
            return self.__run_prot_blast()

    def __run_prot_blast(self):
        pass

    def __run_nucl_blast(self):
        input_file = settings.TEMP_DIR + '/' + str(uuid.uuid4()) + '.fasta'
        output_file = settings.TEMP_DIR + '/' + str(uuid.uuid4()) + '.xml'

        with open(input_file, 'wt') as fasta_file:
            fasta_file.write('> input sequence \n')
            fasta_file.write(self.sequence)

        cmd = "blastn"
        options = {'db': self.db, 'outfile': output_file, 'format': 5,
                   'fasta_file': input_file}

        os.popen(cmd + ' ' + BLAST_OPTIONS.format(**options)).read()
        result = open(output_file, 'rt').read()

        os.remove(input_file)
        os.remove(output_file)

        return result



run = BlastRun('TGTAGACGCGTTTTCATCGTTAGCAGCCAATGGAACT', 'sample_db')
print(run.run())