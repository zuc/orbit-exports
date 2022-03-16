import os
import requests
import sys

def main():
    api_token = os.getenv('ORBIT_API_TOKEN') or sys.exit('No ORBIT_API_TOKEN found in env vars.')
    workspace = os.getenv('ORBIT_WORKSPACE') or sys.exit('No ORBIT_WORKSPACE found in env vars.')

    auth_header = {'Authorization': 'Bearer {}'.format(api_token)}

    exported_orgs = []
    base_url = 'https://app.orbit.love/api/v1'
    page_url = '/{}/organizations'.format(workspace)
    finished = False

    while finished != True:
        r = requests.get('{}{}'.format(base_url, page_url), headers=auth_header)
        data = r.json()
        for org in data['data']:
            org_attr = org['attributes']
            item = {'name': org_attr['name'], 'website': org_attr['website'], 'members_count': org_attr['members_count'],
                    'employees_count': org_attr['employees_count'], 'last_active': org_attr['last_active'],
                    'active_since': org_attr['active_since']}
            exported_orgs.append(item)
        if data['links']['next'] == None:
            finished = True
        else:
            page_url = data['links']['next']

    with open('orgs.csv', 'w') as f:
        f.write('name,website,members_count,employees_count,last_active,active_since\n')
        for org in exported_orgs:
            f.write('{},{},{},{},{},{}\n'.format(org['name'], org['website'], org['members_count'], org['employees_count'],
            org['last_active'], org['active_since']))

    return 0

if __name__ == '__main__':
    sys.exit(main())
