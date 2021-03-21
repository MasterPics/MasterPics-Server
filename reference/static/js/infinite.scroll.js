//top_button
//Get the button
mybutton = document.getElementById("myBtn");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function () {
    scrollFunction()
};

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        mybutton.style.display = "block";
    } else {
        mybutton.style.display = "none";
    }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}


let infinite = new Waypoint.Infinite({
    element: $('.grid')[0],
    items: '.grid-item',
    onBeforePageLoad: function () {
        console.log("here here")
        $('.loading').show();
    },
    onAfterPageLoad: function () {
        console.log("here here2")
        $('.loading').hide();
        let msnry = new Masonry('.grid', {
            itemSelector: '.grid-item',
            gutter: 10,
        })
    }
});


let msnry = new Masonry('.grid', {
    // optionsW
    itemSelector: '.grid-item',
    gutter: 10,
    // columnWidth: 200
});