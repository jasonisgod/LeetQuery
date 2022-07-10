
var DOMAIN = 'http://jasonisgod.xyz:9003';
// var DOMAIN = 'http://127.0.0.1:9003';
var TOP_N = 5;
var VER_JS = 'v2.0.1';
var TIME_RELOAD = 60000;
var TIME_DELAY_1 = 2000;
var TIME_DELAY_2 = 5000;

$(document).ready(function(){ init(); });

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    var modal = document.getElementById("codeModal");
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

var baseUrl = location.href.substring(0, location.href.lastIndexOf('/'));
var tableData = {};
var usernameList = [];
var contestList = [];
var handicapList = {};

function requestHandicap() {
    return $.ajax({
        url: DOMAIN + '/api/get/config/handicap', 
        success: (data, status, xhr) => handicapList = JSON.parse(data)
    });
}

function requestUsername() {
    return $.ajax({
        url: DOMAIN + '/api/get/config/username', 
        success: (data, status, xhr) => usernameList = JSON.parse(data)
    });
}

function requestContest() {
    return $.ajax({
        url: DOMAIN + '/api/get/config/contest', 
        success: (data, status, xhr) => contestList = JSON.parse(data)
    });
}

function requestData(contest, username) {
    return $.ajax({
        url: DOMAIN + '/api/get/data/' + contest + '/' + username, 
        success: (data, status, xhr) => {
            if (data != '') {
                tableData[contest].push(JSON.parse(data))
            }
        }
    });
}

function init() {

    $('#ver-display').html(VER_JS);
    requestHandicap();
    requestUsername();
    requestContest();

    // $.when(requestHandicap(), requestUsername(), requestContest()).done( (a1, a2, a3) => {    });
    setTimeout(() => {
        contestList = contestList.slice(0, TOP_N)
        contestList.forEach(contest => {
            tableData[contest] = [];
            usernameList.forEach(username => requestData(contest, username));
        });
    }, TIME_DELAY_1);

    setTimeout(() => {
        initTables();
        updateTables();
        hljsUpdate();
        hideLoading();
        console.log(handicapList);
        console.log(usernameList);
        console.log(contestList);
        console.log(tableData);
    }, TIME_DELAY_2);

    setTimeout(() => location.reload(), TIME_RELOAD);
}

function hideLoading() {
    $('#loading').hide();
}

function initTables() {
    contestList.forEach(contest => {
        var h3 = $('<h3>').html(contest);
        $('#box').append(h3);
        var div = $('<div id="' + contest + '"></div>');
        $('#box').append(div);
    });
}

function updateTables() {
    contestList.forEach(contest => {
        if (tableData[contest].length == 0) {
            $('#' + contest).html('[ No Data ]');
            return;
        }
        // console.log(contest);
        tableData[contest].forEach(e => {
            e['handicap'] = getHandicap(contest, e['username']);
            e['black_time'] = getBlackTime(e['handicap'], e['finish_time']);
            // console.log(contest, e['username'], e['handicap'], e['black_time']);
        });
        tableData[contest].sort(function(a, b) {
            var aScore = parseInt(a['score']);
            var bScore = parseInt(b['score']);
            if (aScore != bScore) return bScore - aScore;
            var aBlackTime = a['black_time'];
            var bBlackTime = b['black_time'];
            return aBlackTime - bBlackTime;
        });
        var table = $('<table></table>');
        var tr = $('<thead></thead>');
            tr.append($('<td>Rank</td>'));
            tr.append($('<td>Username</td>'));
            tr.append($('<td>Score</td>'));
            tr.append($('<td>Time</td>'));
            tr.append($('<td>???</td>'));
            tr.append($('<td>Q1 </td>'));
            tr.append($('<td>Q2 </td>'));
            tr.append($('<td>Q3 </td>'));
            tr.append($('<td>Q4 </td>'));
            tr.append($('<td>(Rank)</td>'));
        table.append(tr);
        var count = 1;
        tableData[contest].forEach(e => {
            var tr = $('<tr></tr>');
            tr.append($('<td></td>').text(count)); count++;
            tr.append($('<td></td>').html(e['username'].padEnd(15).replaceAll(' ', '&nbsp')));
            tr.append($('<td></td>').text(e['score']));
            tr.append($('<td></td>').html(e['finish_time']));
            var handicap_str = e['handicap'] == 0? '': '+' + e['handicap'];
            tr.append($('<td></td>').html(handicap_str));
            for (var i = 1; i <= 4; i++) {
                if (e['Q' + i]['solve_time'] == undefined) {
                    tr.append($('<td>.............</td>'));
                    continue;
                }
                var id = contest + '-' + e['username'];
                var solve_time = e['Q' + i]['solve_time'];
                var fail_count = e['Q' + i]['fail_count'];
                var code = e['Q' + i]['code'];
                var td = $('<td></td>').addClass('q');
                var span1 = $('<span></span>').html(solve_time);
                var onclickCmd = "showCode('"+contest+"','"+e['username']+"','"+('Q' + i)+"')";
                var button = $('<button><b>&#60;/&#62;</b></button>').attr("id", 'btn-' + id).attr("onclick", onclickCmd);
                var fail_count_str = (fail_count == 0? '&nbsp&nbsp&nbsp': '+' + fail_count);
                var span2 = $('<span></span>').html(fail_count_str);
                td.append(span1).append(button).append(span2);
                tr.append(td);
            }
            tr.append($('<td></td>').text(e['rank']));
            table.append(tr);
        });
        $('#' + contest).html('').append(table);
    });
}

function getHandicap(contest, username) {
    var handicap = handicapList[contest + '-' + username];
    if (handicap == undefined) handicap = 0;
    return handicap;
}

function getBlackTime(handicap, finish_time_str) {
    var datetime = new Date('1970-01-01T' + finish_time_str + 'Z');
    var blackTime = Date.parse(datetime) + (handicap * 60 * 1000);
    return blackTime;
}

function showCode(contest, username, question) {
    // console.log(contest, username, question);
    tableData[contest].forEach(e => {
        if (e['username'] == username) {
            var code = e[question]['code'];
    code = code.replace(/</gi,'&lt;').replace(/>/gi,'&gt;');
            $('#code').removeAttr("class");
            try {
                var lang = e[question]['lang'].trim();
                if (lang == 'python3')
                    lang = 'python';
                // console.log(lang);
                $('#code').addClass('language-' + lang);
            } catch (e) {
                console.log(e);
            }

            $('#code').html(code);
            // console.log(code);
        }
    });
    hljsUpdate();
    var codeModal = document.getElementById("codeModal");        
    codeModal.style.display = "block";        
    // $([document.documentElement, document.body]).animate({ scrollTop: $("#code").offset().top }, 1000);
}

function hljsUpdate() {
    hljs.highlightAll();
    hljs.initLineNumbersOnLoad();
}

function fetchBoard() {
    tableData = {}
    contestList.forEach(contest => {
        tableData[contest] = [];
        usernameList.forEach(username => {
            var url = (baseUrl) + '/files/' + contest + '-' + username + '.json';
            fetchFile(url, json => tableData[contest].push(json));
        });
    });
}

function fetchFile(url, func) {
    var headers = new Headers();
    headers.append('Content-Type', 'application/json');
    headers.append('Accept', 'application/json');
    fetch(url, {
        mode: 'cors',
        credentials: 'include',
        method: 'GET',
        headers: headers
    }).then(response => response.json())
        .then(json => func(json))
        .catch(error => console.log(error.message));
}

function myTimer() {
    fetchHandicap();
    fetchBoard();
    // TODO: replace by $.when(fetch1, fetch2, fetch3, ...)
    setTimeout(updateTables, 2000);
}

function closeModal() {
    var codeModal = document.getElementById("codeModal");        
    codeModal.style.display = "none"; 
}
