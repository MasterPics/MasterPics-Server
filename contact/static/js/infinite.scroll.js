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