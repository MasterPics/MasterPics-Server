let infinite = new Waypoint.Infinite({

    element: $('.grid')[0],
    items: '.grid-item',
    onBeforePageLoad: function () {
        $('.loading').show();
    },
    onAfterPageLoad: function () {
        $('.loading').hide();
        let msnry = new Masonry('.grid', {
            // optionsW
            itemSelector: '.grid-item',
            columnWidth: 270,
            gutter: 20,
            isFitWidth: true
        });
    }
});
let msnry = new Masonry('.grid', {
    // optionsW
    itemSelector: '.grid-item',
    columnWidth: 270,
    gutter: 20,
    isFitWidth: true
});