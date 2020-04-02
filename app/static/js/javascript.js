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

function init(){


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

    }
    
}

function search(event){

    location.search = "?id=" + document.getElementById("topsearch").value;
    
}


window.onload = () => {updateNav(); init()};
window.onhashchange = () => updateNav();

