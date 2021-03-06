import os
import sqlite3

import database_handler

PATH = '{}/test_data/temp_db.sqlite3'.format(os.getcwd())


class Test_database_handler:

    def teardown_method(self, method):
        os.remove(PATH)

    def test_create_table(self):
        expected = ['id', 'case_number', 'case_date', 'incident', 'ori', 'age', 'arrest_type',
                    'name', 'address', 'apartment', 'city', 'state', 'zip', 'dob', 'phone', 'race', 'sex',
                    'subject_type', 'district', 'status']

        db = sqlite3.connect(PATH)
        cursor = db.cursor()
        database_handler.create_table(cursor)
        db.commit()
        cursor = db.execute('select * from cases')
        headers = [description[0] for description in cursor.description]
        db.close()
        assert headers == expected

    def test_query_status(self):
        db = sqlite3.connect(PATH)
        cursor = db.cursor()
        database_handler.create_table(cursor)

        test_row = ['1', '2', '3', '4', '5', '6', '7', '8',
                    '9', '10', '11', '12', '13', '14', '15', '16', '17', '18']

        test_row1 = ['10', '2', '3', '4', '5', '6', '7', '8',
                     '9', '10', '11', '12', '13', '14', '15', '16', '17', '18']

        database_handler.insert_rows(cursor, [test_row, test_row1])

        assert len(database_handler.query_status(cursor, 0)) == 2
        assert database_handler.query_status(cursor, 0)[0] == (1, '1', '2', '3', '4', '5', '6', '7', '8',
                                                               '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', 0)

        assert database_handler.query_status(cursor, 0)[1] == (2, '10', '2', '3', '4', '5', '6', '7', '8',
                                                               '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', 0)

    def test_offense_types(self):

        db = sqlite3.connect(PATH)
        cursor = db.cursor()
        database_handler.create_table(cursor)

        test_row = ['2015-57325012', '10/11/2015', 'valid', 'NQ4054983', '26', 'cited', 'name1',
                    '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '55555', '10/30/1998', '63-(829)189-2968',
                    'White', 'Male', '', 'central']

        test_row1 = ['2015-57325012', '10/11/2015', 'invalid', 'NQ4054983', '26', 'cited', 'name2',
                     '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '55555', '10/30/1998', '63-(829)189-2968',
                     'White', 'Male', '', 'central']

        test_row2 = ['2015-57325012', '10/11/2015', 'invalid', 'NQ4054983', '26', 'cited', 'name3',
                     '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '55555', '10/30/1998', '63-(829)189-2968',
                     'White', 'Male', '', 'central']

        database_handler.insert_rows(cursor, [test_row, test_row1, test_row2])

        assert 'valid' in database_handler.offense_types(cursor)

        assert 'invalid' in database_handler.offense_types(cursor)

        assert len(database_handler.offense_types(cursor)) == 2

    def test_receipt(self):

        db = sqlite3.connect(PATH)
        cursor = db.cursor()
        database_handler.create_table(cursor)

        test_row = ['2015-57325011', '10/11/2015', 'valid', 'NQ4054983', '26', 'cited', 'name1',
                    '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '55555', '10/30/1998', '63-(829)189-2968',
                    'White', 'Male', '', 'central']

        test_row1 = ['2015-57325012', '10/11/2015', 'invalid', 'NQ4054983', '26', 'cited', 'name2',
                     '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '55555', '10/30/1998', '63-(829)189-2968',
                     'White', 'Male', '', 'central']

        test_row2 = ['2015-57325013', '10/11/2015', 'invalid', 'NQ4054983', '26', 'cited', 'name3',
                     '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '55555', '10/30/1998', '63-(829)189-2968',
                     'White', 'Male', '', 'central']

        test_row3 = ['2016-57325014', '10/11/2015', 'invalid', 'NQ4054983', '26', 'cited', 'name4',
                     '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '55555', '10/30/1998', '63-(829)189-2968',
                     'White', 'Male', '', 'central']

        database_handler.insert_rows(cursor, [test_row, test_row1, test_row2, test_row3])
        database_handler.update_status(cursor, 11, 1)
        database_handler.update_status(cursor, 10, 2)
        database_handler.update_status(cursor, 1, 3)
        database_handler.update_status(cursor, 100, 4)

        receipt = database_handler.receipt(cursor)
        assert len(receipt) == 3

        assert receipt[0] == ['2015-57325013', 'name3', 'invalid', 'central']
        assert receipt[1] == ['2015-57325012', 'name2', 'invalid', 'central']
        assert receipt[2] == ['2015-57325011', 'name1', 'valid', 'central']


