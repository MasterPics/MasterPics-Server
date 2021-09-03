let infinite = new Waypoint.Infinite({
    element: $('.grid')[0],
    items: '.grid-content',
    onBeforePageLoad: function () {
        $('.loading').show();
    },
    onAfterPageLoad: function () {
        $('.loading').hide();
        let msnry = new Masonry('.grid', {
            itemSelector: '.grid-content',
            gutter: 10,
        })
    }
});
let msnry = new Masonry('.grid', {
    // optionsW
    itemSelector: '.grid-content',
    gutter: 10,
    // columnWidth: 200
});