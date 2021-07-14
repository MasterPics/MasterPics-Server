let infinite = new Waypoint.Infinite({

    element: $('.grid')[0],
    items: '.grid-item',
    onBeforePageLoad: function () {
        $('.loading').show();
    },
    onAfterPageLoad: function () {
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