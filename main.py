import os

import requests
import speedtest
import sys
import csv

headers = {"Authorization": "bearer GitHub API Token"}
request_repetitions = 10
graphQL_queries = [
    """
    {
      search(query:"language:java, stars:>100", type:REPOSITORY, first:1) {
      nodes {
        ... on Repository {
          nameWithOwner
          url
          stargazerCount
        }
       }
      }
    }
    """,
    """
    {
      search(query:"language:java, stars:>100", type:REPOSITORY, first:50) {
      nodes {
        ... on Repository {
          nameWithOwner
          url
          stargazerCount
          pullRequests{
            totalCount
          }
        }
       }
      }
    }
    """,
    """
    {
      search(query:"language:java, stars:>100", type:REPOSITORY, first:100) {
      nodes {
        ... on Repository {
          nameWithOwner
          url
          forkCount
          stargazerCount
          watchers{
            totalCount
          }
          pullRequests{
            totalCount
          }
        }
       }
      }
    }
    """
]
rest_queries = [
    "https://api.github.com/search/repositories?q=language:java+stars:%3E100&sort=stars&order=desc&page=1&per_page=25",
    "https://api.github.com/search/repositories?q=language:java+stars:%3E100&sort=stars&order=desc&page=1&per_page=50"
    "https://api.github.com/search/repositories?q=language:java+stars:%3E100&sort=stars&order=desc&page=1&per_page=100"]


def run_graphql_query(query):
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    print(f"Response content = {request.content}")
    print(f"Response time = {request.elapsed.microseconds} microseconds")
    print(f"Response size = {sys.getsizeof(request.content)} bytes")
    return request.elapsed.microseconds, sys.getsizeof(request.content)


def run_rest_query(query):
    request = requests.get(query)
    print(f"Response content = {request.content}")
    print(f"Response time = {request.elapsed.microseconds} microseconds")
    print(f"Response size = {sys.getsizeof(request.content)} bytes")
    return request.elapsed.microseconds, sys.getsizeof(request.content)


def make_speed_test():
    try:
        speed = speedtest.Speedtest()
        download = speed.download() / 1024 / 1024
        valid_speed = 140 > download > 100
        return valid_speed, download
    except Exception as e:
        return False, 0


def write_csv(content):
    results_file_name = 'results.csv'
    with open(results_file_name, mode='a+') as results_file:
        writer = csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(content)


def setup_results():
    results_file = 'results.csv'
    if not os.path.exists(results_file):
        with open(results_file, mode='w') as results_file:
            writer = csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            header = ['ResponseTime', 'ResponseSize', 'DownloadSpeed']
            writer.writerow(header)


def main():
    setup_results()
    for query in graphQL_queries:
        for _ in range(request_repetitions):
            valid_speed = False
            while not valid_speed:
                valid_speed, download = make_speed_test()
            response_time, response_size = run_graphql_query(query)
            print(f"Speed test download {download} Mb/s")
            write_csv([response_time, response_size, download])
    for query in rest_queries:
        for _ in range(request_repetitions):
            valid_speed = False
            while not valid_speed:
                valid_speed, download = make_speed_test()
            response_time, response_size = run_rest_query(query)
            write_csv([response_time, response_size, download])
            print(f"Speed test download {download} Mb/s")


if __name__ == '__main__':
    main()
