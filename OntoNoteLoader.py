# reproduction/seqence_labelling/ner/data/OntoNoteLoader.py

from fastNLP.core.vocabulary import VocabularyOption
from base_loader import DataSetLoader, DataInfo
# from fastNLP.io.dataset_loader import DataSetLoader
from typing import Union, Dict
from fastNLP import DataSet
from fastNLP import Vocabulary
from fastNLP import Const
from reproduction.utils import check_dataloader_paths

# from fastNLP.io.dataset_loader import ConllLoader
# from dataset_loader import ConllLoader
from fastNLP.io.loader.conll import ConllLoader

# from reproduction.sequence_labelling.ner.data.utils import iob2bioes, iob2
from fastNLP.io.pipe.utils import iob2bioes, iob2
import os, sys

class OntoNoteNERDataLoader(DataSetLoader):
    """
    用于读取处理为Conll格式后的OntoNote数据。将OntoNote数据处理为conll格式的过程可以参考https://github.com/yhcc/OntoNotes-5.0-NER。
    """
    def __init__(self, encoding_type:str='bio'):
        assert encoding_type in ('bioes', 'bio')
        self.encoding_type = encoding_type
        if encoding_type=='bioes':
            self.encoding_method = iob2bioes
        else:
            self.encoding_method = iob2

    def load(self, path:str)->DataSet:
        """
        给定一个文件路径，读取数据。返回的DataSet包含以下的field
            raw_words: List[str]
            target: List[str]
        :param path:
        :return:
        """
        dataset = ConllLoader(headers=['raw_words', 'target'], indexes=[3, 10]).load(path)
        def convert_to_bio(tags):
            bio_tags = []
            flag = None
            for tag in tags:
                label = tag.strip("()*")
                if '(' in tag:
                    bio_label = 'B-' + label
                    flag = label
                elif flag:
                    bio_label = 'I-' + flag
                else:
                    bio_label = 'O'
                if ')' in tag:
                    flag = None
                bio_tags.append(bio_label)
            return self.encoding_method(bio_tags)

        def convert_word(words):
            converted_words = []
            for word in words:
                word = word.replace('/.', '.')  # 有些结尾的.是/.形式的
                if not word.startswith('-'):
                    converted_words.append(word)
                    continue
                # 以下是由于这些符号被转义了，再转回来
                tfrs = {'-LRB-':'(',
                        '-RRB-': ')',
                        '-LSB-': '[',
                        '-RSB-': ']',
                        '-LCB-': '{',
                        '-RCB-': '}'
                        }
                if word in tfrs:
                    converted_words.append(tfrs[word])
                else:
                    converted_words.append(word)
            return converted_words

        dataset.apply_field(convert_word, field_name='raw_words', new_field_name='raw_words')
        dataset.apply_field(convert_to_bio, field_name='target', new_field_name='target')

        return dataset

    def process(self, paths: Union[str, Dict[str, str]], word_vocab_opt:VocabularyOption=None,
                lower:bool=True)->DataInfo:
        """
        读取并处理数据。返回的DataInfo包含以下的内容
            vocabs:
                word: Vocabulary
                target: Vocabulary
            datasets:
                train: DataSet
                    words: List[int], 被设置为input
                    target: int. label，被同时设置为input和target
                    seq_len: int. 句子的长度，被同时设置为input和target
                    raw_words: List[str]
                xxx(根据传入的paths可能有所变化)
        :param paths:
        :param word_vocab_opt: vocabulary的初始化值
        :param lower: 是否使用小写
        :return:
        """
        paths = check_dataloader_paths(paths)
        data = DataInfo()
        input_fields = [Const.TARGET, Const.INPUT, Const.INPUT_LEN]
        target_fields = [Const.TARGET, Const.INPUT_LEN]
        for name, path in paths.items():
            dataset = self.load(path)
            dataset.apply_field(lambda words: words, field_name='raw_words', new_field_name=Const.INPUT)
            if lower:
                dataset.words.lower()
            data.datasets[name] = dataset

        # 对construct vocab
        word_vocab = Vocabulary(min_freq=2) if word_vocab_opt is None else Vocabulary(**word_vocab_opt)
        word_vocab.from_dataset(data.datasets['train'], field_name=Const.INPUT,
                                no_create_entry_dataset=[dataset for name, dataset in data.datasets.items() if name!='train'])
        word_vocab.index_dataset(*data.datasets.values(), field_name=Const.INPUT, new_field_name=Const.INPUT)
        data.vocabs[Const.INPUT] = word_vocab

        # cap words
        cap_word_vocab = Vocabulary()
        cap_word_vocab.from_dataset(*data.datasets.values(), field_name='raw_words')
        cap_word_vocab.index_dataset(*data.datasets.values(), field_name='raw_words', new_field_name='cap_words')
        input_fields.append('cap_words')
        data.vocabs['cap_words'] = cap_word_vocab

        # 对target建vocab
        target_vocab = Vocabulary(unknown=None, padding=None)
        target_vocab.from_dataset(*data.datasets.values(), field_name=Const.TARGET)
        target_vocab.index_dataset(*data.datasets.values(), field_name=Const.TARGET)
        data.vocabs[Const.TARGET] = target_vocab

        for name, dataset in data.datasets.items():
            dataset.add_seq_len(Const.INPUT, new_field_name=Const.INPUT_LEN)
            dataset.set_input(*input_fields)
            dataset.set_target(*target_fields)

        return data


if __name__ == '__main__':
    loader = OntoNoteNERDataLoader()

    if not os.path.isdir(r'./v4_/'):
        os.mkdir(r'./v4_/')

    dataset = loader.load(r'./v4/english/train.txt')
    en_train = open(r'./v4_/en_train.txt', 'w', encoding='utf-8') 
    for i in range(len(dataset.datasets['train'])):
        for j in range(len(dataset.datasets['train']['raw_words'][i])):
            en_train.write(dataset.datasets['train']['raw_words'][i][j] + ' ' + dataset.datasets['train']['target'][i][j] + '\n')
            
    en_train.close()

    dataset = loader.load(r'./v4/english/dev.txt')
    en_dev = open(r'./v4_/en_dev.txt', 'w', encoding='utf-8') 
    for i in range(len(dataset.datasets['train'])):
        for j in range(len(dataset.datasets['train']['raw_words'][i])):
            en_dev.write(dataset.datasets['train']['raw_words'][i][j] + ' ' + dataset.datasets['train']['target'][i][j] + '\n')
            
    en_dev.close()

    dataset = loader.load(r'./v4/english/test.txt')
    en_test = open(r'./v4_/en_test.txt', 'w', encoding='utf-8') 
    for i in range(len(dataset.datasets['train'])):
        for j in range(len(dataset.datasets['train']['raw_words'][i])):
            en_test.write(dataset.datasets['train']['raw_words'][i][j] + ' ' + dataset.datasets['train']['target'][i][j] + '\n')
            
    en_test.close()

    dataset = loader.load(r'./v4/chinese/train.txt')
    ch_train = open(r'./v4_/ch_train.txt', 'w', encoding='utf-8') 
    for i in range(len(dataset.datasets['train'])):
        for j in range(len(dataset.datasets['train']['raw_words'][i])):
            ch_train.write(dataset.datasets['train']['raw_words'][i][j] + ' ' + dataset.datasets['train']['target'][i][j] + '\n')
            
    ch_train.close()

    dataset = loader.load(r'./v4/chinese/dev.txt')
    ch_dev = open(r'./v4_/ch_dev.txt', 'w', encoding='utf-8') 
    for i in range(len(dataset.datasets['train'])):
        for j in range(len(dataset.datasets['train']['raw_words'][i])):
            ch_dev.write(dataset.datasets['train']['raw_words'][i][j] + ' ' + dataset.datasets['train']['target'][i][j] + '\n')
            
    ch_dev.close()

    dataset = loader.load(r'./v4/arabic/train.txt')
    ar_train = open(r'./v4_/ar_train.txt', 'w', encoding='utf-8') 
    for i in range(len(dataset.datasets['train'])):
        for j in range(len(dataset.datasets['train']['raw_words'][i])):
            ar_train.write(dataset.datasets['train']['raw_words'][i][j] + ' ' + dataset.datasets['train']['target'][i][j] + '\n')
            
    ar_train.close()

    dataset = loader.load(r'./v4/arabic/dev.txt')
    ar_dev = open(r'./v4_/ar_dev.txt', 'w', encoding='utf-8') 
    for i in range(len(dataset.datasets['train'])):
        for j in range(len(dataset.datasets['train']['raw_words'][i])):
            ar_dev.write(dataset.datasets['train']['raw_words'][i][j] + ' ' + dataset.datasets['train']['target'][i][j] + '\n')
            
    ar_dev.close()


    


"""
train 115812 2200752
development 15680 304684
test 12217 230111
train 92403 1901772
valid 13606 279180
test 10258 204135
""" 