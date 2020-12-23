import sys
import requests

auth_params = {
    'key': "",
    'token': "",
}

board_id = ""

base_url = "https://api.trello.com/1/{}"

column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()


def read():
    for column in column_data:
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()

        print('{} ({}):'.format(column['name'], len(task_data)))

        if not task_data:
            print('\t' + 'No tasks')
            continue
        for task in task_data:
            print('\t' + task['name'])


def create(task_name, column_name):
    for column in column_data:
        if column['name'] == column_name:
            requests.post(base_url.format('cards'), data={'name': task_name, 'idList': column['id'], **auth_params})
            print('Success!')
            break


def create_column(column_name):
    columns = []
    for column in column_data:
        columns.append(column['name'])
    if column_name in columns:
        print('The List "{}" already exists. Please choose a different name.'.format(column_name))
    else:
        requests.post(base_url.format('boards') + '/' + board_id + '/lists', data={'name': column_name, **auth_params})
        print('Success!')


def move(task_name, column_name):
    task_id = None
    tasks = []

    for column in column_data:
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()

        for task in task_data:
            if task['name'] == task_name:
                task_obj = {'num': len(tasks) + 1, 'name': task['name'], 'id': task['id'], 'column': column['name']}
                tasks.append(task_obj)

    if len(tasks) > 1:
        print('There are {} cards with the name "{}".'.format(len(tasks), task_name))
        for task in tasks:
            print('{}. {} ({}) -- {}'.format(task['num'], task['name'], task['column'], task['id']))
        num_to_move = int(input('Which of them would you like to move? Please enter the number: '))
        if num_to_move > len(tasks):
            print('Incorrect input')
        else:
            for task in tasks:
                if task['num'] == num_to_move:
                    task_id = task['id']
                    break
            for column in column_data:    
                if column['name'] == column_name:    
 
                    requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})    
                    break 


    elif len(tasks) == 1:
        task_id = tasks[0]['id']

        for column in column_data:
            if column['name'] == column_name:    
                requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})    
     

    else:
        print('No card "{}" found.'.format(task_name))





if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] =='create_column':
        create_column(sys.argv[2])
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])
