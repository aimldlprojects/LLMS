




strftime('%Y-%m-%d', substr(date_text, 7, 4) || '-' || substr(date_text, 1, 2) || '-' || substr(date_text, 4, 2))
''')


cursor.execute('''
    UPDATE your_table
    SET date_text = strftime('%Y-%m-%d', substr(date_text, 7, 4) || '-' || substr(date_text, 1, 2) || '-' || substr(date_text, 4, 2))
''')
