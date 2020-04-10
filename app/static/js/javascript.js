
var client_id = "va97w97mn1qzq0nlrjavlifr92lstz"; //Twitch-API Client ID

var result_template = 
'<a class="result_card" href="https://www.twitch.tv/{NAME}">\
<img src="{THUMBNAIL}">\
<div class="gradient"></div>\
<img class="avatar" src="https://static-cdn.jtvnw.net/user-default-pictures-uv/75305d54-c7cc-40d1-bb9c-91fbe85943c7-profile_image-150x150.png">\
<p class="stream_username">{NAME}</p>\
<p class="stream_title">{TITLE}</p>\
<p class="stream_viewers">•{VIEWERS}</p>\
<p class="result_label">{INDEX}</p>\
</a>';


function updateNav(){ //Updates Navbar and currently displayed content based on URL hash path.

    if(location.hash === ""){location.hash = "#Home"};

    hash = location.hash.substr(1, location.hash.length).toLowerCase();

    navLinks = document.getElementById("nav_links").getElementsByTagName("a"); //Iterates through and updates nav links.

    for (let i = 0; i < navLinks.length; i++) { 

        let link = navLinks[i];

        let id = link.id.substr(4, link.id.length).toLowerCase();

        if (id === hash)

            link.className = "navlink nav_active";

        else

            link.className = "navlink";

    } 

    pages = document.getElementById("pages").getElementsByClassName("content_container"); //Iterates through and updates content divs.

    for (let i = 0; i < pages.length; i++) { 

        let page = pages[i];

        let id = page.id.substr(8, page.id.length).toLowerCase();

        if (id === hash)

            page.className = "content_container content_active";

        else

            page.className = "content_container";

    } 

}


const options = {
    responseType: 'json',
    headers: {'Client-ID': client_id}
};

function getID(username){

    axios.get('https://api.twitch.tv/helix/users?login=' + encodeURI(username), options).then(response => {

        if (response.data.data.length > 0){
            
            //console.log(response.data.data[0].id);
            getFollows(response.data.data[0].id);
            console.log(response.data.data);
            
        }else{

            console.log("INVALID USERNAME");
        }

    });

}

function getFollows(id){


    axios.get('https://api.twitch.tv/helix/users/follows?first=100&from_id=' + id, options).then(response => {

        let add = "";

        response.data.data.map( function (value) {

            add += "&user_id=" + value.to_id; //Generate URL query parameters, in this case a list of users.

        });

        getStreams(add);

    });
}

function getStreams(add){

    axios.get('https://api.twitch.tv/helix/streams?first=5' + add, options).then(response =>{



        console.log(response.data);
        renderStreams(response.data.data.slice(0,5));


    })

}

function renderStreams(data){
    let generatedHTML = '<div class="empty"></div>';

    data.map((stream, i) => {

        generatedHTML += result_template.replace("{NAME}", stream.user_name).replace("{NAME}", stream.user_name).replace("{TITLE}", stream.title).replace("{VIEWERS}", stream.viewer_count.toLocaleString()).replace("{THUMBNAIL}", stream.thumbnail_url.replace("{width}x{height}", "300x168")).replace("{INDEX}", i + 1);

        

    })

    document.getElementById("content_results").innerHTML += generatedHTML + '<div class="empty"></div>';
}



function init(){
    console.log(options)
    
    
    //Update both search bars when value is changed. Needs to be optimized/rewritten.
    let topsearch = document.getElementById("topsearch");
    let midsearch = document.getElementById("midsearch");
    topsearch.addEventListener("input", () => {midsearch.value = topsearch.value});
    midsearch.addEventListener("input", () => {topsearch.value = midsearch.value});


    //Handle firing of search function on form submission.
    document.getElementsByClassName("searchbar_wrapper")[0].addEventListener("submit", (event)=>{event.preventDefault(); search(event)});
    document.getElementsByClassName("searchbar_wrapper")[1].addEventListener("submit", (event)=>{event.preventDefault(); search(event)});


    //Check if url already contains username to search, whether from a saved bookmark or from submitting searchbar form.
    searchParams = new URLSearchParams(location.search);

    if(searchParams.has("id")){

        midsearch.value = searchParams.get("id");
        topsearch.value = searchParams.get("id");
        document.getElementById("nav_results").innerHTML = searchParams.get("id").toUpperCase();
        getID(searchParams.get("id"));
    }
    
}

function search(event){
    location.hash = "#Results"
    location.search = "?id=" + document.getElementById("topsearch").value;

}


window.addEventListener("load", () => {updateNav(); init()});
window.addEventListener("hashchange",() => updateNav());

