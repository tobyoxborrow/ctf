import json
import requests


def api_v1_get(command=''):
    '''Perform a "normal" v1 API GET request'''

    url = 'https://network-degree-db-2016.captchaflag.com/%s' % command

    headers = {
    #    'Authorization': 'Token token={0}'.format(api_access_key),
    #    'Content-Type': 'application/json',
        }

    response = requests.get(url, headers=headers)

    return response


def get_students():
    r = api_v1_get('students')
    j = r.json()
    return j


def get_student(student_id):
    r = api_v1_get('students/%s' % student_id)
    j = r.json()
    return j


def get_advisor(advisor_id):
    r = api_v1_get('advisors/%s' % advisor_id)
    j = r.json()
    return j


def main():
    students = get_students()
    for student in students:
        for key in student.keys():
            if key == 'degrees':
                continue
            print('%s: %s' % (key, student[key]))
        # suid = student['uid']
        # si = get_student(suid)
        if 'degrees' not in student:
            continue
        print('Degrees:')
        degrees = student['degrees']
        for degree in degrees:
            for key in degree.keys():
                if key == 'advisor':
                    continue
                print('%s: %s' % (key, degree[key]))
            if 'advisor' not in degree:
                continue
            advisor = get_advisor(degree['advisor']['id'])
            if not advisor:
                continue
            print('Advisors:')
            print(advisor)
        print('')
        print('')


if __name__ == '__main__':
    main()
