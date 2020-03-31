function updateNav(){ //Updates Navbar and currently displayed content based on URL hash path.

    if(location.hash === ""){location.hash = "#Home"};

    hash = location.hash.substr(1, location.hash.length).toLowerCase();

    navLinks = document.getElementById("nav_links").getElementsByTagName("a"); //Iterates through and updates nav links.

    for (let i = 0; i < navLinks.length; i++) { 

        let link = navLinks[i]

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


window.onload = () => updateNav();
window.onhashchange = () => updateNav();