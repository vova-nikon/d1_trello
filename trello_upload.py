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
    tasks = []
    for column in column_data:
        if column['name'] == column_name:
            task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
            for task in task_data:
                tasks.append(task['name'])
            if task_name in tasks:
                print('The card "{}" already exists in this List. Please choose a different name or update the name of the other card.'.format(task_name))
                break
            else:
                requests.post(base_url.format('cards'), data={'name': task_name, 'idList': column['id'], **auth_params})
                print('Success!')
                break

def create_column(column_name):
    columns = []
    for column in column_data:
        columns.append(column['name'])
    if column_name in columns:
        print('The List "{}" already exists. Please choose a different name or update the name of the other card by using update_card(old_name, new_name, column_name).'.format(column_name))
    else:
        requests.post(base_url.format('boards') + '/' + board_id + '/lists', data={'name': column_name, **auth_params})
        print('Success!')

def move(task_name, column_name):
    tasks = []
    task_id = None

    for column in column_data:
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()

        for task in task_data:
            if task['name'] == task_name:
                task_id = task['id']
                break
        if task_id:
            break

    for column in column_data:
        if column['name'] == column_name:
            task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
            for task in task_data:
                tasks.append(task['name'])
            if task_name in tasks:
                print('The card "{}" already exists in the list "{}". Please choose a different name or update the name of the other card by using update_card(old_name, new_name, column_name).'.format(task_name, column_name))
                break
            else:
                requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})
                print('Success!')
                break


def update_card(old_name, new_name, column_name):
    tasks = []
    task_id = None
    for column in column_data:
        if column['name'] == column_name:
            task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
            for task in task_data:
                tasks.append(task['name'])
            if new_name in tasks:
                print('The card "{}" already exists in the list "{}". Please choose a different name or update the name of the other card by using update_card(old_name, new_name, column_name).'.format(new_name, column_name))
                break
            else:
                if task['name'] == old_name:
                    task_id = task['id']
                    requests.put(base_url.format('cards') + '/' + task_id, data={'name': new_name, **auth_params})
                    print('Success!')
                    break




if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] =='create_column':
        create_column(sys.argv[2])
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'update_card':
        update_card(sys.argv[2], sys.argv[3], sys.argv[4])


