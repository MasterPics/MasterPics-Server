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