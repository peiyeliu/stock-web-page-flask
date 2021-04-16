/**
 * tab menu switch function
 * @param tab
 */
function changetab(tab) {
    var heads = document.getElementsByClassName("menu")[0].getElementsByTagName('li');
    var contents = document.getElementsByClassName("con")[0].getElementsByTagName('div');
    for(var i = 0, len = heads.length; i < len; i++) {
        if(heads[i] === tab) {
            heads[i].className = 'active';
            contents[i].className = 'displayed';
        } 
        else {
            heads[i].className = '';
            contents[i].className = '';
        }
    }
}

/**
 * clear the search result when clicking the "clear" button
 */


function showChart(){
    document.getElementById("container").style.display="block"
}

function hideChart(){
    document.getElementById("container").style.display="none"
}

function clearPage(){
    window.location.replace("/")
}


