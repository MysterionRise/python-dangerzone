import time

from bingo_elastic.elastic import elastic_repository_molecule
from bingo_elastic.model.record import IndigoRecordMolecule
from indigo import Indigo


def push(data_):
    indigo = Indigo()
    compound = indigo.loadMolecule(data_)
    indigo_record = IndigoRecordMolecule(indigo_object=compound)

    elasticRepository = elastic_repository_molecule()
    elasticRepository.index_record(record=indigo_record)


def search(data_):
    indigo = Indigo()
    compound = indigo.loadMolecule(data_)
    indigo_record = IndigoRecordMolecule(indigo_object=compound)

    elasticRepository = elastic_repository_molecule()
    return elasticRepository.filter(exact=indigo_record)


def delete():
    elasticRepository = elastic_repository_molecule()
    elasticRepository.delete_all_records()


if __name__ == "__main__":
    delete()
    time.sleep(5)

    data = "C"
    push(data)

    data = "C1CCCCC1"
    push(data)

    data = "C1=CC=CC=C1"
    push(data)

    data = "N"
    push(data)

    time.sleep(5)

    result = search("C1CCCCC1")
    for i in result:
        print(i)
    assert len(list(result)) == 1

    expectedResult = {"3": "C1CCCCC1"}
    assert result == expectedResult
