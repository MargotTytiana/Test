import requests
from bs4 import BeautifulSoup
import csv


def get_issue_details(issue_url):
    response = requests.get(issue_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    issue_type = soup.find('span', {'id': 'type-val'}).text.strip()
    priority = soup.find('span', {'id': 'priority-val'}).text.strip()
    status = soup.find('span', {'id': 'status-val'}).text.strip()
    assignee = soup.find('span', {'id': 'assignee-val'}).text.strip()

    # Extract links
    links = soup.find_all('a')
    for link in links:
        print(link.get('href'))
    header_links = soup.find_all('a', string='GitHub Pull Request #1348')

    # Handle the 'created' span
    created_span = soup.find('span', {'id': 'created-val'})
    created_date = created_span.text.strip() if created_span else None
    created_epoch = created_span.find_next_sibling('span')[
        'data-time'] if created_span and created_span.find_next_sibling('span') else None

    description = soup.find('div', {'id': 'description-val'}).text.strip()

    comments = []
    for comment in soup.find_all('div', class_='issue-data-block'):
        commenter = comment.find('a', {'class': 'user-hover'}).text.strip()
        comment_text = comment.find('div', {'class': 'action-body'}).text.strip()

        comments.append({
            'Commenter': commenter,
            'Comment': comment_text
        })

    return {
        'Type': issue_type,
        'Priority': priority,
        'Status': status,
        'Assignee': assignee,
        'Created': created_date,
        'Created Epoch': created_epoch,
        'Description': description,
        'Issue Links': header_links,
        'Comments': comments
    }


def write_to_csv(data, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Type', 'Priority', 'Status', 'Assignee', 'Created', 'Created Epoch',
                      'Description', 'Comments', 'Issue Links']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(data)

    for comment_data in data['Comments']:
        writer.writerow({
            'Type': data['Type'],
            'Priority': data['priority'],
            'Status': data['status'],
            'Assignee': data['Assignee'],
            'Created': data['Created'],
            'Created Epoch': data['Created Epoch'],
            'Description': data['Description'],
            'Commenter': comment_data['Commenter'],
            'Comment': comment_data['Comment'],
            'Issue Links': data['Issue Links']
        })


if __name__ == "__main__":
    issue_url = 'https://issues.apache.org/jira/browse/CAMEL-10597'
    output_csv = 'camel_issue.csv'

    issue_data = get_issue_details(issue_url)
    write_to_csv(issue_data, output_csv)
