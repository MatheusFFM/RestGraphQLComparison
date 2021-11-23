import requests
import speedtest
import sys


headers = {"Authorization": "bearer git token"}
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
rest_queries = ["https://api.github.com/search/repositories?q=language:java+stars:%3E100&sort=stars&order=desc&page=1&per_page=25", 
                "https://api.github.com/search/repositories?q=language:java+stars:%3E100&sort=stars&order=desc&page=1&per_page=50"
                "https://api.github.com/search/repositories?q=language:java+stars:%3E100&sort=stars&order=desc&page=1&per_page=100"]


def run_graphql_query(query):
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    print(f"Response content = {request.content}")
    print(f"Response time = {request.elapsed.microseconds} microseconds")
    print(f"Response size = {sys.getsizeof(request.content)} bytes")


def run_rest_query(query):
    request = requests.get(query)
    print(f"Response content = {request.content}")
    print(f"Response time = {request.elapsed.microseconds} microseconds")
    print(f"Response size = {sys.getsizeof(request.content)} bytes")


def make_speed_test():
    speed = speedtest.Speedtest()
    download = speed.download() / 1024 / 1024
    valid_speed = 180 > download > 150
    return valid_speed, download


def main():
    for query in graphQL_queries:
        for _ in range(request_repetitions):
            valid_speed = False
            while not valid_speed:
                valid_speed, download = make_speed_test()
            run_graphql_query(query)
            print(f"Speed test download {download} Mb/s")
    for query in rest_queries:
        for _ in range(request_repetitions):
            run_rest_query(query)



if __name__ == '__main__':
    main()
