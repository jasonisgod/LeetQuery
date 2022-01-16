
var url = 'https://leetcode.com/graphql'
var data = 
{
    operationName: "getContestRankingData",
    query: "query getContestRankingData($username: String!) {\n  userContestRanking(username: $username) {\n    attendedContestsCount\n    rating\n    globalRanking\n    __typename\n  }\n  userContestRankingHistory(username: $username) {\n    contest {\n      title\n      startTime\n      __typename\n    }\n    rating\n    ranking\n    __typename\n  }\n}\n",
    variables: {username: "leovincentseles"}
}

fetch(url, {
    method: "POST",
    origin: 'https://leetcode.com',
    headers: 
    {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin':'*'
    }, 
    body: JSON.stringify(data)
}).then(res => {
    console.log(res);
});