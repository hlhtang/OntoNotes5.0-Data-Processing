import os, sys

Named_Entity = ['CARDINAL\n',
                'DATE\n',
                'EVENT\n',
                'FAC\n',
                'GPE\n',
                'LANGUAGE\n',
                'LAW\n',
                'LOC\n',
                'MONEY\n',
                'NORP\n',
                'ORDINAL\n',
                'ORG\n',
                'PERCENT\n',
                'PERSON\n',
                'PRODUCT\n',
                'QUANTITY\n',
                'TIME\n',
                'WORK_OF_ART\n']

with open(r'./v4_/ch_train.txt', 'r', encoding='utf-8') as ch_train:
    ch_train_ = open(r'./v4_/ch_train_.txt', 'w', encoding='utf-8')
    for i in ch_train:
        i = i.split(' ')
        if i[1] in ['B-'+ NE for NE in Named_Entity]:
            for raw_ch_index in range(len(i[0])):
                if raw_ch_index == 0:
                    ch_train_.write(i[0][raw_ch_index] + ' B-' + i[1][2:])
                else:
                    ch_train_.write(i[0][raw_ch_index] + ' I-' + i[1][2:])

        if i[1] in ['I-'+ NE for NE in Named_Entity]:
            for raw_ch_index in range(len(i[0])):
                ch_train_.write(i[0][raw_ch_index] + ' I-' + i[1][2:])

        if i[1] == 'O\n':
            if i[0] == '。':
                ch_train_.write(i[0] + ' O' + '\n')
                ch_train_.write('\n')
            else:
                for raw_ch_index in range(len(i[0])):
                    ch_train_.write(i[0][raw_ch_index] + ' O' + '\n')

    ch_train_.close()

with open(r'./v4_/ch_dev.txt', 'r', encoding='utf-8') as ch_dev:
    ch_dev_ = open(r'./v4_/ch_dev_.txt', 'w', encoding='utf-8')

    for i in ch_dev:
        i = i.split(' ')
        if i[1] in ['B-'+ NE for NE in Named_Entity]:
            for raw_ch_index in range(len(i[0])):
                if raw_ch_index == 0:
                    ch_dev_.write(i[0][raw_ch_index] + ' B-' + i[1][2:])
                else:
                    ch_dev_.write(i[0][raw_ch_index] + ' I-' + i[1][2:])

        if i[1] in ['I-'+ NE for NE in Named_Entity]:
            for raw_ch_index in range(len(i[0])):
                ch_dev_.write(i[0][raw_ch_index] + ' I-' + i[1][2:])

        if i[1] == 'O\n':
            if i[0] == '。':
                ch_dev_.write(i[0] + ' O' + '\n')
                ch_dev_.write('\n')
            else:
                for raw_ch_index in range(len(i[0])):
                    ch_dev_.write(i[0][raw_ch_index] + ' O' + '\n')

    ch_dev_.close()